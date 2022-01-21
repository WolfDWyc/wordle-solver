# wordle-solver

Utilities for solving wordle puzzles and finding charecteristics of the puzzle and the words used in it. Supports multiple languages.

# Running

- Clone the repository to your local machine, and install the dependencies:

```bash
git clone https://github.com/WolfDWyc/wordle-solver.git
cd wordle-solver
pip install -r requirements.txt
```

- Choose a language by changing the `LANGUAGE` variable in `./src/wordle.py` file (Will be moved to a configuraiton file in the future, and maybe as a parameter that can be changed at runtime).

- Run your perferred script (Example: `python ./src/play.py`)

# Contributing and developing 

## Adding scenarios

Simply create a new file in `./src` and import what you need from the main `./src/wordle.py` file: 
```python
# Probably all you'll need:
from wordle import get_best_word, input_guess, create_data, Turn, answers, guesses
# Less recommended:
from wordle import *
```

## Editing wordle.py 

When editing the main `./src/wordle.py` file, open a new branch and make your changes there. To merge your changes into the master branch, open a pull request and wait for approval first.

# Disclaimer

`./src/play.py` does not work perfectly for answers with repeating letters yet.

# Sources
- English: https://www.powerlanguage.co.uk/wordle/
- Hebrew: https://meduyeket.net/