from schemas import QuizQuestion
from utils import parse_json_response
from gemini_client import generate_text


def generate_quiz(text: str) -> list[QuizQuestion]:
    """
    Generate exactly three MCQs from the supplied educational text.
    """

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions from the content below.

CONTENT:
{text}

Return ONLY valid JSON.

The JSON must have this exact structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "The exact correct option text",
    "explanation": "Short explanation of why this answer is correct."
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Only one correct answer per question.
- correct_answer must exactly match one option.
- Questions must be based on the supplied content.
- Make distractors plausible.
- Do not include Markdown.
- Do not include ```json.
"""

    raw_response = generate_text(
        prompt,
        temperature=0.7,
        max_output_tokens=2500,
    )

    data = parse_json_response(raw_response)

    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    questions = []

    for item in data[:3]:
        if not isinstance(item, dict):
            continue

        question = item.get("question")
        options = item.get("options")
        correct_answer = item.get("correct_answer")
        explanation = item.get("explanation", "")

        if not question:
            continue

        if not isinstance(options, list) or len(options) != 4:
            continue

        if correct_answer not in options:
            continue

        questions.append(
            QuizQuestion(
                question=str(question),
                options=[str(option) for option in options],
                correct_answer=str(correct_answer),
                explanation=str(explanation),
            )
        )

    if len(questions) != 3:
        raise ValueError(
            "Gemini did not return three valid quiz questions."
        )

    return questions