import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { formatCurrency, formatDate } from "@/lib/utils";
import type { ForecastDataPoint } from "@/lib/api";

interface ForecastChartProps {
  data: ForecastDataPoint[];
}

export function ForecastChart({ data }: ForecastChartProps) {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-strong rounded-lg p-4 shadow-xl">
          <p className="text-sm font-semibold mb-2">{formatDate(label)}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {formatCurrency(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-strong rounded-xl p-6 mb-8 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 gradient-text">Gasoline Price Forecast</h2>
      <ResponsiveContainer width="100%" height={450}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ffffff" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#ffffff" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorSarima" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(217, 91%, 60%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(217, 91%, 60%)" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorXGBoost" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            stroke="rgba(255,255,255,0.5)"
            style={{ fontSize: "12px" }}
          />
          <YAxis
            tickFormatter={(value) => `$${value.toFixed(2)}`}
            stroke="rgba(255,255,255,0.5)"
            style={{ fontSize: "12px" }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: "20px" }}
            iconType="line"
          />
          <Line
            type="monotone"
            dataKey="actual"
            stroke="#ffffff"
            strokeWidth={3}
            dot={{ r: 4, fill: "#ffffff" }}
            activeDot={{ r: 6 }}
            name="Actual Price"
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="sarima"
            stroke="hsl(217, 91%, 60%)"
            strokeWidth={2.5}
            strokeDasharray="5 5"
            dot={{ r: 3, fill: "hsl(217, 91%, 60%)" }}
            activeDot={{ r: 5 }}
            name="SARIMA Forecast"
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="xgboost"
            stroke="hsl(142, 71%, 45%)"
            strokeWidth={2.5}
            strokeDasharray="3 3"
            dot={{ r: 3, fill: "hsl(142, 71%, 45%)" }}
            activeDot={{ r: 5 }}
            name="XGBoost Prediction"
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
