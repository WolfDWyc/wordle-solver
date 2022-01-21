from wordle import *

if __name__ == "__main__":
    perms = []
    for i in range(len(guesses)):
        for j in range(i+1, len(guesses)):
            perms.append((guesses[i], guesses[j]))
    print(len(perms))

    turn = Turn(create_data(answers, progress=False))
    for answer in answers:

        pbar = tqdm(total=len(perms))
        remainings = {}
        for guess in guesses:
            remainings[guess] = turn.get_remaining(input_guess(guess, answer))

        next_perms = []
        for w1, w2 in perms:
            pbar.update(n=1)
            intersection = remainings[w1] & remainings[w2]
            if 0 < len(intersection) < 6:
                next_perms.append((w1, w2))

        perms = next_perms
        print(f"\n#####{len(perms)}#####\n")
