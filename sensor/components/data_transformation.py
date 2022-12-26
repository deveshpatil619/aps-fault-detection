## Importing the important libraries

import os,sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import(DataTransformationArtifact,DataValidationArtifact)

from sensor.entity.config_entity import DataTransformationConfig
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data,save_object


from sensor.exception import SensorException
from sensor.logger import logging

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
    data_transformation_config: DataTransformationConfig):
        """
        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """

        try:
                self.data_validation_artifact = data_validation_artifact
                self.data_transformation_config = data_transformation_config  
            
        except Exception as e:
            raise SensorException(e,sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)




    @classmethod
    def get_data_transformer_object(cls)->Pipeline:  ##this method will give output as pipeline
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant",fill_value=0)  ## filling the missing values with 0

            preprocessor = Pipeline(
                steps=[
                    ("Imputer",simple_imputer),  ## first we will fill the missing values with 0
                    ("Robust_scaler",robust_scaler)  ## then we will apply the robust scaler
                ]
            )
            return preprocessor

        except Exception as e:
            raise SensorException(e,sys) from e 

            
    def initiate_data_transformation(self,)->DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_data_transformer_object()

            ## This is for the training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1) ## dropping the target_column in train_df
            target_feature_train_df = train_df[TARGET_COLUMN]  ## taking the target column only
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())  ## mapping the positive and negative of to 0 and 1

            ## For the testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1) ## dropping the target_column in test_df
            target_feature_test_df = test_df[TARGET_COLUMN] ## taking the target column only
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict()) ## mapping the positive and negative of to 0 and 1


            preprocessor_object = preprocessor.fit(input_feature_train_df)  ## creating the pre_processor object
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority") ## using the SMOTETomek to balance the datasets

            input_feature_train_final,target_feature_train_final = smt.fit_resample(transformed_input_train_feature,
            target_feature_train_df)

            input_feature_test_final,target_feature_test_final = smt.fit_resample(transformed_input_test_feature,
            target_feature_test_df)

            ### concatinating the traing and testing arrays

            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]

            ## save numpy array data

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)

            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array = test_arr)

            ## saving the object
            
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            ## creating the data_transformation_artifacts

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path

            )
            
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys) from e














