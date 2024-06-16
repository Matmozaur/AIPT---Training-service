from typing import Dict

from pydantic import BaseModel


class TrainingInput(BaseModel):
    exercises: Dict[int, int]
