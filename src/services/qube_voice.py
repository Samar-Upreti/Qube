import pyttsx3 as speek

engine = speek.init()

def voice(message):

    engine.say(message)
    engine.runAndWait()