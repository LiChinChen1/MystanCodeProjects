"""
File: hangman.py
Name: Chin
-----------------------------
This program plays hangman game.
Users sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'   # Turn lower case to be upper case.

import random

N_TURNS = 7                                     # This constant controls the number of guess the player has.


def main():
    """
    This program plays hangman game.
    1. Program will show a dashed word, and ask player to input one character each round.
    2. If the player input is correct, show the updated word on console.
    3. Players have N_TURNs chances to try and win this game
    4. No matter win or lose, program will show the answer.
    """

    answer = random_word()
    dashed = answer_dash(answer)
    t_dashed = answer_dash(answer)
    n_dashed = ""
    n_turns = N_TURNS

    print(answer)

    while True:

        print("The word looks like " + dashed)
        print("You have " + str(n_turns) + " wrong guesses left.")

        while True:
            guess = str(input("Your guess: "))                  # Input format control.

            if guess.isalpha() and len(guess) == 1:
                break

            print("Illegal format.")
            print("")

        if guess.islower():                                     # Turn lower case to be upper case.
            guess = ALPHABET[lower_ALPHABET.find(guess)]

        for j in range(len(answer)):
            if guess == answer[j]:
                n_dashed += answer[j]                           # To show "the word looks like"
                t_dashed += answer[j]                           # To judge the guesses is true or false.
            else:
                n_dashed += dashed[j]
                t_dashed += "-"

        if t_dashed == answer_dash(answer):
            print("There is no " + guess + "'s in the word.")
            n_turns = n_turns - 1
        else:
            print("You are correct!")

        dashed = n_dashed
        t_dashed = ""
        n_dashed = ""
        print("")

        if answer == dashed:
            print("You win!!")
            print("The word was: " + answer)
            break

        elif n_turns == 0:
            print("You are completely hung :( ")
            print("The word was: " + answer)
            break


def random_word():
    """
    To random choice of the answer.
    """
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


def answer_dash(answer):
    """
    Create a line of "-" , and the lens is as long as the answer.
    """
    dash = ""
    for i in range(len(answer)):
        dash += "-"
    return dash


# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == '__main__':
    main()
