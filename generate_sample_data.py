# Sample Data Generator
# 
# This script creates sample blood type data for testing the forecasting pipeline.
# The generated data includes realistic trends, seasonality, and noise.

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def generate_sample_data(output_path='./data/blood_type_data.csv', 
                         start_date='2023-01-01',
                         end_date='2024-12-31',
                         seed=42):
    """
    Generate sample blood type data with realistic patterns.
    
    Parameters:
    -----------
    output_path : str
        Where to save the CSV file
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    seed : int
        Random seed for reproducibility
    """
    np.random.seed(seed)
    
    # Blood types
    blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    
    # Create date range - WEEKDAYS ONLY (Monday-Friday)
    # This matches typical blood bank operations (no weekend data)
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = all_dates[all_dates.dayofweek < 5]  # Monday=0, Friday=4
    
    # Generate data for each blood type
    data = []
    for bt in blood_types:
        # Different base level for each blood type (reflecting real-world demand)
        base_level = np.random.uniform(80, 150)
        
        # Trend component (slight increase or decrease over time)
        trend = np.linspace(0, np.random.uniform(-20, 20), len(dates))
        
        # Seasonality component (yearly pattern - higher in winter, lower in summer)
        seasonality = 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365.25)
        
        # Weekly pattern (some types peak on certain days)
        weekly = 8 * np.sin(np.arange(len(dates)) * 2 * np.pi / 7)
        
        # Random noise
        noise = np.random.normal(0, 5, len(dates))
        
        # Combine components
        metric = base_level + trend + seasonality + weekly + noise
        
        # Ensure non-negative values and realistic ranges
        metric = np.maximum(metric, 10)  # Minimum 10 units
        metric = np.minimum(metric, 300)  # Maximum 300 units (cap outliers)
        
        # Create records for this blood type
        for i, date in enumerate(dates):
            data.append({
                'date': date.date(),
                'blood_type': bt,
                'metric': round(metric[i], 2)
            })
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"✓ Sample data generated successfully!")
    print(f"  - Output: {output_path}")
    print(f"  - Records: {len(df)}")
    print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  - Blood types: {df['blood_type'].nunique()}")
    print(f"\nData sample:")
    print(df.head(10))
    
    return df


if __name__ == '__main__':
    # Generate sample data
    df = generate_sample_data()
    
    # Show basic statistics
    print(f"\nData Summary by Blood Type:")
    print(df.groupby('blood_type')['metric'].describe().round(2))
