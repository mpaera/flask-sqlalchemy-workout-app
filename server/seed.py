from app import app, db
from models import Workout, Exercise, WorkoutExercise


with app.app_context():
    db.drop_all()
    db.create_all()

    workout1 = Workout(
        name="Full Body Workout",
        description="A complete full body strength workout"
    )

    workout2 = Workout(
        name="Upper Body Workout",
        description="A workout focused on upper body muscles"
    )

    exercise1 = Exercise(
        name="Push Ups",
        description="Upper body pushing exercise"
    )

    exercise2 = Exercise(
        name="Squats",
        description="Lower body strength exercise"
    )

    exercise3 = Exercise(
        name="Plank",
        description="Core stability exercise"
    )

    db.session.add_all([
        workout1,
        workout2,
        exercise1,
        exercise2,
        exercise3
    ])

    db.session.commit()

    print("Database seeded successfully!")
