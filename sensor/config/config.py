## importing the required libraries

import pandas as pd
import pymongo
from pymongo import MongoClient
import json
from dataclasses import dataclass


## here we will provide the mongodb localhost url to connect python to mongodb

@dataclass
class EnvironmentVariable:

    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key:str = os.getenv("AWS_SECRET_KEY_ACCESS")


env_var = EnvironmentVariable()
mongo_client = MongoClient(env_var.mongo_db_url) ## calling the mongoclient url
TARGET_COLUMN = "class"  ## specifing the target_column
















