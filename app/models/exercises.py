from pydantic import BaseModel
from enum import Enum
from typing import Dict


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


class Exercise(BaseModel):
    name: str
    engagements: Dict[MuscleGroup, float]


class ExercisePerformed(Exercise):
    sets: int
