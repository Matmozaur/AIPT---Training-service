import logging
from typing import Dict

from models.exercises import MuscleGroup,Training


def effective_sets(training: Training) -> Dict[MuscleGroup, float]:
    result = {k: 0 for k in MuscleGroup}
    for exercise_link in training.exercisesperformed:
        logging.debug(exercise_link)
        exercise = exercise_link.exerciseperformed
        for v in exercise.exercise.engagements:
            logging.debug(v)
            result[v.muscle_group_id] += v.engagement * exercise.sets
    return {k: round(v, 2) for k, v in result.items()}
