from wordle import Turn, create_data, GUESSES, ANSWERS, input_guess
from tqdm import tqdm

if __name__ == "__main__":
    perms = []
    for i in range(len(GUESSES)):
        for j in range(i+1, len(GUESSES)):
            perms.append((GUESSES[i], GUESSES[j]))
    print(len(perms))

    turn = Turn(create_data(ANSWERS, progress=False))
    for answer in ANSWERS:

        pbar = tqdm(total=len(perms))
        remainings = {}
        for guess in GUESSES:
            remainings[guess] = turn.get_remaining(input_guess(guess, answer))

        next_perms = []
        for w1, w2 in perms:
            pbar.update(n=1)
            intersection = remainings[w1] & remainings[w2]
            if 0 < len(intersection) < 6:
                next_perms.append((w1, w2))

        perms = next_perms
        print(f"\n#####{len(perms)}#####\n")
