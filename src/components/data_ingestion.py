import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 
from sklearn.model_selection import train_test_split
import os 
from dataclasses import dataclass
from typing import Tuple


@dataclass
class DataInjestionConfig : 
    raw_data_path   : str = os.path.join('artifact', 'data', 'raw_data.csv')
    train_data_path : str = os.path.join('artifact', 'data', 'train.csv')
    test_data_path  : str = os.path.join('artifact', 'data', 'test.csv')

class DataInjestion :
    
    def __init__(self) -> None :
        self.data_injestion_config = DataInjestionConfig()

    def initiate_data_injestion(self) -> Tuple[str] : 
        # we need to read the data from the data folder, here you can see
        # we are in components folder we think we need to go two level up and go to data folder
        # but that is not a case now, because of configuring in setup.py the top level is src now
        # so we can only use 'data/raw_data.xlsx' for providing a path

        try : 

            logging.info('Data Injestion is initiated...')
            raw_data = pd.read_excel('data/raw_data.xlsx')

            #converting the column names into lower cases for convenience
            raw_data.columns = raw_data.columns.str.lower()

            # deleting null values and unnecessary data
            
            raw_data.drop(raw_data[(raw_data['route'].isna()) | (raw_data['total_stops'].isna())].index, inplace=True)
            raw_data.drop(raw_data[raw_data['duration'] == '5m'].index, inplace = True)
            raw_data.drop(columns='route', inplace = True)

            logging.info('Data in readed successfully...')

            target_column = 'price'
            X = raw_data[raw_data.columns[raw_data.columns != target_column]]
            y = raw_data[target_column] 

            logging.info('Data splitting is initiated...')

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.25, random_state=42
            )

            logging.info('Data is splitted...')

            # concat for make a data as train and test

            train_data = pd.concat([X_train, y_train], axis=1)
            test_data  = pd.concat([X_test, y_test], axis=1)

            os.makedirs(os.path.join(os.getcwd(), 'artifact', 'data'), exist_ok=True) #creating the artifact folder


            # raw_data_path   = os.path.join(os.getcwd(), self.data_injestion_config.raw_data_path)
            # train_data_path = os.path.join(os.getcwd(), self.data_injestion_config.train_data_path)
            # test_data_path  = os.path.join(os.getcwd(), self.data_injestion_config.test_data_path)
            
            #saving the dataset

            raw_data.to_csv(self.data_injestion_config.raw_data_path, index=False)
            train_data.to_csv(self.data_injestion_config.train_data_path, index=False)
            test_data.to_csv(self.data_injestion_config.test_data_path, index=False)

            logging.info('Data is stored in artifact folder...')

            return (self.data_injestion_config.raw_data_path, 
                self.data_injestion_config.train_data_path, 
                self.data_injestion_config.test_data_path)
            
        except Exception as e : 
            logging.error(e)
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    obj = DataInjestion()
    paths = obj.initiate_data_injestion()
    for path in paths:
        print(path)