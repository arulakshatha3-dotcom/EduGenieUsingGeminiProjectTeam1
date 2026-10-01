from gemini_client import generate_text


def explain_topic(topic: str) -> str:
    """
    Explain a difficult concept in beginner-friendly language.
    """

    prompt = f"""
You are EduGenie, a patient educational tutor.

Explain the following topic to a student:

Topic:
{topic}

Use this structure:

1. Simple Definition
2. How It Works
3. Easy Example
4. Important Points
5. One-line Summary

Requirements:
- Use simple English.
- Avoid unnecessary technical terms.
- If a technical term is necessary, explain it.
- Make the explanation suitable for a beginner.
"""

    return generate_text(
        prompt,
        temperature=0.6,
        max_output_tokens=1800,
    )