import logging
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
            logging.debug(training_input)
            training = Training()
            logging.debug(training)
            session.add(training)
            # session.commit()

            total_exercises = 0
            total_sets = 0

            # Iterate over the input exercises
            for exercise_id, sets in training_input.exercises.items():
                logging.debug(exercise_id)
                logging.debug(sets)
                # Ensure the exercise exists
                exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()
                logging.debug(exercise)
                if not exercise:
                    raise ValueError(f"Exercise with id {exercise_id} does not exist")

                # Create ExercisePerformed instance
                exercise_performed = ExercisePerformed(sets=sets,
                                                       exercise_id=exercise_id,
                                                       exercise=exercise)
                logging.debug(exercise_performed)
                session.add(exercise_performed)
                # session.commit()

                # Link to Training
                training_exercise_performed_link = TrainingExercisePerformedLink(
                    training_id=training.id,
                    exerciseperformed_id=exercise_performed.id,
                    exercise_performed=exercise_performed
                )
                session.add(training_exercise_performed_link)

                total_exercises += 1
                total_sets += sets
                logging.debug(training_exercise_performed_link)
                training.exercisesperformed.append(training_exercise_performed_link)
                session.flush()

            logging.debug(training)
            return TrainingEvaluation(effective_sets=effective_sets(training))
