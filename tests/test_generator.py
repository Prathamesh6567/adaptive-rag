from types import SimpleNamespace
from unittest.mock import patch

from src.generator import generate_answer


def test_empty_query():

    result = generate_answer("", [])

    assert "valid question" in result.lower()


def test_no_retrieved_context():

    result = generate_answer(
        "What is the attendance requirement?",
        []
    )

    assert "couldn't find enough" in result.lower()


@patch("src.generator.chat")
def test_successful_answer_generation(mock_chat):

    mock_chat.return_value = SimpleNamespace(
        message=SimpleNamespace(
            content="Students need at least 75% attendance."
        )
    )

    results = [
        (
            0.82,
            "attendance.txt",
            "Students must maintain at least 75% attendance."
        )
    ]

    answer = generate_answer(
        "What attendance is required?",
        results
    )

    assert "75%" in answer

    mock_chat.assert_called_once()


@patch("src.generator.chat")
def test_empty_model_response(mock_chat):

    mock_chat.return_value = SimpleNamespace(
        message=SimpleNamespace(content=" ")
    )

    results = [
        (
            0.80,
            "library.txt",
            "The library is open from 9 AM to 5 PM."
        )
    ]

    answer = generate_answer(
        "When does the library open?",
        results
    )

    assert "empty response" in answer.lower()