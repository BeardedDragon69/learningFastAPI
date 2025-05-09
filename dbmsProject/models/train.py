from pydantic import Field, BaseModel

from typing import List

from bson import ObjectId

class Train(BaseModel):
       trainName: str = Field(..., example="Rajdhani Express")
       trainId: str = Field(..., example= "12345")
       stations: List[str] = Field(..., example=["Delhi", "Kanpur", "Prayagraj"])
       coachIds: List[str] =Field(..., examples=["CoachId 1", "CoachId 2"])

