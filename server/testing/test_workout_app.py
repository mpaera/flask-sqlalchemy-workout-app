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
            name="Strength Training",
            description="Full body strength workout"
        )

        exercise = Exercise(
            name="Push Ups",
            description="Upper body exercise"
        )

        db.session.add_all([workout, exercise])
        db.session.commit()

        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=3,
            reps=10
        )

        db.session.add(workout_exercise)
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

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Strength Training"


def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Push Ups"


def test_get_workout(client):
    response = client.get("/workouts/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Strength Training"


def test_get_exercise(client):
    response = client.get("/exercises/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Push Ups"


def test_workout_exercise_relationship(client):
    response = client.get("/workouts/1")

    assert response.status_code == 200

    data = response.get_json()

    assert "exercises" in data


def test_missing_workout(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_missing_exercise(client):
    response = client.get("/exercises/999")
    assert response.status_code == 404
