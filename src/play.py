from wordle import *


if __name__ == "__main__":
    print("DISCLAIMER: Does not work perfectly for answers with repeating letters yet.")

    remaining = answers

    while True:
        feedback = input("Enter feedback from wordle (Format: letter0color letter1color...):\n").split(" ")
        feedback = tuple([(letter[0], int(letter[1])) for letter in feedback])
        remaining = Turn(create_data(remaining)).get_remaining(feedback)
        print(len(remaining), remaining)
        print(get_best_word(remaining))