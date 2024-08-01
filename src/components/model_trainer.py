import os
import sys
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from sklearn.base import BaseEstimator
from src import utils



@dataclass
class ModelTrainerConfig:
    model_path : str = os.path.join('artifact', 'model', 'regressor.pkl')

class ModelTrainer:
    def __init__(self) -> None :
        self.file_path = ModelTrainerConfig()

    
    def initiate_model_trainer(self, train_df: pd.DataFrame, test_df: pd.DataFrame):

        target_column = 'price'
        X_train = train_df[train_df.columns[train_df.columns != target_column]]
        y_train = train_df[target_column]

        X_test = test_df[train_df.columns[train_df.columns != target_column]]
        y_test = test_df[target_column]

        try : 
            
            logging.info('Model Training is Initiated...')
            reports =  utils.evaluate_models(X_train, X_test, y_train, y_test)

            max_test_score = max([model['test_score'] for model in list(reports.values())])
            
            best_model: BaseEstimator = [model['estimator'] for model in list(reports.values()) if model['test_score'] == max_test_score][0]

            print(best_model)

            logging.info('Saving the best Estimator/Model...')
            utils.save_object(self.file_path.model_path, best_model) #Saving the best model...
        
            y_pred_train = best_model.predict(X_train)
            y_pred_test  = best_model.predict(X_test)


            mse = mean_squared_error(y_train, y_pred_train), mean_squared_error(y_test, y_pred_test)
            res  = f"The MSE for train data is {mse[0]} and for test data is {mse[1]}"

            logging.info(res)
            print(res)

            return mse
        

        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

    

if __name__ == '__main__':

    obj = DataTransformation()
    train_df, test_df, _ = obj.initiate_data_transformation()

    mt = ModelTrainer()
    mse = mt.initiate_model_trainer(train_df, test_df)


        
