from enum import Enum
from typing import List, Optional

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


class ExercisePerformed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id", primary_key=True)
    sets: int
