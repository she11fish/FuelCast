"""FastAPI application for FuelCast gasoline price forecasting"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List

from app.config import API_TITLE, API_DESCRIPTION, API_VERSION, CORS_ORIGINS
from app.models import ForecastDataPoint, MetricsResponse, FeatureImportance
from app.services.data_generator import generate_data
from app.services.model_service import model_service
from app.utils import calculate_rmse, dataframe_to_forecast_list

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data storage
historical_data: pd.DataFrame = None
forecast_data: pd.DataFrame = None


@app.on_event("startup")
async def startup_event():
    """Initialize models and data on startup"""
    global historical_data, forecast_data
    
    # Load models
    model_service.load_xgboost_model()
    model_service.load_sarimax_model()
    
    # Generate data with real model predictions
    historical_data, forecast_data = generate_data()
    print(f"✓ Generated {len(historical_data)} historical data points")
    print(f"✓ Generated {len(forecast_data)} forecast data points")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FuelCast API",
        "version": API_VERSION,
        "endpoints": {
            "/forecast": "Get historical and predicted gas prices",
            "/metrics": "Get model performance metrics",
            "/importance": "Get XGBoost feature importance",
            "/docs": "Interactive API documentation"
        }
    }


@app.get("/forecast", response_model=List[ForecastDataPoint])
async def get_forecast():
    """
    Get historical gas prices and future forecasts from SARIMA and XGBoost models
    
    Returns:
        List of data points with date, actual price, SARIMA prediction, and XGBoost prediction
    """
    combined_df = pd.concat([historical_data, forecast_data], ignore_index=True)
    return dataframe_to_forecast_list(combined_df)


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get model performance metrics and current gas price
    
    Returns:
        Dictionary with SARIMA RMSE, XGBoost RMSE, and current price
    """
    hist_df = historical_data.copy()
    
    # Calculate RMSE for both models
    sarima_rmse = calculate_rmse(hist_df['actual'], hist_df['sarima'])
    xgb_rmse = calculate_rmse(hist_df['actual'], hist_df['xgboost'])
    
    # Get current price (last actual price)
    current_price = float(hist_df['actual'].iloc[-1])
    
    return MetricsResponse(
        sarima_rmse=round(sarima_rmse, 3),
        xgboost_rmse=round(xgb_rmse, 3),
        current_price=round(current_price, 2)
    )


@app.get("/importance", response_model=List[FeatureImportance])
async def get_feature_importance():
    """
    Get XGBoost feature importance scores
    
    Returns:
        List of features with their importance scores
    """
    # Try to get real feature importance from model
    features = model_service.get_feature_importance()
    
    # Fallback to synthetic data if extraction fails
    if features is None:
        features = model_service.get_fallback_importance()
    
    return features


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
