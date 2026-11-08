
from pathlib import Path
import re

from sentence_transformers import SentenceTransformer, util
try:
    from .adaptive_router import route_query
except ImportError:
    from adaptive_router import route_query
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_NAME = "all-MiniLM-L6-v2"
THRESHOLD = 0.50
TOP_K = 3

print("Loading semantic search model...")
model = SentenceTransformer(MODEL_NAME)

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

def retrieve(query, top_k=TOP_K):
    filenames = route_query(query)

    if not filenames:
        return []

    documents = load_sentences(filenames)

    if not documents:
        return []

    sentences = [sentence for _, sentence in documents]
    embeddings = model.encode(sentences, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = scores.argsort(descending=True)[:top_k]

    results = []

    for index in top_indices:
        i = int(index)
        score = scores[i].item()

        if score >= THRESHOLD:
            filename, sentence = documents[i]
            results.append((score, filename, sentence))

    return results

def main():
    print("\nAdaptive RAG — Semantic Retriever")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nAsk a question: ").strip()

        if query.lower() == "exit":
            print("Exiting. Bye bhai!")
            break

        if not query:
            print("Please enter a question.")
            continue

        filenames = route_query(query)

        if not filenames:
            print("No matching document found.")
            continue

        results = retrieve(query)

        if not results:
            print("No sufficiently relevant document found.")
            continue

        print("Selected documents:", ", ".join(filenames))
        print("\nRelevant results:")

        for score, filename, sentence in results:
            if score >= 0.60:
                confidence = "High"
            elif score >= THRESHOLD:
                confidence = "Medium"
            else:
                confidence = "Low"

            print(f"\nAnswer: {sentence}")
            print(f"Source: {filename}")
            print(f"Similarity: {score:.3f}")
            print(f"Confidence: {confidence}")

if __name__ == "__main__":
    main()