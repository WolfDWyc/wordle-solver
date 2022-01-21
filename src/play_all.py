import multiprocessing as mp
import random

from wordle import *


def play(answer, progress=False, best_word="roate"):
    guess_count = 0
    remaining = answers
    while best_word != answer and len(remaining) > 1:
        if guess_count == 6:
            return -1
        feedback = input_guess(best_word, answer)
        remaining = Turn(create_data(remaining, progress=progress)).get_remaining(feedback)
        # print(len(remaining), remaining)
        best_word = get_best_word(remaining, progress=progress)
        guess_count += 1
    # print(f"Solved {answer} in {guess_count + 1} guesses")
    return guess_count + 1

results = []
def add(result):
    results.append(result)
    
    print(f"Finished {len(results)} games, with a total of {sum(results)} guesses and an average of {sum(results)/len(results)}")

if __name__ == '__main__':
    # games = ["favor"]
    k = 100
    games = random.sample(answers, k=k)


    pool = mp.Pool(mp.cpu_count())
    for i, answer in enumerate(games):
        pool.apply_async(play, args=(answer,False, "soare"), callback=add)
        # guess_count = play(answer)
        # results[answer] = guess_count
        # print(f"After {i+1} turns, the average is {sum(results.values())/(i+1)}")

    # for word, guess_count in results.items():
    #     if guess_count == -1:
    #         print(f"Failed to guess {word}")
    # print(f"Results: {sum(results.values())}")
    pool.close()
    pool.join()

    print(results)
