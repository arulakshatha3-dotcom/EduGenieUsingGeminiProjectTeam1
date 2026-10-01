from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_qa_validation():
    response = client.post(
        "/qa",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422


def test_explain_validation():
    response = client.post(
        "/explain",
        json={
            "topic": ""
        },
    )

    assert response.status_code == 422