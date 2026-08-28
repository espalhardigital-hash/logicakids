"""Shared progression rules for student practice levels."""

PRACTICE_REQUIRED_CORRECT_ANSWERS = 10


def calculate_progress_percentage(correct_answers: int, required_answers: int) -> int:
    """Return a bounded integer percentage derived from the visible counter."""
    if required_answers <= 0:
        return 0
    bounded_correct = max(0, correct_answers)
    return min(100, int((bounded_correct / required_answers) * 100))


def practice_is_complete(
    correct_answers: int,
    required_answers: int = PRACTICE_REQUIRED_CORRECT_ANSWERS,
) -> bool:
    """Return whether a practice level reached its configured correct-answer goal."""
    return required_answers > 0 and correct_answers >= required_answers
