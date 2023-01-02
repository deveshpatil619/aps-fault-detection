""" For neuro-lab mongo db connection data-dump """

import pandas as pd
import pymongo
from pymongo import MongoClient
import json

## provide the mongodb localhost url to connect python to mongodb
client = MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH = "/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME ="aps"         ## db name
COLLECTION_NAME ="sensor"  ## main folder name


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns :{df.shape}")

    ## convert the dataframe to json so that we can dump the data into mongodb

    json_record = list(json.loads(df.T.to_json()).values())  ##transposing the dataframe data and 
    print(json_record[0])

    ## to insert into the database we write
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    





