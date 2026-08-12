import pyttsx3 as speek

engine = speek.init()

def qube_voice(message):

    engine.say(message)
    engine.runAndWait()