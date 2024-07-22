from enum import Enum
from typing import List, Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship


class MuscleGroup(str, Enum):
    Chest = 'Chest'
    Upper_back = 'Upper_back'
    Lower_back = 'Lower_back'
    Abs = 'Abs'
    Traps = 'Traps'
    Shoulders = 'Shoulders'
    Biceps = 'Biceps'
    Triceps = 'Triceps'
    Neck = 'Neck'
    Forearms = 'Forearms'
    Glutes = 'Glutes'
    Quads = 'Quads'
    Hamstrings = 'Hamstrings'
    Calfs = 'Calfs'
    Obliques = 'Obliques'


class MuscleGroupModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: MuscleGroup = Field(sa_column_kwargs={"unique": True})
    engagements: List["ExerciseMuscleGroupLink"] = Relationship(back_populates="muscle_group")


class ExerciseMuscleGroupLink(SQLModel, table=True):
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id", primary_key=True)
    muscle_group_id: Optional[int] = Field(default=None, foreign_key="musclegroupmodel.id", primary_key=True)
    engagement: float = Field(default=0)
    exercise: "Exercise" = Relationship(back_populates="engagements")
    muscle_group: "MuscleGroupModel" = Relationship(back_populates="engagements")


class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    engagements: List["ExerciseMuscleGroupLink"] = Relationship(back_populates="exercise")
    exerciseperformed: "ExercisePerformed" = Relationship(back_populates="exercise")


class ExercisePerformed(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True, unique=True)
    sets: int
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id")
    exercise: "Exercise" = Relationship(back_populates="exerciseperformed")
    trainings: "TrainingExercisePerformedLink" = Relationship(back_populates="exerciseperformed")


class Training(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    exercisesperformed: List["TrainingExercisePerformedLink"] = Relationship(back_populates="training")


class TrainingExercisePerformedLink(SQLModel, table=True):
    training_id: Optional[str] = Field(default=None, foreign_key="training.id", primary_key=True)
    exerciseperformed_id: Optional[str] = Field(default=None, foreign_key="exerciseperformed.id", primary_key=True)
    exerciseperformed: "ExercisePerformed" = Relationship(back_populates="trainings")
    training: "Training" = Relationship(back_populates="exercisesperformed")
