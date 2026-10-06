def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str, low: int | None = None, high: int | None = None):
    """
    Parse user input into an int guess.

    If low and high are given, guesses outside that inclusive range are rejected.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: I asked the Claude Code agent to move parse_guess here and check it for bugs;
    # it found blank input, silent decimal truncation and missing range checks.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = float(raw.strip())
    except ValueError:
        return False, None, "That is not a number."

    # Reject inf/nan and decimals like 4.9 instead of silently truncating them.
    if not value.is_integer():
        return False, None, "Enter a whole number."
    value = int(value)

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: I asked the Claude Code agent to move check_guess here and fix the high/low
    # bug; it swapped the reversed hints and found the string-comparison bug.
    # Compare as integers so a string secret can't trigger lexicographic
    # comparison (e.g. "9" > "10").
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
