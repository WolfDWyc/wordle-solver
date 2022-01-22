import functools
import json
from collections import defaultdict

from tqdm import tqdm

LANGUAGE = "hebrew"
ASSETS_DIR = f"assets\\{LANGUAGE}"

ANSWERS = [answer.strip() for answer in
             open(f"{ASSETS_DIR}\\answers.txt", encoding="utf-8").readlines()]
ANSWERS.sort()

GUESSES = list(set(ANSWERS + [guess.strip() for guess in
             open(f"{ASSETS_DIR}\\guesses.txt", encoding="utf-8").readlines()]))
GUESSES.sort()

LETTERS = [letter.strip() for letter in open(f"{ASSETS_DIR}\\letters.txt", encoding="utf-8").readlines()]
LETTERS.sort()

def input_guess(guess, answer):
    colors = []
    for i in range(len(answer)):
        if guess[i] not in answer:
            colors.append((guess[i], 0))
        elif guess[i] == answer[i]:
            colors.append((guess[i], 2))
        else:
            colors.append((guess[i], 1))
    return tuple(colors)


class Turn:
    def __init__(self, data):
        self.data = data

    # Old get remaining, replaced by intersection + new get remaining
    # def get_remaining(self, output):
    #     sets = []
    #     for i in range(5):
    #         sets.append(self.data[output[i][0]][i][output[i][1]])
    #     return set.intersection(*sets)


    # Explanation:
    # The purpose of get_remaining is:
    # 1. For each of the 5 feedbacks (one per index), get the 5 sets that have the remaining words
    # 2. Intersect the 5 sets
    # The new method caches intersections to avoid recalculating them
    # Caching immutable set objects is problematic, so we cache the letter, index and score (0/1/2) of each set instead
    # Then, we make a cached intersection between 0 and 1, 2 and 3, and a regular intersection between (0,1,2,3) and 4
    # TODO: Make the new method work for all lengths of words

    @functools.lru_cache(maxsize=100000)
    def intersection(self, l1, i1, s1, l2, i2, s2):
        first_set = self.data[l1][i1][s1]
        second_set = self.data[l2][i2][s2]
        return first_set.intersection(second_set)

    @functools.lru_cache(maxsize=150000)
    def get_remaining(self, output):
        inter01 = self.intersection(output[0][0], 0, output[0][1], output[1][0], 1, output[1][1])
        inter23 = self.intersection(output[2][0], 2, output[2][1], output[3][0], 3, output[3][1])
        return inter01.intersection(inter23).intersection(self.data[output[4][0]][4][output[4][1]])

    @functools.lru_cache(maxsize=150000)
    def count_remaining(self, output):
        return len(self.get_remaining(output))


def create_data(remaining, progress=True):
    master = defaultdict(dict)
    if progress: pbar = tqdm(total=len(LETTERS))
    for letter in LETTERS:
        if progress: pbar.update(n=1)
        for position in range(5):
            master[letter][position] = defaultdict(dict)
            for color in range(3):
                master[letter][position][color] = set()
                for answer in remaining:
                    if color == 0:
                        if letter not in answer:
                            master[letter][position][color].add(answer)
                    elif color == 1:
                        if letter in answer and answer[position] != letter:
                            master[letter][position][color].add(answer)
                    else:
                        if answer[position] == letter:
                            master[letter][position][color].add(answer)
    return master

def get_best_word(remaining, save_scores=True, save_data=True, progress=True):
    data = create_data(remaining, progress=progress)
    turn = Turn(data)

    if save_data:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(turn.data, f, indent=4, ensure_ascii=False, default=list)
    if progress: pbar = tqdm(total=len(GUESSES))
    
    scores = {}
    for guess in GUESSES:
        if progress: pbar.update(n=1)
        score = 0
        for answer in remaining:
            output = input_guess(guess, answer)
            score += turn.count_remaining(output)
        scores[guess] = score/len(remaining)
        # print(turn.intersection.cache_info())

    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    min_score = list(scores.values())[0]
    best_word = list(scores.keys())[0]
    for word, score in scores.items():
        if score == min_score and word in remaining:
            best_word = word
            break
    if save_scores:
        with open("scores.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=4, ensure_ascii=False)
    return best_word

# print(get_best_word(answers))
# remaining = Turn(create_data(answers)).get_remaining((("c", 2), ("o", 2), ("m", 0), ("e", 0), ("t", 0)))
# print(len(remaining), remaining)
# print(get_best_word(remaining))


if __name__ == '__main__':
    print(get_best_word(ANSWERS))
