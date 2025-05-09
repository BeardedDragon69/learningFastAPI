import random
from typing import List
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from models.coaches import Coach
from config.database import collectionName, trainCollection
from schema.schemas import listSerial

routerCoach = APIRouter(
    prefix="/coach",
    tags=['coach']
)

def allocate_random_seats(totalSeats: int, bookedSeats: list, seatsToBook: int) -> list:
    all_seats = set(range(1, totalSeats + 1))
    available_seats = list(all_seats - set(bookedSeats))

    if len(available_seats) < seatsToBook:
        raise ValueError("Not enough available seats to complete the booking.")

    return random.sample(available_seats, seatsToBook)

@routerCoach.get("/getAllCoaches")
async def getCoaches():
    coaches = listSerial(collectionName.find())
    return coaches


@routerCoach.get("/{id}/seatStatus")
async def getSeatStatus(id: str):
    coach = collectionName.find_one({"_id": ObjectId(id)})

    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    totalSeats = coach["totalSeats"]
    bookedSeats = coach.get("bookedSeats", [])
    availableSeats = list(set(range(1, totalSeats + 1)) - set(bookedSeats))

    return {
        "totalSeats": totalSeats,
        "seatsBooked": bookedSeats,
        "seatsAvailable": availableSeats
    }

@routerCoach.get("/getAllBookedSeatsDetailed")
async def getAllBookedSeatsDetailed():
    result = []

    trains = list(trainCollection.find())
    for train in trains:
        train_id = str(train["_id"])
        train_name = train["trainName"]
        train_code = train["trainId"]
        coach_ids = train.get("coachIds", [])

        for coach_id in coach_ids:
            coach = collectionName.find_one({"_id": ObjectId(coach_id)})
            if not coach:
                continue

            coach_number = coach["number"]
            coach_object_id = str(coach["_id"])
            booked_seats = coach.get("bookedSeats", [])

            for seat in booked_seats:
                seat_number = seat["seatNo"] if isinstance(seat, dict) else seat  # handle both formats
                result.append({
                    "trainId": train_code,
                    "trainName": train_name,
                    "coachId": coach_object_id,
                    "coachNumber": coach_number,
                    "seatNumber": seat_number
                })

    return result


@routerCoach.post("/postCoach")
async def postCoach(coach: Coach):
    coach_dict = dict(coach)
    coach_dict["bookedSeats"] = []
    collectionName.insert_one(coach_dict)
    return {"message": "Coach added successfully"}

@routerCoach.put("/{id}/updateSeatBooking")
async def updateSeatBooking(id: str, noOfSeats: int):
    coach = collectionName.find_one({"_id": ObjectId(id)})

    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    totalSeats = coach["totalSeats"]
    bookedSeatsCount = coach["seatsBooked"]
    bookedSeatsList = coach.get("bookedSeats", [])

    try:
        allocatedSeats = allocate_random_seats(totalSeats, bookedSeatsList, noOfSeats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    newBookedSeatsList = bookedSeatsList + allocatedSeats
    newBookedCount = bookedSeatsCount + noOfSeats
    isFilled = newBookedCount == totalSeats

    collectionName.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "seatsBooked": newBookedCount,
                "bookedSeats": newBookedSeatsList,
                "filled": isFilled
            }
        }
    )

    return {
        "message": "Seats successfully booked",
        "allocatedSeats": allocatedSeats,
        "seatsBooked": newBookedCount,
        "filled": isFilled
    }


@routerCoach.put("/{id}/cancelSeatBooking")
async def cancelSeatBooking(id: str, seatNumbers: List[int]):
    coach = collectionName.find_one({"_id": ObjectId(id)})

    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    bookedSeats = coach.get("bookedSeats", [])

    invalidSeats = [seat for seat in seatNumbers if seat not in bookedSeats]
    if invalidSeats:
        raise HTTPException(status_code=400, detail=f"Seats not booked: {invalidSeats}")

    updatedSeats = list(set(bookedSeats) - set(seatNumbers))
    updatedCount = len(updatedSeats)
    isFilled = updatedCount == coach["totalSeats"]

    collectionName.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "bookedSeats": updatedSeats,
                "seatsBooked": updatedCount,
                "filled": isFilled
            }
        }
    )

    return {
        "message": "Seat(s) cancelled successfully",
        "cancelledSeats": seatNumbers,
        "seatsBooked": updatedCount,
        "filled": isFilled
    }

@routerCoach.delete("/deleteCoach/{id}")
async def deleteCoach(id: str):
    coach = collectionName.find_one({"_id": ObjectId(id)})

    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")


    collectionName.delete_one({"_id": ObjectId(id)})

  
    trainCollection.update_many(
        {"coachIds": ObjectId(id)},
        {"$pull": {"coachIds": ObjectId(id)}}
    )

    return {"message": "Coach deleted successfully and removed from assigned trains", "coachId": id}


