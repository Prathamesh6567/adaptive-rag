from ollama import chat
import os

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def generate_answer(query, results):

    if not query.strip():
        return "Please enter a valid question."

    if not results:
        return (
            "I couldn't find enough relevant information "
            "in the available college documents."
        )

    context_parts = []

    for score, filename, sentence in results:
        context_parts.append(
            f"Document: {filename}\n"
            f"Information: {sentence}"
        )

    context = "\n\n".join(context_parts)

    system_prompt = """
You are a college information assistant.

Answer questions using ONLY the provided context.

IMPORTANT RULES:

1. Read every retrieved sentence carefully.
2. Understand the meaning, not just exact keywords.
3. Different wording can express the same meaning.
4. For example:
   Question: How long can students keep borrowed books?
   Context: Books must be returned within 14 days.
   Correct answer: Students can keep borrowed books
   for up to 14 days.
5. Never ignore relevant information in the context.
6. Never invent facts or use outside knowledge.
7. If the answer genuinely cannot be found in the
   context, say that the information is unavailable.
8. Give a direct and concise answer.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": (
                    f"Question: {query}\n\n"
                    f"Retrieved information:\n{context}\n\n"
                    "Answer the question using the retrieved information."
                )
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 150
        }
    )

    answer = response.message.content.strip()

    if not answer:
        return "The model returned an empty response."

    return answer