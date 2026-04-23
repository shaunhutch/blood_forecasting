"""
Configuration module for Power BI and forecasting settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Power BI Configuration
POWERBI_TENANT_ID = os.getenv('POWERBI_TENANT_ID')
POWERBI_CLIENT_ID = os.getenv('POWERBI_CLIENT_ID')
POWERBI_CLIENT_SECRET = os.getenv('POWERBI_CLIENT_SECRET')
POWERBI_DATASET_ID = os.getenv('POWERBI_DATASET_ID')

# Power BI API endpoints
POWERBI_AUTH_URL = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(POWERBI_TENANT_ID)
POWERBI_API_URL = 'https://api.powerbi.com/v1.0/myorg'

# Forecasting Configuration
FORECAST_HORIZON = 30  # Days ahead to forecast
SEASONALITY_MODE = 'additive'  # 'additive' or 'multiplicative'
INTERVAL_WIDTH = 0.80  # 80% confidence interval

# Blood Types
BLOOD_TYPES = ['A Neg', 'A Pos', 'AB Neg', 'AB Pos', 'B Neg', 'B Pos', 'O Neg', 'O Pos']

# Data paths
DATA_PATH = './data'
OUTPUT_PATH = './outputs'

# Logging
LOG_LEVEL = 'INFO'
