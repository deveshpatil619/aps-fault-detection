import os,sys
from sensor.exception import SensorException
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import read_yaml_file
from sensor.config.mongo_db_connection import MongoDBClient
from fastapi import FastAPI
from sensor.constant.application import APP_HOST,APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response



"""env_file_path = os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']
"""









if __name__ == "__main__":
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()

        #mongodb_client = MongoDBClient()
        #print(mongodb_client.database.list_collection_names())
    except Exception as e:
        raise SensorException(e,sys)




   
  


    


