from typing import Dict

from models.exercises import MuscleGroup,Training


def effective_sets(training: Training) -> Dict[MuscleGroup, float]:
    result = {k: 0 for k in MuscleGroup}
    for exercise in training.exercises:
        for k, v in exercise.engagements.items():
            result[k.value] += v * exercise.sets
    return {k: round(v, 2) for k, v in result.items()}
