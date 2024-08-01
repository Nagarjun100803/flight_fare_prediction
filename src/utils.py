import pickle
import numpy as np
import pandas as pd 
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor



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
                                        'arrival_hour','arrival_minute', 'departure_hour' ,'departure_minute'
                                        ])
    return transformed_df.astype(int)

def evaluate_models(X_train, X_test, y_train, y_test) -> dict :

        models = {

        'Linear Regression': LinearRegression(),
        'Lasso': Lasso(),
        'Ridge': Ridge(),
        'Decision Tree Regressor' : DecisionTreeRegressor(),
        'Random Forest Regressor' : RandomForestRegressor()
        }


        params = {

            'Linear Regression' : {},
            'Decision Tree Regressor' : {
                'criterion' : ['squared_error', 'absolute_error'],
            },
            'Ridge' : {
                'alpha' : [.0001, .001, .01, 1, 10]
            },
            'Lasso' : {
                'alpha' : [.0001, .001, .01, 1, 10]
            },
            'Random Forest Regressor' : {
                'criterion' : ['squared_error', 'absolute_error']
            }
        }   

    
        reports = {}
    
        for estimator_name, estimator in models.items():
            est: BaseEstimator = estimator
            print(f"Model {estimator_name} is taken")
            grid = GridSearchCV(est, 
                                param_grid=params[estimator_name],
                                scoring='neg_mean_squared_error', 
                                verbose=3, cv=2)
            grid.fit(X_train, y_train)

            est.set_params(**grid.best_params_)

            est.fit(X_train, y_train)

            train_score = est.score(X_train, y_train)
            test_score  = est.score(X_test, y_test)

            print(f'{estimator_name} is train score is {round(train_score*100, 2)}')
            print(f'{estimator_name} is test score is {round(test_score*100, 2)}')

            print('\n')
            print('='*100)
            
            reports[estimator_name] = {'train_score':round(train_score*100, 6), 'test_score': round(test_score*100, 6), 
                                    'params': grid.best_params_, 'estimator': est}
    
        return reports
    

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

