from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


@app.route("/")
def index():
    return jsonify({
        "message": "Workout API is running"
    })


# -----------------------------------
# WORKOUTS
# -----------------------------------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(
        workouts_schema.dump(workouts)
    ), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    return jsonify(
        workout_schema.dump(workout)
    ), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())

        workout = Workout(
            name=data["name"],
            description=data["description"]
        )

        db.session.add(workout)
        db.session.commit()

        return jsonify(
            workout_schema.dump(workout)
        ), 201

    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    except ValueError as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 400


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200


# -----------------------------------
# EXERCISES
# -----------------------------------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(
        exercises_schema.dump(exercises)
    ), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    return jsonify(
        exercise_schema.dump(exercise)
    ), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())

        exercise = Exercise(
            name=data["name"],
            description=data["description"]
        )

        db.session.add(exercise)
        db.session.commit()

        return jsonify(
            exercise_schema.dump(exercise)
        ), 201

    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    except ValueError as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 400


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200


# -----------------------------------
# ADD EXERCISE TO WORKOUT
# -----------------------------------

@app.route("/workouts/<int:workout_id>/exercises", methods=["POST"])
def add_exercise_to_workout(workout_id):
    try:
        workout = db.session.get(Workout, workout_id)

        if not workout:
            return jsonify({
                "error": "Workout not found"
            }), 404

        data = workout_exercise_schema.load(
            request.get_json()
        )

        exercise = db.session.get(
            Exercise,
            data["exercise_id"]
        )

        if not exercise:
            return jsonify({
                "error": "Exercise not found"
            }), 404

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=data["exercise_id"],
            sets=data["sets"],
            reps=data.get("reps")
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201

    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    except ValueError as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)