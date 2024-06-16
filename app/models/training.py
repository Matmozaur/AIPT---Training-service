from pydantic import BaseModel
from typing import List, Dict

from models.exercises import ExercisePerformed, MuscleGroup


class Training(BaseModel):
    exercises: List[ExercisePerformed]


class TrainingEvaluation(BaseModel):
    effective_sets: Dict[MuscleGroup, float]
