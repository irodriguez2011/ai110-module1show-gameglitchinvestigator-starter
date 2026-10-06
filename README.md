# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game's purpose

This is a number guessing game built with Streamlit. The game picks a secret number, and you try to guess it in a limited number of attempts. After each guess it tells you to go higher or lower. Easy is 1–20 with 6 attempts, Normal is 1–100 with 8 attempts, and Hard is 1–200 with 5 attempts. You lose 5 points for each wrong guess, and a win is worth 100 points minus 10 for each extra attempt.

### Bugs I found

- **The hints were backwards.** Guessing too high told you to "Go HIGHER!" and guessing too low told you to "Go LOWER!"
- **The secret number had "commitment issues."** On every other attempt, the app turned the secret into a string, so Python compared the numbers lexicographically, like words. For example, "9" > "10" is True because it only looks at the first character, so the hints flipped.
- **New Game didn't really start a new game.** After you won or lost, it kept saying "You already won," it picked the secret from 1–100 no matter the difficulty, and it didn't reset the score or history.
- **Changing difficulty kept the old secret.** You could switch to Easy (1–20) and still have a secret like 87 that you could never guess.
- **The attempt counter was wrong.** Attempts started at 1 instead of 0, "Attempts left" was always one guess behind, and typing something that wasn't a number still used up an attempt.
- **The prompt always said "between 1 and 100,"** even on Easy and Hard.
- **Scoring was inconsistent.** A "Too High" guess sometimes added 5 points, and the win points were off by one.
- **Bad input wasn't handled well.** Blank spaces said "That is not a number," decimals like 4.9 were quietly cut down to 4, and guesses outside the range were accepted.
- **Pressing Enter didn't submit the guess,** even though the box said "Press Enter to apply." You had to click Submit Guess.

### Fixes I applied

- Moved `check_guess` and `parse_guess` from `app.py` into `logic_utils.py`.
- Fixed `check_guess` so the hints point the right way, and it converts both values to integers before comparing them.
- Removed the code that turned the secret into a string.
- Fixed `parse_guess` so it rejects blank input, decimals, and guesses outside the difficulty's range.
- Added a `start_new_game()` function that resets the secret, attempts, score, status and history. It runs when you click New Game or change the difficulty.
- Made attempts start at 0, made typos not use an attempt, and made "Attempts left" update right after each guess.
- Made the prompt show the real range for the difficulty.
- Made every wrong guess cost 5 points, and a first-try win worth 100.
- Put the guess box and Submit button in a form so pressing Enter submits the guess.
- Added tests for each fix in `tests/test_game_logic.py`.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. **Start the app.** Run `python -m streamlit run app.py` inside the `.venv`. The game opens in the browser on Normal difficulty. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8", and the blue box says "Guess a number between 1 and 100. Attempts left: 8." In this game, the Developer Debug Info shows the secret is **37**.
2. **Try a bad guess.** I type `abc` and press Enter. The app says "That is not a number." and "Attempts left" stays at 8, so a typo doesn't cost an attempt.
3. **Try an out-of-range guess.** I type `150` and press Enter. The app says "Guess must be between 1 and 100." and "Attempts left" is still 8.
4. **First real guess.** I guess `50`. The hint says "📉 Go LOWER!" because 50 is higher than 37. "Attempts left" drops to 7 and the score is -5.
5. **Second guess.** I guess `25`. The hint says "📈 Go HIGHER!" because 25 is lower than 37. "Attempts left" is 6, the score is -10, and the history in the debug panel shows `[50, 25]`.
6. **Winning guess.** I guess `37`. The hint says "🎉 Correct!", balloons pop up, and the app says "You won! The secret was 37. Final score: 70." (-10 from the two wrong guesses, plus 80 for winning on the third attempt.)
7. **Start a new game.** I click New Game 🔁. The game resets with a new secret, "Attempts left: 8", a score of 0, and an empty history, so I can play again.
8. **Change the difficulty.** I pick Easy in the sidebar. A new game starts right away, and the box says "Guess a number between 1 and 20. Attempts left: 6."

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
plugins: anyio-4.15.1
collecting ... collected 24 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  4%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  8%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 12%]
tests/test_game_logic.py::test_string_secret_compares_as_number PASSED   [ 16%]
tests/test_game_logic.py::test_parse_valid_guess PASSED                  [ 20%]
tests/test_game_logic.py::test_parse_empty_guess PASSED                  [ 25%]
tests/test_game_logic.py::test_parse_not_a_number PASSED                 [ 29%]
tests/test_game_logic.py::test_parse_rejects_decimal_and_non_finite PASSED [ 33%]
tests/test_game_logic.py::test_parse_out_of_range PASSED                 [ 37%]
tests/test_game_logic.py::test_attempts_start_at_zero PASSED             [ 41%]
tests/test_game_logic.py::test_attempts_left_updates_after_guess PASSED  [ 45%]
tests/test_game_logic.py::test_invalid_input_does_not_use_an_attempt PASSED [ 50%]
tests/test_game_logic.py::test_out_of_range_guess_is_rejected PASSED     [ 54%]
tests/test_game_logic.py::test_secret_stays_the_same_across_guesses PASSED [ 58%]
tests/test_game_logic.py::test_hint_correct_on_every_attempt PASSED      [ 62%]
tests/test_game_logic.py::test_can_win PASSED                            [ 66%]
tests/test_game_logic.py::test_first_try_win_scores_100 PASSED           [ 70%]
tests/test_game_logic.py::test_wrong_guesses_always_lose_5 PASSED        [ 75%]
tests/test_game_logic.py::test_lose_after_attempt_limit PASSED           [ 79%]
tests/test_game_logic.py::test_new_game_after_win_lets_you_play_again PASSED [ 83%]
tests/test_game_logic.py::test_new_game_secret_uses_difficulty_range PASSED [ 87%]
tests/test_game_logic.py::test_changing_difficulty_starts_new_game_in_range PASSED [ 91%]
tests/test_game_logic.py::test_prompt_shows_difficulty_range PASSED      [ 95%]
tests/test_game_logic.py::test_enter_submits_guess PASSED                [100%]

============================== 24 passed in 1.12s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
