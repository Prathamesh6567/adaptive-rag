
# Adaptive RAG - Smart College Assistant

## Overview
This project retrieves relevant information from college documents based on a user's question.

## Current Features
- Routes questions to attendance or library documents.
- Retrieves matching sentences from selected files.
- Calculates a keyword-overlap similarity score.
- Displays a basic confidence label.
- Returns no results for unsupported topics when no matching keywords are found.

## Project Structure

adaptive-rag/
├── data/
│   ├── attendance.txt
│   └── library.txt
├── src/
│   ├── adaptive_router.py
│   ├── main.py
│   └── retriever.py
├── tests/
└── README.md

## Requirements
- Python 3.10 or later
- No external Python packages required for the current basic implementation

## Run the Project

From the project root, run:

```bash
python src/retriever.py
```

Ask a question when prompted. Type `exit` to quit.

## Example Questions
- What is the minimum attendance required?
- How many books can I borrow at a time?
- Can I borrow books if my attendance is low?
- Who is the principal of the college?

## Current Limitations
- Retrieval uses keyword overlap, not embedding-based semantic search.
- Confidence labels are heuristic, not calibrated probabilities.
- Answers are retrieved document sentences, not LLM-generated responses.

## Future Improvements
- Add text chunking and embeddings.
- Integrate a vector database.
- Add an LLM for context-grounded answers.
- Implement adaptive retrieval and automated tests.


## Architecture

1. User enters a question.
2. The adaptive router selects relevant documents.
3. The semantic retriever loads sentences from the selected documents.
4. Sentence Transformers generates embeddings.
5. Cosine similarity ranks the sentences against the question.
6. A similarity threshold filters low-scoring results.
7. The system displays relevant text, source filename, similarity score, and confidence.

## Current Limitations

- The router uses predefined keywords.
- The similarity threshold is experimental and may need tuning.
- The system retrieves existing text; it does not generate answers using an LLM.
- Current data sources are local text files.

## Future Improvements

- Add more document types and data sources.
- Improve routing for ambiguous questions.
- Evaluate retrieval quality with a test dataset.
- Add an LLM for grounded answer generation.
- Build a user-friendly interface.