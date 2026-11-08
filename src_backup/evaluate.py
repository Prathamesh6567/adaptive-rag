from src.adaptive_router import route_query
from src.retriver import retrieve
from src.generator import generate_answer


SUPPORTED_TESTS = [
    {
        "question": "What is the minimum attendance required?",
        "expected": ["75%"]
    },
    {
        "question": "How many books can students borrow?",
        "expected": ["3"]
    },
    {
        "question": "How long can students keep borrowed books?",
        "expected": ["14 days"]
    },
    {
        "question": "When is the college library open?",
        "expected": ["9 AM", "5 PM"]
    }
]

UNSUPPORTED_TESTS = [
    "Who is the college principal?",
    "What is the college canteen timing?",
    "What is the college examination fee?"
]


def run_evaluation():

    passed = 0
    failed = 0

    print("\n========== SUPPORTED QUESTION TESTS ==========")

    for index, test in enumerate(SUPPORTED_TESTS, start=1):

        question = test["question"]
        expected = test["expected"]

        print(f"\nTest {index}: {question}")

        selected_files = route_query(question)

        if not selected_files:
            print("FAILED: No document selected.")
            failed += 1
            continue

        results = retrieve(question)

        if not results:
            print("FAILED: No relevant information retrieved.")
            failed += 1
            continue

        answer = generate_answer(question, results)

        print("Answer:", answer)

        if all(word.lower() in answer.lower() for word in expected):
            print("RESULT: PASSED")
            passed += 1
        else:
            print("RESULT: NEEDS REVIEW")
            failed += 1

    print("\n========== UNSUPPORTED QUESTION TESTS ==========")

    for index, question in enumerate(UNSUPPORTED_TESTS, start=1):

        print(f"\nUnsupported Test {index}: {question}")

        selected_files = route_query(question)

        if not selected_files:
            print("Answer: No matching college document found.")
            print("RESULT: PASSED - No unsupported answer generated.")
            passed += 1
        else:
            print("RESULT: NEEDS REVIEW - A document was selected.")
            failed += 1

    total = len(SUPPORTED_TESTS) + len(UNSUPPORTED_TESTS)

    print("\n========== FINAL EVALUATION REPORT ==========")
    print("Total tests:", total)
    print("Passed:", passed)
    print("Failed / Needs review:", failed)

    if failed == 0:
        print("Overall Result: ALL TESTS PASSED!")
    else:
        print("Overall Result: SOME TESTS NEED REVIEW.")


if __name__ == "__main__":
    run_evaluation()
