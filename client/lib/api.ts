const API_BASE_URL = "http://localhost:8000";

export interface ForecastDataPoint {
  date: string;
  actual: number | null;
  sarima: number | null;
  xgboost: number | null;
}

export interface Metrics {
  sarima_rmse: number;
  xgboost_rmse: number;
  current_price: number;
}

export interface FeatureImportance {
  feature: string;
  score: number;
}

export async function fetchForecastData(): Promise<ForecastDataPoint[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/forecast`);
    if (!response.ok) {
      throw new Error(`Failed to fetch forecast data: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching forecast data:", error);
    throw error;
  }
}

export async function fetchMetrics(): Promise<Metrics> {
  try {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) {
      throw new Error(`Failed to fetch metrics: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching metrics:", error);
    throw error;
  }
}

export async function fetchFeatureImportance(): Promise<FeatureImportance[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/importance`);
    if (!response.ok) {
      throw new Error(`Failed to fetch feature importance: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching feature importance:", error);
    throw error;
  }
}
