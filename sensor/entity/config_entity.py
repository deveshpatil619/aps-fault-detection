## Required_imports
import os,sys
from datetime import datetime
from sensor.exception import SensorException
from sensor.constant import training_pipeline



class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):  ## here the output of the pipeline modules will be stored in artifact folder
        try:
            timestamp = timestamp.strftime('%d_%m_%Y__%H:%M:%S')
            self.pipeline_name : str = training_pipeline.PIPEINE_NAME
            self.artifact_dir : str = os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
            self.timestamp :str = timestamp
        except Exception as e:
            raise SensorException(e, sys)



class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name :str = "aps"
            self.collection_name :str= "sensor"

            self.data_ingestion_dir : str= os.path.join(training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME) ## inside the artifact directory the data_ingestion folder will be created
            self.feature_store_path : str= os.path.join(self.data_ingestion_dir,
            training_pipeline.FILE_NAME) ## FILE_NAME defined as "sensor.csv" in the constant folder/training_pipeline
            self.train_file_path : str = os.path.join(self.data_ingestion_dir,
            training_pipeline.TRAIN_FILE_NAME) ## TRAIN_FILE_NAME defined as "sensor.csv" in the constant folder/training_pipeline
            self.test_file_path : str = os.path.join(self.data_ingestion_dir,
            training_pipeline.TEST_FILE_NAME) ## TEST_FILE_NAME defined as "sensor.csv" in the constant folder/training_pipeline

            self.train_test_split : float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name : str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

        except Exception as e:
            raise SensorException(e,sys)



class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...