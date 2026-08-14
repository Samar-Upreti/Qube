import random as ra
def greeting():
    greet_word = [
        "Hello, how may I help you?",
        "Hello, sir.",
        "Yes, sir?",
        "How may I assist you?",
        "At your service.",
        "I'm listening.",
        "I'm listening, sir.",
        "Ready when you are.",
        "Yes, I'm here.",
        "How can I help?",
        "What can I do for you?",
        "Awaiting your command.",
        "I'm ready.",
        "Go ahead.",
        "Yes?",
        "Hmm, I'm listening.",
        "Right away.",
        "Certainly.",
        "Of course.",
        "As you wish."
    ]
    return ra.choice(greet_word)

def greeting_again():
    greet_word = [
        "I told you, I'm listening.",
        "Yes, I'm still listening.",
        "I'm listening, you can speak.",
        "I'm right here.",
        "You already have my attention.",
        "I'm waiting for your command.",
        "Yes, I heard you.",
        "I'm ready, go ahead.",
        "I'm still here.",
        "I am listening, sir.",
        "You have my attention.",
        "Go ahead, I'm listening.",
        "I'm waiting.",
        "I heard the wake word.",
        "Yes? What do you need?",
        "I'm already listening.",
        "No need to call me again, I'm listening.",
        "I'm awake. What's your command?",
        "You called me, I'm here.",
        "I'm listening. Please continue."
    ]
    return ra.choice(greet_word)
