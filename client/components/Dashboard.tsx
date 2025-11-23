"use client";

import { useEffect, useState } from "react";
import { TimeRangeSelector, type TimeRange } from "./TimeRangeSelector";
import { KPICards } from "./KPICards";
import { ForecastChart } from "./ForecastChart";
import { FeatureImportance } from "./FeatureImportance";
import {
  fetchForecastData,
  fetchMetrics,
  fetchFeatureImportance,
  type ForecastDataPoint,
  type Metrics,
  type FeatureImportance as FeatureImportanceType,
} from "@/lib/api";
import { Loader2, AlertCircle } from "lucide-react";

export function Dashboard() {
  const [timeRange, setTimeRange] = useState<TimeRange>("all");
  const [forecastData, setForecastData] = useState<ForecastDataPoint[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [featureImportance, setFeatureImportance] = useState<FeatureImportanceType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [forecast, metricsData, importance] = await Promise.all([
          fetchForecastData(),
          fetchMetrics(),
          fetchFeatureImportance(),
        ]);
        setForecastData(forecast);
        setMetrics(metricsData);
        setFeatureImportance(importance);
      } catch (err) {
        console.error("Error loading dashboard data:", err);
        setError(
          "Failed to load data. Make sure the FastAPI backend is running at http://localhost:8000"
        );
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filter data based on time range
  const filteredData = forecastData.filter((point) => {
    if (timeRange === "all") return true;
    if (timeRange === "forecast") return point.actual === null;
    if (timeRange === "last-year") {
      const pointDate = new Date(point.date);
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      return pointDate >= oneYearAgo;
    }
    return true;
  });

  // Get predicted price (first future data point with XGBoost value)
  const predictedPrice = forecastData.find(
    (point) => point.actual === null && point.xgboost !== null
  )?.xgboost || null;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="glass-strong rounded-xl p-8 max-w-md text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Connection Error</h3>
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
      <KPICards metrics={metrics} predictedPrice={predictedPrice} />
      <ForecastChart data={filteredData} />
      <FeatureImportance data={featureImportance} />
    </div>
  );
}
