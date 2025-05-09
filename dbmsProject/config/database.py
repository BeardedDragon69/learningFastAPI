from pymongo import MongoClient

client = MongoClient("mongodb+srv://sertesir:icms1234@cluster0.qfgcqjz.mongodb.net/?appName=Cluster0")


db = client.train_db

collectionName = db["coachCollection"]
trainCollection = db["trainCollection"]