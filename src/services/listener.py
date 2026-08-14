import whisper
from openwakeword.model import Model
import sounddevice as sd
import numpy as np
import webbrowser
import webrtcvad 
from pathlib import Path
from difflib import get_close_matches
from collections import deque

from src.responce.wake_calls import wake
from src.responce.greet import greeting,greeting_again
from src.responce.commands import open_command
from src.services.qube_voice import voice

def listen_commands():

    sample_rate = 16000
    chunck_size = 320
    channel = 1
    silence_limit = 0.7

    model = whisper.load_model("base", download_root=r"D:\Qube\src\models\whisper_base")
    wake_word = wake()
    command_dict = open_command()
    commands = command_dict.keys()

    Base_Dir = Path(__file__).resolve().parent.parent.parent
    log_path = Base_Dir/"src"/"data"/"given_commands"/"command.txt"

    oww_model = Model(wakeword_models=[wake_word], inference_framework="onnx")
    vad = webrtcvad.Vad(3)
    command_buffer = []
    silence_chunks = 0
    speech_detected = False
    silence_limit_chunks = int(silence_limit / (chunck_size / sample_rate))

    #overlapping oww and command problem solve
    pre_roll_sec = 0.4
    pre_roll_chunks = int(pre_roll_sec / (chunck_size / sample_rate))
    rolling_buffer = deque(maxlen=pre_roll_chunks)

    state = "listening"

    while True:
        try:
            audio = sd.rec(
                chunck_size,
                samplerate=sample_rate,
                channels=channel,
                dtype="int16"
            )
            sd.wait()

            audio_frame = audio
            audio_data = audio_frame.flatten()
            rolling_buffer.append(audio_data)
            

            if state == "listening":
                prediction = oww_model.predict(audio_data)
                if prediction[wake_word] >= 0.5:
                    voice(greeting())
                    state = "command"
                    command_buffer = list(rolling_buffer) 
                    silence_chunks = 0
                    speech_detected = False

            elif state == "command":

                prediction = oww_model.predict(audio_data)
                command_buffer.append(audio_data)
                is_speech = vad.is_speech(audio_data.tobytes(), sample_rate)

                if is_speech:
                    speech_detected = True
                    silence_chunks = 0
                else:
                    silence_chunks += 1

                if speech_detected and silence_chunks >= silence_limit_chunks:

                    full_audio = np.concatenate(command_buffer)
                    audio_flot = full_audio.astype(np.float32)/32768.0
                    audio_txt = model.transcribe(audio_flot)["text"].casefold().strip()
                    predict_command = get_close_matches(audio_txt,commands,n=1,cutoff=0.7)

                    if prediction[wake_word] >= 0.5:
                        voice(greeting_again())
                        command_buffer = list(rolling_buffer) 
                        silence_chunks = 0
                        speech_detected = False

                    else:
                        if predict_command:
                            matched_key = predict_command[0]
                            webbrowser.open(command_dict[matched_key])

                            #for model training (command store hogi)      
                            with open(log_path, "a", encoding="utf-8") as f:
                                f.write(audio_txt + "\n")

                        command_buffer = []
                        silence_chunks = 0
                        speech_detected = False

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    listen_commands()
