import sys
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
import streamlit as st
from src.utils import load_object, get_transformed_df
from src.exception import CustomException
from src.logger import logging
from src.pipeline.predict_pipeline import CustomDataObject
from datetime import datetime


airlines = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
        'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
        'Vistara Premium economy', 'Jet Airways Business',
        'Multiple carriers Premium economy', 'Trujet']

sources = ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
destinations = ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad']
total_stops_list = ['non-stop', '2 stops', '1 stop', '3 stops', '4 stops']


additional_infos = ['No info', 'In-flight meal not included',
                'No check-in baggage included', '1 Short layover', 'No Info',
                '1 Long layover', 'Change airports', 'Business class',
                'Red-eye flight', '2 Long layover']


@st.cache_resource
def load_preprocessor_and_model():
    preprocessor: ColumnTransformer = load_object('artifact/model/preprocessor.pkl')
    model: BaseEstimator = load_object('artifact/model/regressor.pkl')

    return preprocessor, model

def main() -> None:
    st.set_page_config(page_title='flight-fare-prediction',
                       initial_sidebar_state='collapsed')
    
    st.title('Flight Fare Prediction')

    preprocessor, model = load_preprocessor_and_model()
    # st.latex(preprocessor)
    # st.latex(model)

    with st.form(key='form', border=True):
        col1, col2 = st.columns(2)

        airline: str = col1.selectbox('Airlines', options=airlines)
        source: str = col1.selectbox('Source', options=sources)
        destination: str = col1.selectbox('Destination', destinations)
        total_stops: str = col1.selectbox('Total stops', total_stops_list)

        date_of_journey: str = col2.date_input('Date of Journey', min_value=datetime(2019, 1, 1), max_value=datetime(2019, 6,30))
        duration: str = col2.text_input('Duration',placeholder='2h 15m')
        arrival_time: str = col2.text_input('Arrival time', placeholder='02:50')
        dep_time: str = col2.text_input('Departure time', placeholder='22:50')

        additional_info:str = st.selectbox('Additional Info', additional_infos)

        button = st.form_submit_button('Predict', type='primary', use_container_width=True)
    
    if button:

        if not all([duration, dep_time, arrival_time]):
            st.error('All fields are required..')
            st.stop()
       
        obj = CustomDataObject(airline, source, destination, additional_info, total_stops,
                               date_of_journey, duration, arrival_time, dep_time)

        try : 
            X = obj.get_data_as_frame()
            transformed_X = get_transformed_df(preprocessor.transform(X))
            
            res = model.predict(transformed_X)

            st.title(f'The Approximate Fare of this flight is:  {res[0]: .2f}')
        
        except Exception as e:
            logging.error(e)
            st.error('Give values in the correct format')
            # raise CustomException(e, sys)
            

    

if __name__ == '__main__':
    main()
