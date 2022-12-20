import os,sys
from sensor.config.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline import training_pipeline
from sensor.data_access.sensor_data import SensorData


if __name__ == "__main__":
    training_pipeline = training_pipeline.TrainPipeline()
    training_pipeline.run_pipeline()




   # mongodb_client = MongoDBClient()
    #print(mongodb_client.database.list_collection_names())
  


    


