from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner",
) -> str:
    """
    Generate a structured learning path.
    """

    prompt = f"""
You are EduGenie, a personalized learning-path assistant.

Create a learning roadmap for:

Topic:
{topic}

Student level:
{level}

Create a practical path from the student's current level
towards advanced understanding.

Use this structure:

# Learning Roadmap

## 1. Current Level
Explain what the learner should already know.

## 2. Stage 1 - Fundamentals
List the concepts to learn.

## 3. Stage 2 - Intermediate
List the concepts to learn.

## 4. Stage 3 - Advanced
List the concepts to learn.

## 5. Practice Projects
Give suitable hands-on projects.

## 6. Suggested Resources
Suggest:
- Documentation
- Tutorials
- Videos
- Books
- Practice websites

Do not invent specific URLs.
If you mention a resource, use a recognizable resource name.

## 7. Suggested Timeline
Give a realistic weekly learning plan.

## 8. Final Goal
Explain what the learner should be able to do after completing the roadmap.

Keep the roadmap practical and beginner-friendly.
"""

    return generate_text(
        prompt,
        temperature=0.7,
        max_output_tokens=3000,
    )