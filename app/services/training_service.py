import os

from models.exercises import Exercise, ExercisePerformed, TrainingExercisePerformedLink
from models.request import TrainingInput
from models.exercises import Training
from models.response import TrainingEvaluation
from utils.training_score import effective_sets

from sqlmodel import create_engine, Session


DATABASE_URL = f"postgresql://{os.environ.get("DB_USER", 'postgres')}:{os.environ.get("DB_PASS", 'test')}@{os.environ.get("DB_DOMAIN", 'pg_training')}/postgres"


class TrainingService:

    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)

    def analyse_training(self, training_input: TrainingInput) -> TrainingEvaluation:
        with Session(self.engine) as session:
            training = Training()
            session.add(training)
            session.commit()  # Ensure training.id is populated

            total_exercises = 0
            total_sets = 0

            # Iterate over the input exercises
            for exercise_id, sets in training_input.exercises.items():
                # Ensure the exercise exists
                exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()
                if not exercise:
                    raise ValueError(f"Exercise with id {exercise_id} does not exist")

                # Create ExercisePerformed instance
                exercise_performed = ExercisePerformed(sets=sets, exercise_id=exercise_id)
                session.add(exercise_performed)
                session.commit()  # Ensure exercise_performed.id is populated

                # Link to Training
                training_exercise_performed_link = TrainingExercisePerformedLink(
                    training_id=training.id,
                    exerciseperformed_id=exercise_performed.id
                )
                session.add(training_exercise_performed_link)

                total_exercises += 1
                total_sets += sets

        return TrainingEvaluation(effective_sets=effective_sets(training))
