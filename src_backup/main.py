from src.adaptive_router import route_query
from src.retriver import retrieve
from src.generator import generate_answer


def main():

    print("\n======================================")
    print("     ADAPTIVE RAG COLLEGE ASSISTANT")
    print("======================================")
    print("Powered by Ollama - Llama 3.2:3B")
    print("Type 'exit' to quit.")

    while True:

        query = input("\nYou: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a question.")
            continue

        selected_files = route_query(query)

        if not selected_files:
            print("No matching college document found.")
            continue

        print("\nSelected documents:", selected_files)
        print("Searching relevant information...")

        results = retrieve(query)

        if not results:
            print("No sufficiently relevant information found.")
            continue

        print("Generating answer using Ollama...")

        try:
            answer = generate_answer(query, results)

            print("\n========== ANSWER ==========")
            print(answer)

            print("\n========== SOURCES ==========")

            for filename in selected_files:
                print("-", filename)

            print("\n========== EVIDENCE ==========")

            for score, filename, sentence in results:
                print(f"\nSource: {filename}")
                print(f"Similarity: {score:.3f}")
                print(f"Content: {sentence}")

        except Exception as error:
            print("Answer generation failed:", error)


if __name__ == "__main__":
    main()