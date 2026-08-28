import pytest

from app.core.progression import (
    PRACTICE_REQUIRED_CORRECT_ANSWERS,
    calculate_progress_percentage,
    practice_is_complete,
)


def test_practice_goal_is_ten_correct_answers() -> None:
    assert PRACTICE_REQUIRED_CORRECT_ANSWERS == 10


@pytest.mark.parametrize(
    ("correct_answers", "expected_percentage", "expected_complete"),
    [
        (0, 0, False),
        (9, 90, False),
        (10, 100, True),
        (11, 100, True),
    ],
)
def test_visible_counter_and_completion_share_the_same_source(
    correct_answers: int,
    expected_percentage: int,
    expected_complete: bool,
) -> None:
    assert (
        calculate_progress_percentage(
            correct_answers,
            PRACTICE_REQUIRED_CORRECT_ANSWERS,
        )
        == expected_percentage
    )
    assert practice_is_complete(correct_answers) is expected_complete


def test_invalid_requirement_fails_closed() -> None:
    assert calculate_progress_percentage(10, 0) == 0
    assert practice_is_complete(10, 0) is False
