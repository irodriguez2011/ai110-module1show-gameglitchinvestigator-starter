import random
import streamlit as st

# FIX: I asked the Claude Code agent to move check_guess and parse_guess into
# logic_utils.py; it did the refactor and updated this import.
from logic_utils import check_guess, parse_guess


def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Claude Code agent changed Hard from 1-50 to 1-200 so it has the biggest
        # range; I questioned it, since 5 attempts already make Hard the hardest.
        return 1, 200
    return 1, 100


def update_score(current_score: int, outcome: str, attempt_number: int):
    # FIX: Claude Code agent found the scoring bugs (off-by-one win points, "Too High"
    # adding +5 on even attempts) while checking the app against the README for me.
    if outcome == "Win":
        # First-try win is worth 100, minus 10 for each extra attempt.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


# FIX: Claude Code agent added this so New Game resets status, score and history
# and picks a secret in the difficulty's range; I asked it to explain how it works.
def start_new_game(low: int, high: int, difficulty: str):
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Claude Code agent found that changing difficulty kept the old secret (e.g. 87
# on Easy) and replaced the separate session_state checks with this.
# Start a fresh game on first load, or when the difficulty (and so the range) changes.
if st.session_state.get("difficulty") != difficulty:
    start_new_game(low, high, difficulty)

st.subheader("Make a guess")

# FIX: Claude Code agent found "Attempts left" lagged one guess behind and fixed it
# with placeholders; I asked it to walk me through how st.empty() works.
# Placeholders are filled in by render_status() after the guess is processed,
# so they never show the previous attempt's numbers.
info_box = st.empty()
debug_box = st.empty()


def render_status():
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_box.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


# FIX: I found this bug while playing; the Claude Code agent explained the cause
# and moved the input into st.form.
# FIXME: Pressing Enter didn't submit the guess, even though the box said "Press Enter to apply".
with st.form("guess_form"):
    raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Claude Code agent replaced the old reset here (attempts=0, secret from 1-100,
# status never reset) with start_new_game().
if new_game:
    start_new_game(low, high, difficulty)
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_status()
    st.stop()

if submit:
    # FIX: Claude Code agent added range checking by passing low/high to parse_guess.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: Claude Code agent moved the attempt counter so typos don't use an attempt.
        # Invalid input doesn't cost an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Claude Code agent removed the code that turned the secret into a string
        # on even attempts, which flipped the hints (the "commitment issues" bug).
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
