from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from schema.schemas import listTrainSerial, individualTrainSerial
from models.train import Train
from config.database import trainCollection, collectionName
from bson import ObjectId

routerTrains = APIRouter(
    prefix="/trains",
    tags=['trains']
)

class CoachAssignment(BaseModel):
    coachIds: List[str]

@routerTrains.get("/getAllTrain")
async def get_trains():
    trains = list(trainCollection.find())
    return listTrainSerial(trains)

@routerTrains.post("/addTrain")
async def add_train(train: Train):
    existing = trainCollection.find_one({"trainId": train.trainId})
    if existing:
        raise HTTPException(status_code=400, detail="Train ID already exists")
    trainCollection.insert_one(dict(train))
    trains= list(trainCollection.find())
    return {listTrainSerial(train)}

@routerTrains.post("/assignCoachesToTrain/{trainId}")
async def assign_coaches_to_train(trainId: str, coach_assignment: CoachAssignment):
    try:
        train_obj_id = ObjectId(trainId)
    except:
        raise HTTPException(status_code=400, detail="Invalid train ID format")

    train = trainCollection.find_one({"_id": train_obj_id})
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    for coach_id in coach_assignment.coachIds:
        try:
            coach_obj = ObjectId(coach_id)
        except:
            raise HTTPException(status_code=400, detail=f"Invalid coach ID format: {coach_id}")

        if not collectionName.find_one({"_id": coach_obj}):
            raise HTTPException(status_code=404, detail=f"Coach with ID {coach_id} not found")

    trainCollection.find_one_and_update(
        {"_id": train_obj_id},
        {"$addToSet": {"coachIds": {"$each": coach_assignment.coachIds}}}
    )

    return {
        "message": "Coaches assigned successfully",
        "trainId": trainId,
        "coachIds": coach_assignment.coachIds
    }


@routerTrains.delete("/deleteTrain/{id}")
async def deleteTrain(id: str):
    train = trainCollection.find_one({"_id": ObjectId(id)})

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    trainCollection.delete_one({"_id": ObjectId(id)})

    return {"message": "Train deleted successfully", "trainId": id}