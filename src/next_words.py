from wordle import *

if __name__ == "__main__":

    first_turn = Turn(create_data(ANSWERS, progress=False))
    remainings = {}
    for answer in ANSWERS:
        feedback_0 = input_guess("roate", answer)
        feedback_1 = input_guess("linds", answer)
        feedback = (*feedback_0, *feedback_1)
        if feedback not in remainings:
            remaining = first_turn.get_remaining(feedback_0) & first_turn.get_remaining(feedback_1)
            remainings[feedback] = {"remaining": remaining, "count": 1}
        else:
            remainings[feedback]["count"] += 1


    avg_scores = defaultdict(lambda: 0)
    for remaining in tqdm(remainings.values()):
        best_word = get_best_word(remaining["remaining"], progress=False, save_scores=True)
        # TODO: Just return all of the scores instead of just the best one, so we don't need to read the scores.json file
        with open("scores.json", "r", encoding="utf-8") as file:
            scores = json.load(file)
        for word, score in scores.items():
            avg_scores[word] += score * remaining["count"]

    avg_scores = {k: v/len(ANSWERS) for k, v in sorted(avg_scores.items(), key=lambda item: item[1])}
    with open("avg_scores.json", "w", encoding="utf-8") as file:
        json.dump(avg_scores, file, indent=4, ensure_ascii=False)

