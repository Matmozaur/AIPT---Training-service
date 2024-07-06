from typing import Dict, Optional, List

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from models.exercises import MuscleGroup, ExercisePerformed


class Training(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercises: List["TrainingExercisePerformedLink"] = Relationship(back_populates="exerciseperformed")


class TrainingExercisePerformedLink(SQLModel, table=True):
    training_id: Optional[int] = Field(default=None, foreign_key="training.id", primary_key=True)
    exerciseperformed_id: Optional[int] = Field(default=None, foreign_key="exercise.id", primary_key=True)
    exerciseperformed: "ExercisePerformed" = Relationship(back_populates="exerciseperformed")
    training: "Training" = Relationship(back_populates="training")


class TrainingEvaluation(BaseModel):
    effective_sets: Dict[MuscleGroup, float]
