from typing import Dict

from pydantic import BaseModel

from models.exercises import MuscleGroup


class TrainingEvaluation(BaseModel):
    effective_sets: Dict[MuscleGroup, float]
