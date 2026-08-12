import random as ra
def greeting():
    greet_word = [
        "Hello How May I Help You",
        "Hii Dear",
        "Hmm",
        "i am listining"
    ]
    word = ra.choice(greet_word)
    return word