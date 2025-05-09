def individualSerial(coach) -> dict:
       return{
              "id": str(coach["_id"]),
              "number":int(coach["number"]),
              "type":str(coach["type"]),
              "totalSeats" : int(coach["totalSeats"]),
              "seatsBooked": int(coach["seatsBooked"]),
              # "seatsLeft": int(coach["seatsLeft"]),
              "filled": coach["filled"]
       }

def individualTrainSerial(train)->dict:
       return{
              "id": str(train["_id"]),
              "trainName": str(train["trainName"]),
              "trainId": int(train["trainId"]),
              "stations": str (train["stations"]),
              "coachId" : [str(cid) for cid in train.get("coachIds", [])]
       }



def listSerial(coaches) -> list:
       return [individualSerial(coach) for coach in coaches]

def listTrainSerial(trains)->list:
       return[individualTrainSerial(train) for train in trains]