import os
import datetime
from pymongo import MongoClient

uri = "mongodb+srv://kacper:test@baza1.flvotty.mongodb.net/?retryWrites=true&w=majority&appName=Baza1"
database_name = "products"  
collection_name = "ecommerce"  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

def backup_database():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{current_time}.json")

    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    try:
        print("Pinged your deployment. You successfully connected to MongoDB!")

        with open(backup_path, "w") as backup_file:
            for document in collection.find():
                backup_file.write(str(document) + "\n")

        print("Backup completed successfully.")

    except Exception as e:
        print(f"Failed to backup MongoDB: {e}")

if __name__ == "__main__":
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    backup_database()
