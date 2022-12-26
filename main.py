import os,sys
from sensor.exception import SensorException
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline


if __name__ == "__main__":
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()

        #mongodb_client = MongoDBClient()
        #print(mongodb_client.database.list_collection_names())
    except Exception as e:
        raise SensorException(e,sys)




   
  


    


