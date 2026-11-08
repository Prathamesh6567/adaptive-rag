
from pathlib import Path
from adaptive_router import route_query
from sentence_transformers import SentenceTransformer, util

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []

for path in DATA_DIR.glob("*.txt"):
    content = path.read_text(encoding="utf-8")

    for line in content.splitlines():
        line = line.strip()

        if line:
            documents.append((path.name, line))

if not documents:
    print("No document content found.")
    raise SystemExit

sentences = [sentence for _, sentence in documents]
embeddings = model.encode(sentences, convert_to_tensor=True)

while True:
    query = input("\nAsk a question (or 'exit'): ").strip()

    if query.lower() == "exit":
        print("Exiting semantic search. Bye bhai!")
        break

    if not query:
        print("Please enter a question.")
        continue

    selected = route_query(query)

    if not selected:
        print("No sufficiently relevant document found.")
        continue

    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = scores.argsort(descending=True)[:3]

    best_score = scores[top_indices[0]].item()

    if best_score < 0.50:
        print("No sufficiently relevant documents found.")
        continue

    print("\nSemantic search results:")

    for index in top_indices:
        i = int(index)
        print(f"\nDocument: {documents[i][0]}")
        print(f"Similarity: {scores[i].item():.3f}")
        print(f"Text: {documents[i][1]}")