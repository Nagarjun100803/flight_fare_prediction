import pandas as pd 
from dataclasses import dataclass
from typing import Literal



@dataclass
class CustomDataObject:
    airline: Literal['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
        'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
        'Vistara Premium economy', 'Jet Airways Business',
        'Multiple carriers Premium economy', 'Trujet']

    source: Literal['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
    destination: Literal['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad']
    additional_info: Literal['No info', 'In-flight meal not included',
                'No check-in baggage included', '1 Short layover', 'No Info',
                '1 Long layover', 'Change airports', 'Business class',
                'Red-eye flight', '2 Long layover']
    total_stops: Literal['non-stop', '2 stops', '1 stop', '3 stops', '4 stops']
    date_of_journey: str
    duration: str 
    arrival_time: str
    dep_time: str


    def get_data_as_frame(self) -> pd.DataFrame:
        data = {
            'airline': [self.airline],
            'source': [self.source],
            'destination': [self.destination],
            'additional_info': [self.additional_info],
            'total_stops': [self.total_stops],
            'duration': [self.duration],
            'arrival_time': [self.arrival_time],
            'dep_time': [self.dep_time],
            'date_of_journey': [self.date_of_journey]
        }

        return pd.DataFrame(data)




