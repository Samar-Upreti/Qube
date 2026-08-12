import speech_recognition as sr
from pathlib import Path
import sounddevice as sd
import os

from src.responce.wake_calls import wake
from src.responce.greet import greeting
from src.services.qube_voice import qube_voice
from src.responce.commands import open_command

def listen_commands():

    r = sr.Recognizer()
    WAKE_WORD = wake()
    open_commands = open_command()

    state = "listening"

    sample_rate = 16000
    duration = 3
    
    while True:
        try:
            audio = sd.rec(
                int(sample_rate * duration),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            audio_data = sr.AudioData(
                audio.tobytes(),
                sample_rate,
                2
            )

            text = r.recognize_google(audio_data).strip().casefold()

            if state == "listening":

                if text in WAKE_WORD:
                    greet = greeting()
                    qube_voice(greet)
                    state = "command"

            elif state == "command":
                if text in open_commands:
                    os.startfile(open_commands[text])

                    #for model training 
                    Base_Dir = Path(__file__).resolve().parent.parent.parent
                    audio_txt = Base_Dir/"src"/"data"/"given_commands"/"command.txt"
                    with open (audio_txt, "a",encoding="utf-8") as command:
                        command.write(text + "\n")
                        
                    state = "listening"  
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass 
        except Exception as e:
            print(f"Error: {e}")
    

if __name__ == "__main__":
    listen_commands()