import pickle
import numpy as np
import pandas as pd 
from sklearn.compose import ColumnTransformer



def save_object(file_path:str, obj) : 
    
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file, protocol=5)

def load_object(file_path: str):

    with open(file_path, 'rb') as file :
        return pickle.load(file)


def get_transformed_df(array: np.ndarray):

    transformed_df = pd.DataFrame(array,
                                columns=['airline', 'source', 'destination', 'additional_info', 
                                        'duration', 'total_stops', 'journey_day', 'journey_month',
                                        'arrival_hour','arrival_minute', 'departure_hour' ,'departure_minute',
                                        'price'])
    return transformed_df.astype(int)
    
def extract_day_and_month(X: pd.Series) : 
    X = X.astype('datetime64[ns]')
    return pd.DataFrame(
        {
            'journey_day' : X.dt.day,
            'journey_month' : X.dt.month
        }
    )

def calculate_duration_in_minutes(duration:str) -> int :
    time = duration.split(' ')

    if len(time) != 1 :
        return int(time[0].replace('h', '')) * 60 + int(time[1].replace('m', ''))
    
    return int(time[0].replace('h', '')) * 60



def convert_duration(X: pd.Series) : 
    return X.apply(calculate_duration_in_minutes).values.reshape(-1,1)



def convert_total_stops(X: pd.Series) : 
    return X.map({'non-stop':0, '1 stop':1, 
                        '2 stops':2, '3 stops':3, '4 stops':4}).values.reshape(-1,1)



def get_arrival_info(X: pd.Series):
    hour_and_minutes = X.str.split(' ').str[0].str.split(':')
    return pd.DataFrame(
        {
            'arrival_hour' : hour_and_minutes.str[0].astype(int),
            'arrival_minute' : hour_and_minutes.str[1].astype(int)
        }
    )


def get_departure_info(X: pd.Series) :
    hour_and_minutes = X.str.split(':')
    return pd.DataFrame(
        {    
            'departure_hour' : hour_and_minutes.str[0].astype(int),
            'departure_minute' : hour_and_minutes.str[1].astype(int)
        }
    )


def get_additional_info(X: pd.Series): 
    return X.str.lower().values.reshape(-1,1)

