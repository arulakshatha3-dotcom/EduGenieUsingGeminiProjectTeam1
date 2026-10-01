from gemini_client import generate_text


def summarize_text(text: str) -> str:
    """
    Summarize educational content.
    """

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational content.

Text:
{text}

Requirements:
- Keep the main ideas.
- Remove unnecessary repetition.
- Use simple language.
- Preserve important facts.
- Organize the summary with headings or bullet points where appropriate.
- Do not introduce information that is not present in the text.
- Make it useful for exam revision.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1800,
    )