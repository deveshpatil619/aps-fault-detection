import os
from datetime import datetime
from sensor.exception import SensorException


FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"



class TrainingPipelineConfig:
    def __init__(self):  ## here the output of the pipeline modules will be stored in artifact folder
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strptime('%d_%m_%Y__%H:%M:%S')}")
        except Exception as e:
            raise SensorException(e, sys)



class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "aps"
            self.collection_name = "sensor"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion") ## inside the srtifact directory the data_ingestion folder will be created
            self.feature_store_path = os.path.join(self.data_ingestion_dir,"Feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"train_dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"test_dataset",TEST_FILE_NAME)
            self.test_size = 0.2

    def to_dict(self,)->dict:
        try:
            self.__dict__
        except Exception as e:
            raise SensorException(e,sys)



class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...