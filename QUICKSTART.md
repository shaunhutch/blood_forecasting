# QUICK START GUIDE

## Getting Started with Blood Type Time Series Forecasting

### Step 1: Set Up Python Environment

```bash
# Navigate to the project directory
cd c:\Users\SGHUTCHI\Documents\BLOSSOM

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Power BI Connection (Optional)

If you want to use Power BI API:

1. Copy `.env.example` to `.env`:

   ```bash
   copy .env.example .env
   ```

2. Fill in your Power BI credentials:
   ```
   POWERBI_TENANT_ID=your_azure_tenant_id
   POWERBI_CLIENT_ID=your_service_principal_app_id
   POWERBI_CLIENT_SECRET=your_service_principal_secret
   POWERBI_DATASET_ID=your_dataset_id
   ```

**For now, we recommend starting with CSV exports from Power BI.**

### Step 3: Prepare Your Data

Export blood type data from Power BI with the following columns:

- `date`: Date/timestamp (YYYY-MM-DD format)
- `blood_type`: Blood type classification (O+, O-, A+, A-, B+, B-, AB+, AB-)
- `metric`: Numeric value to forecast (inventory, demand, donations, etc.)

**IMPORTANT: Data should contain Monday-Friday only (no weekends).** This is typical for blood bank operations where there's no activity on weekends.

Save as CSV and place in:

```
data/blood_type_data.csv
```

**Sample data will be auto-generated if no CSV is provided (for testing). Sample data is weekday-only.**

### Step 4: Run the Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Navigate to notebooks/ folder
# Open 01_blood_type_forecasting.ipynb
# Run all cells to generate forecasts
```

### Step 5: Review Results

Forecasts are automatically saved to the `outputs/` directory:

- `forecast_[BloodType].csv` - Full forecast with confidence intervals
- `forecast_summary_[BloodType].csv` - Next 30 days summary
- `forecast_comparison.csv` - Comparison across all blood types

## Project Structure

```
BLOSSOM/
├── data/                          # Raw data from Power BI
│   └── blood_type_data.csv       # Your exported data (create this)
├── notebooks/
│   └── 01_blood_type_forecasting.ipynb  # Main analysis notebook
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── powerbi_connector.py      # Power BI data loading
│   └── forecast.py               # Prophet forecasting logic
├── outputs/                       # Generated forecasts (auto-created)
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for credentials
└── README.md                      # Full documentation
```

## Key Features

✅ **Prophet Forecasting**

- Automatic trend and seasonality detection
- Handles missing data and outliers
- Confidence intervals included

✅ **Multi-Blood Type Analysis**

- Individual models for each blood type
- Comparative visualizations
- Side-by-side forecasts

✅ **Easy Data Integration**

- CSV export from Power BI
- Power BI REST API support (requires setup)
- Sample data generation for testing

✅ **Results Export**

- CSV exports for further analysis
- Ready for Power BI re-import
- Multiple summary formats

## ⏰ Weekday-Only Data Handling

This project is **optimized for Monday-Friday data (no weekends)**. Here's what happens automatically:

| Aspect          | Behavior                                                   |
| --------------- | ---------------------------------------------------------- |
| **Training**    | Sample data & notebook filters to weekdays only (Mon-Fri)  |
| **Seasonality** | Weekly patterns disabled (since data has gaps on weekends) |
| **Forecasting** | Forecasts generated for business days only                 |
| **Output**      | CSV results contain only Monday-Friday predictions         |

**Why?** Blood banks typically don't track/report on weekends, making weekday-only data the norm.

## Troubleshooting

### "No module named 'prophet'"

```bash
# Install prophet
pip install prophet

# On Windows, if prophet fails, try:
conda install -c conda-forge prophet
```

### "Data file not found"

The notebook will automatically generate sample data for testing. To use your own:

1. Export from Power BI as CSV
2. Place in `data/` folder
3. Ensure columns: date, blood_type, metric

### Power BI API Connection Issues

1. Verify credentials in `.env` file
2. Check service principal has appropriate Power BI permissions
3. For now, use CSV export method (recommended)

## Next Steps

1. **Load Your Data**: Replace sample data with your Power BI export
2. **Run the Forecast**: Execute the notebook to generate predictions
3. **Review Results**: Check visualizations and summaries
4. **Iterate**: Adjust Prophet parameters for better accuracy
5. **Integrate**: Export forecasts back to Power BI for dashboards

## Support

For issues or questions:

- Check [Prophet Documentation](https://facebook.github.io/prophet/)
- Review notebook comments and markdown sections
- Refer to README.md for detailed information

---

**Ready to start? Run the notebook!**

```bash
jupyter notebook notebooks/01_blood_type_forecasting.ipynb
```
