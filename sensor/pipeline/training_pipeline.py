import os,sys
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from sensor.entity.config_entity import ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact,ModelTrainerArtifact
from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher




class TrainPipeline:

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        
        self.training_pipeline_config = training_pipeline_config


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config) ## data_ingestion_config file
            logging.info("starting the data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config) ## passing the data_ingestion_config to data_ingestion
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion() ## data_ingestion_artifact we got the output
            logging.info (f"data ingestion completed and artifacts: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)



    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)  ## data_validation_config file
            logging.info("starting the data validation")
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
            data_validation_config = data_validation_config) ## passing the data_ingestion_artifact and data_validation_config to data_validation
            
            data_validation_artifact = data_validation.initiate_data_validation() ## data_validation_artifact we got output
            logging.info (f"data validation completed and artifacts: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)





    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config) ## data_transformation_config file
            logging.info("starting the data transformation")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config) ## passing the data_transformation_config and data_validation_artifact to data_validation

            data_transformation_artifact = data_transformation.initiate_data_transformation() ## Initiating the data_transformation stage and data_transformation_artifact we got as output.
            logging.info (f"data transformation completed and artifacts: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)


    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config) ##model_trainer_config file
            logging.info("starting the model traning")
            model_trainer = ModelTrainer(model_trainer_config = model_trainer_config, 
            data_transformation_artifact = data_transformation_artifact)  ## passing the model_trainer_config and data_transformation_artifact as input to the model_trainer

            model_trainer_artifact = model_trainer.initiate_model_trainer() ## Initiating the model_trainer and output as Modeltrainerartifact
            logging.info (f"model_trainer completed and artifacts: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)




        
    def start_model_evaluation(self,DataT):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    


    def run_pipeline(self):
        try:

            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise SensorException(e, sys)











