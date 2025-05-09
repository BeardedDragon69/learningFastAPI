from typing import List
from pydantic import BaseModel, Field

class Coach(BaseModel):
       number: int
       type: str
       totalSeats: int = Field(lt=31, gt=29)
       seatsBooked: int = Field(lt=31)
       # seatsLeft: int = totalSeats-seatsBooked
       bookedSeats: List[int] =[]
       filled: bool