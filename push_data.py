import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {MONGO_DB_URL}")

import certifi
ca=certifi.where() #certifcate authority bundle

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

class NetworkDataExtract():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            logger.logging.info("MongoDB client initialized successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def push_data_to_mongodb(self, data: pd.DataFrame, db_name: str, collection_name: str):
        try:
            db = self.client[db_name]
            collection = db[collection_name]
            data_dict = json.loads(data.to_json(orient="records"))
            collection.insert_many(data_dict)
            logger.logging.info(f"Data pushed to MongoDB collection '{collection_name}' in database '{db_name}'.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        logger.logging.info("Starting the data extraction process.")
        data_extractor = NetworkDataExtract()
        records = data_extractor.cv_to_json_convertor("Network_Data/phishing.csv")
        count = data_extractor.insert_data_to_mongodb(records, "network_security_db", "network_data")
        logger.logging.info(f"Inserted {count} records into MongoDB.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    File_PATH = "Network_Data/phishing.csv"
    DATABASE="network_security_db"
    Collection ="network_data"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_convertor(file_path=File_PATH)
    print(records)
    no_of_records=networkobj.insert_data_to_mongodb(records,DATABASE,Collection)

    