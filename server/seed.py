from app import app, db
from models import Workout, Exercise


with app.app_context():
    Workout.query.delete()
    Exercise.query.delete()

    workouts = [
        Workout(
            name="Full Body Workout",
            description="A complete full body strength workout"
        ),
        Workout(
            name="Upper Body Workout",
            description="A workout focused on upper body muscles"
        )
    ]

    exercises = [
        Exercise(
            name="Push Ups",
            muscle_group="Chest"
        ),
        Exercise(
            name="Squats",
            muscle_group="Legs"
        ),
        Exercise(
            name="Plank",
            muscle_group="Core"
        )
    ]

    db.session.add_all(workouts)
    db.session.add_all(exercises)
    db.session.commit()

    print("Database seeded successfully")