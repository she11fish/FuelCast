"""Data models"""
from typing import Optional
from pydantic import BaseModel


class ForecastDataPoint(BaseModel):
    date: str
    actual: Optional[float] = None
    sarima: Optional[float] = None
    xgboost: Optional[float] = None


class MetricsResponse(BaseModel):
    sarima_rmse: float
    xgboost_rmse: float
    current_price: float


class FeatureImportance(BaseModel):
    feature: str
    score: float
