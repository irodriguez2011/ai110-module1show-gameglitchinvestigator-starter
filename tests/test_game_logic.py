from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, parse_guess

APP_PATH = str(Path(__file__).parent.parent / "app.py")

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_string_secret_compares_as_number():
    # "9" > "10" as strings, but 9 < 10 as numbers
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low"

def test_parse_valid_guess():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("  42  ") == (True, 42, None)
    assert parse_guess("42.0") == (True, 42, None)

def test_parse_empty_guess():
    assert parse_guess("")[0] is False
    assert parse_guess("   ")[0] is False
    assert parse_guess(None)[0] is False

def test_parse_not_a_number():
    ok, value, err = parse_guess("abc")
    assert not ok and value is None and err == "That is not a number."

def test_parse_rejects_decimal_and_non_finite():
    assert parse_guess("4.9")[0] is False
    assert parse_guess("inf")[0] is False
    assert parse_guess("nan")[0] is False

def test_parse_out_of_range():
    ok, _, err = parse_guess("101", 1, 100)
    assert not ok and "between 1 and 100" in err
    assert parse_guess("100", 1, 100) == (True, 100, None)


# --- App tests: run app.py headlessly and drive it like a player would ---

def start_app(secret=50):
    """Load the app on Normal (1-100) with a known secret."""
    at = AppTest.from_file(APP_PATH).run()
    at.session_state.secret = secret
    return at

def submit(at, guess):
    at.text_input[0].input(str(guess))
    at.button[0].click().run()

def click_new_game(at):
    at.button[1].click().run()

def test_attempts_start_at_zero():
    at = start_app()
    assert at.session_state.attempts == 0
    assert "Attempts left: 8" in at.info[0].value

def test_attempts_left_updates_after_guess():
    # The info box used to lag one guess behind
    at = start_app()
    submit(at, 10)
    assert "Attempts left: 7" in at.info[0].value

def test_invalid_input_does_not_use_an_attempt():
    at = start_app()
    submit(at, "abc")
    assert at.session_state.attempts == 0
    assert at.session_state.history == []
    assert at.error[0].value == "That is not a number."

def test_out_of_range_guess_is_rejected():
    at = start_app()
    submit(at, 500)
    assert at.session_state.attempts == 0
    assert "between 1 and 100" in at.error[0].value

def test_secret_stays_the_same_across_guesses():
    at = start_app(secret=50)
    for guess in (10, 20, 30):
        submit(at, guess)
        assert at.session_state.secret == 50

def test_hint_correct_on_every_attempt():
    # The secret used to become a string on even attempts, flipping the hint
    at = start_app(secret=50)
    for _ in range(4):
        submit(at, 9)
        assert at.warning[0].value.endswith("Go HIGHER!")

def test_can_win():
    at = start_app(secret=50)
    submit(at, 50)
    assert at.session_state.status == "won"
    assert "You won!" in at.success[0].value

def test_first_try_win_scores_100():
    at = start_app(secret=50)
    submit(at, 50)
    assert at.session_state.score == 100

def test_wrong_guesses_always_lose_5():
    # "Too High" used to add 5 points on even attempts
    at = start_app(secret=50)
    submit(at, 60)
    submit(at, 70)
    assert at.session_state.score == -10

def test_lose_after_attempt_limit():
    at = start_app(secret=50)
    for _ in range(8):
        submit(at, 1)
    assert at.session_state.status == "lost"
    assert "Out of attempts!" in at.error[0].value

def test_new_game_after_win_lets_you_play_again():
    # New Game used to leave status as "won", locking the game
    at = start_app(secret=50)
    submit(at, 50)
    click_new_game(at)
    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 0
    assert at.session_state.score == 0
    assert at.session_state.history == []

def test_new_game_secret_uses_difficulty_range():
    # New Game used to pick from 1-100 regardless of difficulty
    at = start_app()
    at.sidebar.selectbox[0].select("Easy").run()
    for _ in range(20):
        click_new_game(at)
        assert 1 <= at.session_state.secret <= 20

def test_changing_difficulty_starts_new_game_in_range():
    at = start_app(secret=87)
    submit(at, 10)
    at.sidebar.selectbox[0].select("Easy").run()
    assert 1 <= at.session_state.secret <= 20
    assert at.session_state.attempts == 0

def test_prompt_shows_difficulty_range():
    # The prompt used to always say "between 1 and 100"
    at = start_app()
    at.sidebar.selectbox[0].select("Easy").run()
    assert "between 1 and 20" in at.info[0].value
