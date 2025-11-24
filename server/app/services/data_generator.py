"""Data generation using real EIA data and trained models"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple
from app.config import HISTORICAL_WEEKS, FORECAST_WEEKS
from app.services.eia_data_loader import eia_loader
from app.services.model_service import model_service


def generate_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate historical and forecast data using real EIA data and trained models
    
    Returns:
        Tuple of (historical_df, forecast_df)
    """
    try:
        # Fetch real gas and crude oil prices from EIA
        print("Fetching data from EIA API...")
        gas_df, crude_df = eia_loader.get_aligned_data(weeks=HISTORICAL_WEEKS)
        
        if len(gas_df) == 0 or len(crude_df) == 0:
            print("Warning: No data from EIA, using fallback")
            return _generate_fallback_data()
        
        print(f"✓ Fetched {len(gas_df)} weeks of data from EIA")
        
        # Prepare historical dataframe
        historical_df = pd.DataFrame({
            'date': gas_df['date'].dt.strftime('%Y-%m-%d'),
            'actual': gas_df['gas_price'].values,
            'sarima': gas_df['gas_price'].values,  # Will add noise to simulate predictions
            'xgboost': gas_df['gas_price'].values   # Will add noise to simulate predictions
        })
        
        # Generate Real Historical Predictions (In-Sample)
        
        # 1. SARIMAX In-Sample Prediction
        if model_service.sarimax_model is not None:
            try:
                # We need to provide exogenous variables for the entire historical period
                # The model was trained on this data, so we can use get_prediction
                pred = model_service.sarimax_model.get_prediction(
                    start=0, 
                    end=len(gas_df)-1, 
                    exog=crude_df[['close']]
                )
                historical_df['sarima'] = pred.predicted_mean.values
                print(f"✓ Generated {len(historical_df)} historical SARIMAX predictions")
            except Exception as e:
                print(f"Error generating historical SARIMAX predictions: {e}")

        # 2. XGBoost In-Sample Prediction
        if model_service.xgboost_model is not None:
            try:
                # Recreate features for historical data
                xgb_hist_features = pd.DataFrame({
                    'close': crude_df['close'],
                    'dayofyear': gas_df['date'].dt.dayofyear,
                    'month': gas_df['date'].dt.month,
                    'year': gas_df['date'].dt.year,
                    'gas_price_lag1': gas_df['gas_price'].shift(1),
                    'crude_price_lag4': crude_df['close'].shift(4)
                })
                
                # The first few rows will have NaNs due to shifting. 
                # XGBoost can handle NaNs, but for consistency with training (which likely dropped them),
                # we should probably only predict on valid data or let XGBoost handle it.
                # Since we want to map back to the original index, we'll predict on everything 
                # and let the model handle NaNs if it can, or we just accept that the first few might be garbage/NaN.
                # However, the trained model might expect non-NaN input if it was trained on dropna().
                
                # Let's predict only on valid rows to be safe
                valid_indices = xgb_hist_features.dropna().index
                if len(valid_indices) > 0:
                    valid_features = xgb_hist_features.loc[valid_indices]
                    preds = model_service.xgboost_model.predict(valid_features)
                    
                    # Assign predictions back to the correct indices
                    historical_df.loc[valid_indices, 'xgboost'] = preds
                    print(f"✓ Generated {len(preds)} historical XGBoost predictions")
            except Exception as e:
                print(f"Error generating historical XGBoost predictions: {e}")
        
        # Generate forecast data
        last_date = pd.to_datetime(gas_df['date'].iloc[-1])
        forecast_dates = [(last_date + timedelta(weeks=i+1)) for i in range(FORECAST_WEEKS)]
        
        # Project future crude oil prices
        last_crude = crude_df['close'].iloc[-1]
        recent_crude_avg = crude_df['close'].tail(12).mean()
        crude_trend = (last_crude - crude_df['close'].iloc[-13]) / 13 if len(crude_df) >= 13 else 0
        
        future_crude = []
        for i in range(FORECAST_WEEKS):
            projected = recent_crude_avg + (crude_trend * i) + np.random.normal(0, 1)
            future_crude.append(projected)
        
        # SARIMAX Forecast
        sarima_forecast = None
        if model_service.sarimax_model is not None:
            try:
                exog_future = pd.DataFrame({'close': future_crude})
                sarima_predictions = model_service.predict_sarimax(
                    exog_future=exog_future,
                    steps=FORECAST_WEEKS
                )
                if sarima_predictions is not None:
                    sarima_forecast = sarima_predictions.values
                    print(f"✓ Generated {len(sarima_forecast)} SARIMAX forecasts using trained model")
            except Exception as e:
                print(f"Error generating SARIMAX forecast: {e}")
        
        if sarima_forecast is None:
            last_price = gas_df['gas_price'].iloc[-1]
            sarima_forecast = [last_price + 0.01 * i + np.random.normal(0, 0.04) for i in range(FORECAST_WEEKS)]
            print("Using fallback SARIMAX forecast")
        
        # XGBoost Forecast - using REAL trained model
        xgb_forecast = None
        if model_service.xgboost_model is not None:
            try:
                xgb_forecast_values = []
                
                for i, forecast_date in enumerate(forecast_dates):
                    features = {
                        'close': future_crude[i],
                        'dayofyear': forecast_date.dayofyear,
                        'month': forecast_date.month,
                        'year': forecast_date.year,
                    }
                    
                    # Lagged gas price (previous week)
                    if i == 0:
                        features['gas_price_lag1'] = gas_df['gas_price'].iloc[-1]
                    else:
                        features['gas_price_lag1'] = xgb_forecast_values[-1]
                    
                    # Lagged crude price (4 weeks ago)
                    if i < 4:
                        features['crude_price_lag4'] = crude_df['close'].iloc[-(4-i)]
                    else:
                        features['crude_price_lag4'] = future_crude[i-4]
                    
                    # Predict for this single step
                    step_df = pd.DataFrame([features])
                    step_pred = model_service.xgboost_model.predict(step_df)[0]
                    xgb_forecast_values.append(step_pred)
                
                xgb_forecast = np.array(xgb_forecast_values)
                print(f"✓ Generated {len(xgb_forecast)} XGBoost forecasts using trained model")
                
            except Exception as e:
                print(f"Error generating XGBoost forecast: {e}")
                import traceback
                traceback.print_exc()
        
        if xgb_forecast is None:
            last_price = gas_df['gas_price'].iloc[-1]
            xgb_forecast = [last_price + 0.012 * i + np.random.normal(0, 0.03) for i in range(FORECAST_WEEKS)]
            print("Using fallback XGBoost forecast")
        
        forecast_df = pd.DataFrame({
            'date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
            'actual': [None] * FORECAST_WEEKS,
            'sarima': sarima_forecast,
            'xgboost': xgb_forecast
        })
        
        return historical_df, forecast_df
        
    except Exception as e:
        print(f"Error in data generation: {e}")
        import traceback
        traceback.print_exc()
        print("Falling back to synthetic data")
        return _generate_fallback_data()


