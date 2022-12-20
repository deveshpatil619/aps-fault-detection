## importing the important libraries
import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_db_connection
import os,sys


def get_collections_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """ 
    Description:- This function return the list of  collection as dataframe
    ==============================================================
    params:
    database_name : database name
    collection_name : collection name
    ==============================================================
    return pandas dataframe of a collection """
    try:
        logging.info(f"Reading the data from database:{database_name} and collection:{collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find())) 

        logging.info(f"Found the columns:{df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column _id")
            df = df.drop("_id",axis =1) 
        logging.info(f"Rows and columns in df:{df.shape}")
        return df
    except Exception as e:
        raise SensorException(e, sys)















