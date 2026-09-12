import pytest

from app import app, db
from models import Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        workout = Workout(
            name="Full Body",
            description="A complete full body workout"
        )

        exercise = Exercise(
            name="Push Ups",
            description="Upper body exercise"
        )

        db.session.add(workout)
        db.session.add(exercise)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200


def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200


def test_get_workout_by_id(client):
    response = client.get("/workouts/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Full Body"


def test_get_exercise_by_id(client):
    response = client.get("/exercises/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Push Ups"