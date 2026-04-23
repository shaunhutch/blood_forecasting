"""
Time series forecasting module using Facebook's Prophet.
"""
import pandas as pd
import numpy as np
from prophet import Prophet
from typing import Dict, Tuple
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class BloodTypeForecaster:
    """Forecaster for blood type metrics using Prophet.
    
    Note: Designed for weekday-only data (Monday-Friday). 
    Weekends are automatically excluded from forecasts.
    """
    
    def __init__(self, forecast_horizon: int = 30, seasonality_mode: str = 'additive', 
                 weekdays_only: bool = True):
        """
        Initialize the forecaster.
        
        Args:
            forecast_horizon: Number of days to forecast ahead
            seasonality_mode: 'additive' or 'multiplicative'
            weekdays_only: If True, input data is Mon-Fri only and forecasts will be filtered to weekdays
        """
        self.forecast_horizon = forecast_horizon
        self.seasonality_mode = seasonality_mode
        self.weekdays_only = weekdays_only
        self.models: Dict[str, Prophet] = {}
        self.forecasts: Dict[str, pd.DataFrame] = {}
        self.weekday_forecasts: Dict[str, pd.DataFrame] = {}  # Forecasts filtered to weekdays only
    
    def prepare_data(self, df: pd.DataFrame, blood_type: str) -> pd.DataFrame:
        """
        Prepare data for Prophet.
        
        Args:
            df: Input dataframe with 'date' and metric columns
            blood_type: Blood type to filter for
        
        Returns:
            pd.DataFrame: Data formatted for Prophet (columns: ds, y)
        """
        # Filter for specific blood type
        blood_df = df[df['blood_type'] == blood_type].copy()
        
        # Prepare for Prophet: rename columns to ds (datetime) and y (metric)
        blood_df['ds'] = pd.to_datetime(blood_df['date'])
        blood_df['y'] = blood_df['metric']
        
        # Sort by date
        blood_df = blood_df.sort_values('ds').reset_index(drop=True)
        
        # Remove duplicates (keep first occurrence)
        blood_df = blood_df.drop_duplicates(subset=['ds'], keep='first')
        
        logger.info(f'Prepared data for {blood_type}: {len(blood_df)} records')
        
        return blood_df[['ds', 'y']]
    
    def fit_model(self, df: pd.DataFrame, blood_type: str) -> Prophet:
        """
        Fit a Prophet model for a specific blood type.
        
        Args:
            df: Input dataframe (must have 'date' and 'metric' columns)
            blood_type: Blood type to model
        
        Returns:
            Prophet: Fitted model
        """
        # Prepare data
        train_df = self.prepare_data(df, blood_type)
        
        if len(train_df) < 3:
            logger.warning(f'Insufficient data for {blood_type}: only {len(train_df)} records')
            return None
        
        # Initialize and fit Prophet model
        # Note: Disable weekly seasonality for weekday-only data
        # Prophet will still capture yearly patterns and trends
        model = Prophet(
            seasonality_mode=self.seasonality_mode,
            yearly_seasonality=True,
            weekly_seasonality=not self.weekdays_only,  # Disable if data is weekdays-only
            daily_seasonality=False,
            interval_width=0.80
        )
        
        try:
            logger_prophet = logging.getLogger('prophet')
            prev_state = logger_prophet.disabled
            logger_prophet.disabled = True

            try:
                model.fit(train_df)
            finally:
                logger_prophet.disabled = prev_state
            logger.info(f'Successfully fitted model for {blood_type}')
            self.models[blood_type] = model
            return model
        except Exception as e:
            logger.error(f'Failed to fit model for {blood_type}: {str(e)}')
            return None
    
    def forecast(self, blood_type: str) -> pd.DataFrame:
        """
        Generate forecast for a specific blood type.
        
        Args:
            blood_type: Blood type to forecast
        
        Returns:
            pd.DataFrame: Forecast with columns including yhat, yhat_lower, yhat_upper
                         If weekdays_only=True, only weekday rows are included
        """
        if blood_type not in self.models:
            logger.error(f'No model found for {blood_type}')
            return None
        
        model = self.models[blood_type]
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=self.forecast_horizon)
        
        # Make forecast
        logger_prophet = logging.getLogger('prophet')
        prev_state = logger_prophet.disabled
        logger_prophet.disabled = True

        try:
            forecast_df = model.predict(future)
        finally:
            logger_prophet.disabled = prev_state
        
        # Filter to weekdays only if configured
        if self.weekdays_only:
            forecast_df['dayofweek'] = forecast_df['ds'].dt.dayofweek
            forecast_df = forecast_df[forecast_df['dayofweek'] < 5].copy()  # Mon=0, Fri=4
            forecast_df = forecast_df.drop('dayofweek', axis=1)
            self.weekday_forecasts[blood_type] = forecast_df
        
        self.forecasts[blood_type] = forecast_df
        logger.info(f'Generated forecast for {blood_type}')
        
        return forecast_df
    
    def forecast_all_blood_types(self, df: pd.DataFrame, blood_types: list) -> Dict[str, pd.DataFrame]:
        """
        Fit models and generate forecasts for all blood types.
        
        Args:
            df: Input dataframe with blood type data
            blood_types: List of blood types to forecast
        
        Returns:
            Dict: Dictionary of forecasts by blood type
        """
        all_forecasts = {}
        
        for blood_type in blood_types:
            logger.info(f'Processing {blood_type}...')
            
            # Fit model
            self.fit_model(df, blood_type)
            
            # Generate forecast
            if blood_type in self.models:
                forecast_df = self.forecast(blood_type)
                if forecast_df is not None:
                    all_forecasts[blood_type] = forecast_df
        
        return all_forecasts
    
    def get_forecast_summary(self, blood_type: str, days_ahead: int = 7) -> pd.DataFrame:
        """
        Get summary of forecast for next N days.
        
        Args:
            blood_type: Blood type to summarize
            days_ahead: Number of days to include in summary
        
        Returns:
            pd.DataFrame: Summary with date, point forecast, and confidence interval
        """
        if blood_type not in self.forecasts:
            logger.error(f'No forecast found for {blood_type}')
            return None
        
        forecast_df = self.forecasts[blood_type]
        future_forecast = forecast_df.tail(days_ahead)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        future_forecast = future_forecast.rename(columns={
            'ds': 'date',
            'yhat': 'forecast',
            'yhat_lower': 'lower_bound',
            'yhat_upper': 'upper_bound'
        })
        
        return future_forecast.reset_index(drop=True)
    
    def save_forecasts(self, output_path: str):
        """
        Save all forecasts to CSV files.
        
        Args:
            output_path: Directory to save forecast files
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for blood_type, forecast_df in self.forecasts.items():
            filename = f'forecast_{blood_type.replace("+", "pos").replace("-", "neg")}.csv'
            filepath = output_dir / filename
            forecast_df.to_csv(filepath, index=False)
            logger.info(f'Saved forecast to {filepath}')
    
    def get_model_metrics(self, blood_type: str) -> Dict:
        """
        Get basic metrics about the fitted model.
        
        Args:
            blood_type: Blood type to get metrics for
        
        Returns:
            Dict: Model metrics and parameters
        """
        if blood_type not in self.models:
            return None
        
        model = self.models[blood_type]
        
        return {
            'blood_type': blood_type,
            'seasonality_mode': self.seasonality_mode,
            'parameters': {
                'seasonality_prior_scale': model.seasonality_prior_scale,
                'seasonality_mode': model.seasonality_mode,
                'yearly_seasonality': model.yearly_seasonality,
                'weekly_seasonality': model.weekly_seasonality
            }
        }
