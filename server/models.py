from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError(
                "Workout name must be at least 3 characters long"
            )
        return name.strip()

    @validates("description")
    def validate_description(self, key, description):
        if not description or len(description.strip()) < 5:
            raise ValueError(
                "Workout description must be at least 5 characters long"
            )
        return description.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError(
                "Exercise name must be at least 3 characters long"
            )
        return name.strip()

    @validates("description")
    def validate_description(self, key, description):
        if not description or len(description.strip()) < 5:
            raise ValueError(
                "Exercise description must be at least 5 characters long"
            )
        return description.strip()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=True)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    __table_args__ = (
        CheckConstraint(
            "sets > 0",
            name="check_sets_positive"
        ),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_reps_positive"
        ),
    )

    @validates("sets")
    def validate_sets(self, key, sets):
        if sets <= 0:
            raise ValueError("Sets must be greater than zero")
        return sets

    @validates("reps")
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than zero")
        return reps
