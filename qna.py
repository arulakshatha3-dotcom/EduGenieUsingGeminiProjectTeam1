from gemini_client import generate_text


def answer_question(question: str) -> str:
    """
    Answer an academic/general educational question.
    """

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Student question:
{question}

Instructions:
- Give a direct answer first.
- Explain the important concept simply.
- Use examples when useful.
- Avoid unnecessary complexity.
- Do not invent facts.
- If the question is ambiguous, clearly mention the assumption.
- Format the response so a student can easily study it.
"""

    return generate_text(
        prompt,
        temperature=0.5,
        max_output_tokens=1200,
    )