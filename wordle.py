from datetime import datetime
import random

def word_picker() -> str:
    word_list = []
    with open("word_list.txt", "r") as words:
        for line in words:
            line = line[:-1]
            word_list.append(line)
    current_time = int(datetime.now().strftime("%d%m%Y"))
    random.seed(current_time)

    return random.choice(word_list)

def word_checker(word: str, guess: str):
    # Checking for bad inputs

    if len(word) != 5 or len(guess) != 5:
        return "Invalid Guess!"

    # + represents correct letter, correct position
    # - represents correct letter, wrong position
    # x represents wrong letter
    base = ["x", "x", "x", "x", "x"]
    word_extras = []
    guess_extras = []
    #First check for any +
    for i in range(0, 5):
        if word[i] == guess[i]:
            base[i] = "+"
        #elif guess[i] in word:
        #    base[i] = "-"
        else:
            word_extras.append(word[i])
            guess_extras.append((i, guess[i]))
    for idx, extra in guess_extras:
        if extra in word_extras:
            base[idx] = "-"
            word_extras.remove(extra)
    return "".join(base)

def make_wordfile():
    word_list = []
    with open("words.txt", "r") as words:
        for line in words:
            line = line[:-1]
            if len(line) == 5 and line.isalpha():
                word_list.append(line)
    output = open("word_list.txt", "w")
    for word in word_list:
        output.write(word + "\n")
    output.close()


if __name__ == "__main__":
    result = "xxxxx"
    while result != "+++++":
        wotd = word_picker().lower()
        # print(wotd)
        guess = input("Guess: ")
        result = word_checker(wotd, guess)
        print(result)