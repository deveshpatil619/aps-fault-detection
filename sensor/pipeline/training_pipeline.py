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
    is_pipeline_running =False
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

            model_trainer_artifact = model_trainer.initiate_model_trainer() ## Initiating the model_trainer and output as model_trainer_artifact
            logging.info (f"model_trainer completed and artifacts: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)




    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,model_trainer_artifact:ModelTrainerArtifact):
        try:
            model_eval_config = ModelEvaluationConfig(training_pipeline_config = self.training_pipeline_config) ## model_evaluation_config file
            logging.info("starting the model evaluation")
            model_eval = ModelEvaluation(model_eval_config = model_eval_config, ## passing the model_eval_config and data_validation_artifact and model_trainer_artifact as input to the model_eval
            data_validation_artifact = data_validation_artifact, model_trainer_artifact = model_trainer_artifact)

            model_eval_artifact = model_eval.initiate_model_evaluation() ## Initiating the  model_evaluation and output as model_eval_artifact
            logging.info (f"model_eval completed and artifacts: {model_eval}")

            return model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys)



    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config = self.training_pipeline_config) ## model_pusher_config file
            logging.info("starting the model evaluation")
            model_pusher = ModelPusher(model_pusher_config= model_pusher_config,
            model_eval_artifact = model_eval_artifact) ## passing the model_pusher_config and model_eval_artifact as input to the model_pusher.

            model_pusher_artifact = model_pusher.initiate_model_pusher() ##Initiating the model_pusher and output as model_pusher_artifact
            logging.info(f"model_pusher completed and artifacts: {model_pusher}")

            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)

    


    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True  ## make status true when the running of pipeline will start
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact = data_transformation_artifact)
            model_eval_artifact =self.start_model_evaluation(data_validation_artifact = data_validation_artifact, model_trainer_artifact= model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact = model_eval_artifact)
            TrainPipeline.is_pipeline_running = False  ## make status false when the running of pipoeline is finished
        except Exception as e:
            TrainPipeline.is_pipeline_running = False
            raise SensorException(e, sys)











