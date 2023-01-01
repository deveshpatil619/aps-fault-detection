## Importing the important libraries

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object,write_yaml_file
from sensor.ml.model.estimator import ModelResolver
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping
import pandas  as  pd
import os,sys

class ModelEvaluation:
    def __init__(self,model_eval_config:ModelEvaluationConfig,
      data_validation_artifact:DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact):

        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_evaluation(self)->ModelEvaluationArtifact: 
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path  ##train and test files paths
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            train_df = pd.read_csv(valid_train_file_path)  ## reading the train and test files in dataframe
            test_df = pd.read_csv(valid_test_file_path)

            ## concatinating the two dataframes
            df = pd.concat([train_df,test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(),inplace=True)
            df.drop(TARGET_COLUMN,axis=1,inplace=True)






            train_model_file_path = self.model_trainer_artifact.trained_model_file_path## train_model_file_path 

            model_resolver = ModelResolver()   
            is_model_accepted = True ## initializing if the model exists or not

            if not model_resolver.is_model_exist(): ## checking if the model file exists or not and if not returnng the model_evaluation_artifact
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = None,
                    trained_model_path = train_model_file_path,
                    best_model_path= None,
                    train_model_metric_artifact= self.model_trainer_artifact.test_metric_artifact ,
                    best_model_metric_artifact=None)
                
                logging.info(f"Model_Evaluation_Artifact:{model_evaluation_artifact}")
                return model_evaluation_artifact

            ## if model exists then the model path will be as follows
            latest_model_path = model_resolver.get_best_model_path()
            train_model = load_object(file_path = train_model_file_path ) ## loading the train model

            latest_model = load_object(file_path = latest_model_path)  ## loading the latest model

            

           
            y_trained_pred = train_model.predict(df)
            y_latest_pred  = latest_model.predict(df)

            trained_metric = get_classification_score(y_true=y_true,y_pred=y_trained_pred)  ## Performance metrics for  y_trained_pred model
            latest_metric = get_classification_score(y_true=y_true,y_pred=y_latest_pred)  ## Performance metrics for  y_latest_pred model

            difference = trained_metric.f1_score - latest_metric.f1_score

            if (self.model_eval_config.change_threshold < difference):
                ##0.02 < 0.03
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = difference,
                    trained_model_path = train_model_file_path,
                    best_model_path= latest_model_path,
                    train_model_metric_artifact= trained_metric ,
                    best_model_metric_artifact= latest_metric)

            ##  creating the model_evaluation_artifact report file
            model_eval_report = model_evaluation_artifact.__dict__()

            ## saving the report
            write_yaml_file(file_path= self.model_eval_config.report_file_path, content=model_eval_report)


            logging.info(f"Model_Evaluation_Artifact:{model_evaluation_artifact}")
            return model_evaluation_artifact

            

        except Exception as e:
            raise SensorException(e,sys)


