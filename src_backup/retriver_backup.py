from pathlib import Path
import re
import math

from adaptive_router import route_query

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "if", "has",
    "have", "does", "do", "how", "can", "to", "of",
    "in", "on", "for", "and", "or", "my", "i", "me",
    "please", "tell", "about", "much", "many", "at",
    "time", "minimum", "required", "college", "student",
    "students"
}


def tokenize(text):
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def select_documents(query):
    return route_query(query)


def load_sentences(filenames):
    documents = []

    for filename in filenames:
        path = DATA_DIR / filename

        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")

        for sentence in re.split(r"(?<=[.!?])\s+|\n+", content):
            sentence = sentence.strip()

            if sentence:
                documents.append((filename, sentence))

    return documents


def similarity(query, sentence):
    query_words = tokenize(query)
    sentence_words = tokenize(sentence)

    if not query_words or not sentence_words:
        return 0.0

    overlap = query_words & sentence_words

    if not overlap:
        return 0.0

    return len(overlap) / math.sqrt(
        len(query_words) * len(sentence_words)
    )


def retrieve(query, top_k=3):
    filenames = select_documents(query)

    if not filenames:
        return []

    documents = load_sentences(filenames)
    results = []

    for filename, sentence in documents:
        score = similarity(query, sentence)

        if score > 0:
            results.append((score, filename, sentence))

    results.sort(key=lambda result: result[0], reverse=True)

    return results[:top_k]


def main():
    print("Adaptive RAG Retriever")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nAsk a question: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            print("Please enter a question.")
            continue

        filenames = select_documents(query)

        if not filenames:
            print("No matching found.")
            continue

        results = retrieve(query)

        if not results:
            print("No matching found.")
            continue

        print(f"Selected documents: {', '.join(filenames)}")

        print("\nAnswer:")
        for score, filename, sentence in results:
          if score >= 0.50:
            confidence = "High"
          elif score >= 0.25:
            confidence = "Medium"
          else:
            confidence = "Low"

          print(sentence)
          print(f"Source: {filename}")
          print(f"Matching score: {score:.3f}")
          print(f"Confidence: {confidence}")
          
if __name__ == "__main__":
    main()