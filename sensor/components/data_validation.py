## importing the libraries

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd


class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
    data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  ## reading the schema file_path



        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            
            number_of_columns = self._schema_config["columns"]  ## length of columns we will get from schema
            if len(dataframe.columns)==number_of_columns:  ## comparing the dataframe columns and the number_of_columns
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_column_exist(self,dataframe = pd.DataFrame)-> bool:
        try:

            numerical_columns = self._schema_config['numerical_columns'] ## length of numerical_columns we will get from schema
            dataframe_columns = dataframe.columns  ## columns from the 


            for num



    @staticmethod
    def read_data(file_path)-> pd.DataFrame:  ## output of the file_read should be in dataframe format
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise  SensorException(e,sys)


    def detect_dataset_drift():
        pass

    def initiate_data_validation(self) -> DataIngestionArtifact :
        try:
            error_message =""
            train_file_path = self.data_ingestion_artifact.trained_file_path ## we need to take the trained and test file paths from data_ingestion_artifacts
            test_file_path = self.data_ingestion_artifact.test_file_path  ## we need to take the trained and test file paths from data_ingestion_artifacts
            
            ## reading the data from the train and test files locations
            train_dataframe = DataValidation.read_data(train_file_path) ## calling the  @static_method read_data
            test_dataframe  = DataValidation.read_data(test_file_path) ##calling the  @static_method read_data

            ## validate the number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe doennot contain all columns"

        except Exception as e:
            raise SensorException(e,sys)
