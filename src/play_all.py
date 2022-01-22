import json
import multiprocessing as mp
import random

from tqdm import tqdm

from wordle import Turn, create_data, get_best_word, ANSWERS, input_guess


def play(answer, progress=False, best_word="roate"):
    guess_count = 0
    remaining = ANSWERS
    while best_word != answer and len(remaining) > 1:
        if guess_count == 6:
            return -1
        feedback = input_guess(best_word, answer)
        remaining = Turn(create_data(remaining, progress=progress)).get_remaining(feedback)
        # print(len(remaining), remaining)
        best_word = get_best_word(remaining, progress=progress)
        guess_count += 1
    # print(f"Solved {answer} in {guess_count + 1} guesses")
    return answer, guess_count + 1

# k = 100
# games = random.sample(ANSWERS, k=k)


games = ANSWERS
pbar = tqdm(total=len(games))
results = []
guess_count = {}


def add(result):
    results.append(result[1])
    guess_count[result[0]] = result[1]
    pbar.update(n=1)


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count() - 2)
    for i, answer in enumerate(games):
        pool.apply_async(play, args=(answer, False, "המיות"), callback=add)
        # guess_count = play(answer)
        # results[answer] = guess_count
        # print(f"After {i+1} turns, the average is {sum(results.values())/(i+1)}")
    # for word, guess_count in results.items():
    #     if guess_count == -1:
    #         print(f"Failed to guess {word}")
    # print(f"Results: {sum(results.values())}")
    pool.close()
    pool.join()
    with open("results.json", "w") as f:
        json.dump(guess_count, f, indent=4, ensure_ascii=False)
    print(sum(results)/len(results))
