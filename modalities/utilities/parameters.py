import os 
from dotenv import load_dotenv

load_dotenv()

RAW_DATA = os.environ.get('RAWDATA')
ANALYSIS_DATA = os.environ.get('ANALYSIS_DATA')