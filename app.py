from flask import Flask, render_template, request, flash
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

app = Flask(__name__)
app.secret_key = "987654321"
app.str_to_print = ""
app.guesses = ""
app.num_guesses = 0

@app.route("/")
def index():
    flash("Hey sexy ;)")
    return render_template("index.html")

@app.route("/word", methods=["POST", "GET"])
def test():
    # result = "xxxxx"
    # if result != "+++++":
    if app.num_guesses < 5:
        wotd = word_picker().lower()
        # print(wotd)
        guess = str(request.form['guess'])
        
        app.guesses += f"{guess}\n"
        flash(app.guesses)

        result = word_checker(wotd, guess)
        app.str_to_print += f"{result}\n"
        # print(result)
        flash(app.str_to_print)
        if result != "Invalid Guess!":
            app.num_guesses += 1
        return render_template("index.html")
    else:
        wotd = word_picker().lower()
        flash(wotd)
        return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)
