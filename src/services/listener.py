import whisper
from openwakeword.model import Model
import sounddevice as sd
import numpy as np
import os
from pathlib import Path

from src.responce.wake_calls import wake
from src.responce.greet import greeting
from src.responce.commands import open_command
from services.qube_voice import voice

def listen_commands():

    sample_rate = 16000
    chunck_size = 1280
    channel = 1

    model = whisper.load_model("base")
    wake_word = wake()
    oww_model = Model(wakeword_models=[wake_word], inference_framework="onnx")
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

            greet_responce = greeting()
            audio_frame = audio
            audio_data = np.frombuffer(audio_frame, dtype=np.int16)
            prediction = oww_model.predict(audio_data)
            audio_txt = model.transcribe(audio)

            if state == "listening":
                if prediction[wake_word] >= 0.5:
                    voice(greet_responce)
                    state = "command"

            elif state == "command":
                if prediction[open_command] >= 0.5:
                    os.startfile(open_command[audio_txt])
                    state = "listening"

                    #for model training 
                    Base_Dir = Path(__file__).resolve().parent.parent.parent
                    audio_txt = Base_Dir/"src"/"data"/"given_commands"/"command.txt"
                    with open (audio_txt, "a",encoding="utf-8") as command:
                        command.write(audio_txt + "\n")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    listen_commands()