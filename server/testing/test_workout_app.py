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


# -------------------------------------------------
# EXISTING 8 TESTS
# -------------------------------------------------

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


# -------------------------------------------------
# REBUILT 9 TESTS
# -------------------------------------------------

def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "name": "Cardio Workout",
            "description": "Thirty minute cardio session"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Cardio Workout"
    assert data["description"] == "Thirty minute cardio session"
    assert "id" in data


def test_create_workout_missing_required_field(client):
    response = client.post(
        "/workouts",
        json={
            "name": "Cardio Workout"
        }
    )

    assert response.status_code == 400


def test_delete_workout(client):
    response = client.delete("/workouts/1")

    assert response.status_code == 200

    check = client.get("/workouts/1")
    assert check.status_code == 404


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Squats",
            "muscle_group": "Legs"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Squats"
    assert data["muscle_group"] == "Legs"
    assert "id" in data


def test_create_exercise_missing_required_field(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Squats"
        }
    )

    assert response.status_code == 400


def test_delete_exercise(client):
    response = client.delete("/exercises/1")

    assert response.status_code == 200

    check = client.get("/exercises/1")
    assert check.status_code == 404


def test_add_exercise_to_workout(client):
    response = client.post(
        "/workouts/1/exercises",
        json={
            "exercise_id": 1,
            "sets": 3,
            "reps": 12
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["workout_id"] == 1
    assert data["exercise_id"] == 1
    assert data["sets"] == 3
    assert data["reps"] == 12


def test_add_exercise_to_missing_workout(client):
    response = client.post(
        "/workouts/999/exercises",
        json={
            "exercise_id": 1,
            "sets": 3,
            "reps": 12
        }
    )

    assert response.status_code == 404


def test_add_missing_exercise_to_workout(client):
    response = client.post(
        "/workouts/1/exercises",
        json={
            "exercise_id": 999,
            "sets": 3,
            "reps": 12
        }
    )

    assert response.status_code == 404
