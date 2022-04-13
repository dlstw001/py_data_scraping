from pymongo import MongoClient
import pymongo

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.zuec9.mongodb.net/test"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient

client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
print(client.list_database_names())
db = client.data
print(db.list_collection_names())


