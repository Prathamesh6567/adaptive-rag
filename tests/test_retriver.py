
from src.adaptive_router import route_query
from src.retriver import retrieve

# Router tests

def test_attendance_question_routes_correctly():
    assert "attendance.txt" in route_query(
        "What attendance do I need for exams?"
    )

def test_library_question_routes_correctly():
    assert "library.txt" in route_query(
        "When does the library open?"
    )

def test_unrelated_question_has_no_route():
    assert route_query(
        "Who is the principal of the college?"
    ) == []

# Semantic retrieval tests

def test_attendance_retrieval_returns_relevant_result():
    results = retrieve("What attendance do I need for exams?")

    assert results
    assert any(
        "attendance" in sentence.lower() or "75%" in sentence
        for _, _, sentence in results
    )

def test_library_retrieval_returns_relevant_result():
    results = retrieve("When does the library open?")

    assert results
    assert any(
        "library" in sentence.lower()
        or "9 AM" in sentence
        or "5 PM" in sentence
        for _, _, sentence in results
    )

# Edge-case tests

def test_empty_query_returns_no_results():
    assert retrieve("") == []

def test_unrelated_query_returns_no_results():
    assert retrieve(
        "Who is the principal of the college?"
    ) == []

def test_whitespace_query_returns_no_results():
    assert retrieve("   ") == []

# Result validation test

def test_retrieval_scores_and_sources_are_valid():
    results = retrieve("What attendance is required for exams?")

    assert results

    for score, filename, sentence in results:
        assert 0.0 <= score <= 1.0
        assert filename in ("attendance.txt", "library.txt")
        assert sentence.strip()