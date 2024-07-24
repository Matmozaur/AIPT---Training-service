from fastapi import APIRouter, HTTPException

from models.request import TrainingInput
from models.response import TrainingEvaluation
from services.training_service import TrainingService
from utils.exceptions import TrainingNotFoundError

router_trainings = APIRouter()

training_service = TrainingService()


@router_trainings.post("/analyse_training/")
async def analyse_training(req: TrainingInput) -> TrainingEvaluation:
    try:
        return training_service.analyse_training(req)
    except TrainingNotFoundError:
        raise HTTPException(400, "Could not find requested exercise")
