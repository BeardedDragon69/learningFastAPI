from fastapi import FastAPI
from routes.coaches import routerCoach
from routes.train import routerTrains



app = FastAPI()

app.include_router(routerCoach)
app.include_router(routerTrains)



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sertesir:icms1234@cluster0.qfgcqjz.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)