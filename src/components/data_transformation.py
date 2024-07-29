import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd 
from dataclasses import dataclass
import os
from src import utils
import pickle


@dataclass
class DataTransformationConfig : 
    preprocessor_file_path = os.path.join('artifact', 'model', 'preprocessor.pkl')

class DataTransformation :

    def __init__(self) -> None:
        self.file_path = DataTransformationConfig()

    
    def get_transformer_object(self) -> ColumnTransformer :
        
        categorical_columns = ['airline', 'source', 'destination']

        additional_info_pipeline = Pipeline(
            steps=[
                ('lower', FunctionTransformer(utils.get_additional_info)),
                ('encode', OrdinalEncoder())
                ]
            )
        
        transformer = ColumnTransformer(
                transformers=[
                    ('travel_info', OrdinalEncoder(), categorical_columns),
                    ('additional_info', additional_info_pipeline, 'additional_info'),
                    ('duration', FunctionTransformer(utils.convert_duration), 'duration'),
                    ('total_stops', FunctionTransformer(utils.convert_total_stops), 'total_stops'),
                    ('date_features', FunctionTransformer(utils.extract_day_and_month), 'date_of_journey'),
                    ('arrival_info', FunctionTransformer(utils.get_arrival_info), 'arrival_time'),
                    ('departure_info', FunctionTransformer(utils.get_departure_info), 'dep_time'),
                ],
                remainder='passthrough' 
        )

        return transformer


    def initiate_data_transformation(self):

        #read the injected data

        logging.info('Data is readed for transformation...')

        train_data = pd.read_csv('artifact/data/train.csv')
        test_data  = pd.read_csv('artifact/data/test.csv')

        #creating dir for models

        os.makedirs(os.path.join(os.getcwd(), 'artifact', 'model'), exist_ok=True)

        try :
            logging.info('Transformer is loaded...')

            transformer = self.get_transformer_object()

            logging.info('Transformation is initiated...')
            transformed_train_array = transformer.fit_transform(train_data)
            transformed_test_array  = transformer.transform(test_data)
            logging.info('Data transformation is completed...')


            logging.info('Transformed Data is saved...')
            utils.save_object(self.file_path.preprocessor_file_path, transformer)
            logging.info('model saved...')
        
            return (utils.get_transformed_df(transformed_train_array),
                    utils.get_transformed_df(transformed_test_array), 
                    self.file_path.preprocessor_file_path)

        except Exception as e :
            logging.error(e)
            raise CustomException(e, sys)
            
    

if __name__ == '__main__':
    obj = DataTransformation()
    train_arr, test_arr, _ = obj.initiate_data_transformation()

    print(train_arr.head(5))
    print('='*100)
    print(test_arr.head(5))








