from sensor.config.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys



def test_exception():
    try:
        logging.info("We are dividing 1 by zero")
        result = 2/0
        print(result)
    except Exception as e:
        raise SensorException(e,sys)


if __name__ == "__main__":
    try:
        test_exception()
    except Exception as e:
        print(e)





   # mongodb_client = MongoDBClient()
    #print(mongodb_client.database.list_collection_names())

