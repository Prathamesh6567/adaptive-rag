
from src.adaptive_router import route_query

def test_attendance_question():
    assert route_query("What is the minimum attendance required?") == [
        "attendance.txt"
    ]

def test_library_question():
    assert route_query("How many books can I borrow?") == [
        "library.txt"
    ]

def test_mixed_question():
    result = route_query("Can I borrow books if attendance is low?")

    assert "attendance.txt" in result
    assert "library.txt" in result

def test_unrelated_question():
    assert route_query("Who is the principal of the college?") == []