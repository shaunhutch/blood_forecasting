# Blood Type Time Series Forecasting Project

This project forecasts blood type demand and metrics over time using data from Power BI and Facebook's Prophet forecasting library.

## Project Structure

```
├── data/                 # Raw data exports from Power BI
├── notebooks/            # Jupyter notebooks for analysis and exploration
├── src/                  # Python modules for forecasting and data processing
├── outputs/              # Generated forecasts and visualizations
├── requirements.txt      # Python dependencies
└── .env.example         # Template for environment configuration
```

## Setup Instructions

### 1. Clone/Setup Environment

```bash
cd BLOSSOM
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Power BI Connection

- Copy `.env.example` to `.env`
- Fill in your Power BI credentials:
  - TENANT_ID: Your Azure AD tenant ID
  - CLIENT_ID: Your Power BI service principal app ID
  - CLIENT_SECRET: Your Power BI service principal secret
  - DATASET_ID: Your Power BI dataset ID

### 4. Run Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to `notebooks/` and start with `01_data_exploration.ipynb`

## Data Format

Expected columns in Power BI data:

- `date`: Timestamp of the record (YYYY-MM-DD format)
- `blood_type`: Blood type classification (O+, O-, A+, A-, B+, B-, AB+, AB-)
- `metric`: Numeric value to forecast (inventory, demand, donations, etc.)
- Any additional grouping columns (location, facility, etc.)

**Important:** This project is optimized for **weekday-only data (Monday-Friday)**. The system automatically:

- Excludes weekends from model training
- Disables weekly seasonality patterns in Prophet (since data lacks weekends)
- Filters forecasts to weekdays only
- Generates forecasts for the next N business days

If your data includes weekends, it will still work but may produce less accurate results.

## Forecasting Workflow

1. **Data Exploration**: Analyze historical trends by blood type
2. **Data Preparation**: Clean and aggregate data for forecasting
3. **Model Training**: Fit Prophet models for each blood type
4. **Forecasting**: Generate future predictions
5. **Visualization**: Plot results and export forecasts

## Key Features

- **Automatic weekday handling**: Optimized for Monday-Friday data, automatically excludes weekends
- **Automatic handling of multiple blood types**: Individual models per blood type
- Prophet's built-in seasonality detection (yearly patterns)
- Confidence intervals for uncertainty quantification
- Business day forecasting (next N weekdays only)
- Exportable forecast results as CSV/JSON
- Visualization of historical vs. forecasted data

## Dependencies

- **pandas**: Data manipulation
- **prophet**: Time series forecasting
- **requests**: Power BI API calls
- **python-dotenv**: Environment configuration management
- **matplotlib/seaborn**: Data visualization
- **scikit-learn**: Additional ML utilities

## Notes

- Prophet handles missing data and irregular time series well
- Each blood type is modeled independently for more accurate forecasts
- Adjust Prophet hyperparameters (seasonality_mode, interval_width) in the forecast module as needed
- Consider external regressors (holidays, events) if needed

## Notes

### Weekday-Only Data Handling

This project is optimized for **Monday-Friday data only** (typical for blood bank operations). The system automatically:

- **Filters training data** to weekdays only during model preparation
- **Disables weekly seasonality** in Prophet (since the data inherently lacks weekend patterns)
- **Excludes weekends from forecasts** in the output CSV files
- **Forecasts business days only** when you request 30-day forecasts (≈21-22 actual weekdays)

If your Power BI data includes weekends, the system will still work but may produce less accurate results. Consider filtering to weekdays before exporting from Power BI.

### Prophet Parameters

- **Yearly Seasonality**: Enabled (captures annual patterns like donation drives, holiday effects)
- **Weekly Seasonality**: Disabled (data is weekdays-only, so no weekly pattern exists)
- **Daily Seasonality**: Disabled (typically not relevant for daily-aggregated blood bank data)
- **Confidence Interval**: 80% (balances precision with practical decision-making)

Adjust these in `src/forecast.py` if needed for your specific use case.

## Author

Created for blood donation/inventory forecasting