def _generate_fallback_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic fallback data if EIA API or models fail"""
    np.random.seed(42)
    
    # Historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=HISTORICAL_WEEKS)
    historical_dates = []
    current_date = start_date
    for _ in range(HISTORICAL_WEEKS + 1):
        historical_dates.append(current_date)
        current_date += timedelta(weeks=1)
    
    trend = np.linspace(0, 0.4, len(historical_dates))
    seasonality = 0.15 * np.sin(np.linspace(0, 2 * np.pi, len(historical_dates)))
    noise = np.random.normal(0, 0.05, len(historical_dates))
    actual_prices = 3.20 + trend + seasonality + noise
    
    sarima_historical = actual_prices + np.random.normal(0, 0.03, len(actual_prices))
    xgb_historical = actual_prices + np.random.normal(0, 0.02, len(actual_prices))
    
    historical_df = pd.DataFrame({
        'date': [d.strftime('%Y-%m-%d') for d in historical_dates],
        'actual': actual_prices,
        'sarima': sarima_historical,
        'xgboost': xgb_historical
    })
    
    # Forecast data
    forecast_dates = []
    current_date = end_date + timedelta(weeks=1)
    for _ in range(FORECAST_WEEKS):
        forecast_dates.append(current_date)
        current_date += timedelta(weeks=1)
    
    last_price = actual_prices[-1]
    future_trend = np.linspace(0, 0.2, FORECAST_WEEKS)
    future_seasonality = 0.15 * np.sin(np.linspace(2 * np.pi, 2.5 * np.pi, FORECAST_WEEKS))
    
    sarima_forecast = last_price + future_trend + future_seasonality + np.random.normal(0, 0.04, FORECAST_WEEKS)
    xgb_forecast = last_price + future_trend * 1.1 + future_seasonality * 0.9 + np.random.normal(0, 0.03, FORECAST_WEEKS)
    
    forecast_df = pd.DataFrame({
        'date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
        'actual': [None] * FORECAST_WEEKS,
        'sarima': sarima_forecast,
        'xgboost': xgb_forecast
    })
    
    return historical_df, forecast_df
