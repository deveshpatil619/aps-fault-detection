## importing the modules
import sys,os
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config.mo
from sensor.utils import get_collections_as_dataframe
from sensor.entity.config_entity import DataIngestionConfig




if __name__ == "__main__":
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())

    except Exception as e:
        print(e)


