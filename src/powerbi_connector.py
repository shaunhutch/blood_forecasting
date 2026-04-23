"""
Module for connecting to and retrieving data from Power BI.
"""
import requests
import pandas as pd
from typing import Optional
import logging
from config import (
    POWERBI_AUTH_URL,
    POWERBI_API_URL,
    POWERBI_CLIENT_ID,
    POWERBI_CLIENT_SECRET,
    POWERBI_DATASET_ID
)

logger = logging.getLogger(__name__)


class PowerBIConnector:
    """Connector for retrieving data from Power BI using the REST API."""
    
    def __init__(self):
        """Initialize the Power BI connector."""
        self.access_token = None
        self.authenticate()
    
    def authenticate(self) -> str:
        """
        Authenticate with Power BI using service principal credentials.
        
        Returns:
            str: Access token for API calls
        """
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': POWERBI_CLIENT_ID,
            'client_secret': POWERBI_CLIENT_SECRET,
            'resource': 'https://analysis.windows.net/powerbi/api'
        }
        
        try:
            response = requests.post(POWERBI_AUTH_URL, data=auth_data)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            logger.info('Successfully authenticated with Power BI')
            return self.access_token
        except requests.exceptions.RequestException as e:
            logger.error(f'Authentication failed: {str(e)}')
            raise
    
    def get_dataset_data(self, table_name: str, query: Optional[str] = None) -> pd.DataFrame:
        """
        Retrieve data from a Power BI dataset.
        
        Args:
            table_name: Name of the table in the dataset
            query: DAX query for filtering (optional)
        
        Returns:
            pd.DataFrame: Data from Power BI
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Note: This is a simplified example. Power BI API has limited capabilities for data export.
        # For production, consider using XMLA endpoints or exporting to CSV from Power BI.
        url = f'{POWERBI_API_URL}/datasets/{POWERBI_DATASET_ID}/executeQueries'
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # Process the response based on your Power BI structure
            logger.info(f'Successfully retrieved data from {table_name}')
            return pd.DataFrame(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to retrieve data: {str(e)}')
            raise
    
    def load_from_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load data from a CSV file (alternative to API if exporting from Power BI).
        
        Args:
            filepath: Path to the CSV file exported from Power BI
        
        Returns:
            pd.DataFrame: Data from CSV
        """
        try:
            df = pd.read_csv(filepath)
            logger.info(f'Loaded data from {filepath}')
            return df
        except Exception as e:
            logger.error(f'Failed to load CSV: {str(e)}')
            raise


def get_powerbi_data(source: str = 'csv', filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Retrieve blood type data from Power BI.
    
    Args:
        source: Data source type ('api' or 'csv')
        filepath: Path to CSV file if using CSV source
    
    Returns:
        pd.DataFrame: Blood type data with columns: date, blood_type, metric
    """
    connector = PowerBIConnector()
    
    if source == 'csv' and filepath:
        return connector.load_from_csv(filepath)
    elif source == 'api':
        return connector.get_dataset_data('BloodTypeMetrics')
    else:
        raise ValueError(f'Unknown data source: {source}')
