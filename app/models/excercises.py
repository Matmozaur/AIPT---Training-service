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
    Gluts = 'Gluts'
    Quads = 'Quads'
    Hamstrings = 'Hamstrings'
    Calves = 'Calves'
    

class Exercise(BaseModel):
    name: str
    engagements: Dict[MuscleGroup, float]


class ExercisePerformed(Exercise):
    sets: int
