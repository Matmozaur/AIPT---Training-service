from pydantic import BaseModel
from typing import List

from models.excercises import ExercisePerformed


class Training(BaseModel):
    exercises: List[ExercisePerformed]
