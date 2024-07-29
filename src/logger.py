import os 
from datetime import datetime
import logging 

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y')}.log"

logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH, level=logging.INFO,
    format='[%(asctime)s : %(levelname)s : %(message)s]'
)



if __name__ == '__main__':
    logging.info("watch out")