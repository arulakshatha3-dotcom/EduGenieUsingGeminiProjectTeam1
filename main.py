from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest,
    HealthResponse,
    LearningPathRequest,
    QuestionRequest,
    QuizRequest,
    QuizResponse,
    SimpleResponse,
    TextRequest,
)

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie",
        },
    )


@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():
    return {
        "status": "healthy",
        "application": "EduGenie",
    }


@app.post(
    "/qa",
    response_model=SimpleResponse,
)
async def qa(request: QuestionRequest):
    try:
        result = answer_question(request.question)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "result": str(exc),
        }


@app.post(
    "/explain",
    response_model=SimpleResponse,
)
async def explain(request: ExplainRequest):
    try:
        result = explain_topic(request.topic)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "result": str(exc),
        }


@app.post(
    "/quiz",
    response_model=QuizResponse,
)
async def quiz(request: QuizRequest):
    try:
        questions = generate_quiz(request.text)

        return {
            "success": True,
            "questions": questions,
        }

    except Exception:
        return {
            "success": False,
            "questions": [],
        }


@app.post(
    "/summarize",
    response_model=SimpleResponse,
)
async def summarize(request: TextRequest):
    try:
        result = summarize_text(request.text)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "result": str(exc),
        }


@app.post(
    "/learn/recommendations",
    response_model=SimpleResponse,
)
async def learning_recommendations(
    request: LearningPathRequest,
):
    try:
        result = get_learning_recommendations(
            topic=request.topic,
            level=request.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "result": str(exc),
        }