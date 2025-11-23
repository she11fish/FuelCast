import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { FeatureImportance as FeatureImportanceType } from "@/lib/api";

interface FeatureImportanceProps {
  data: FeatureImportanceType[];
}

export function FeatureImportance({ data }: FeatureImportanceProps) {
  // Sort by score descending and take top 10
  const topFeatures = [...data]
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-strong rounded-lg p-3 shadow-xl">
          <p className="text-sm font-semibold">{payload[0].payload.feature}</p>
          <p className="text-sm text-secondary">
            Score: {payload[0].value.toFixed(3)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-strong rounded-xl p-6 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 gradient-text">
        Feature Importance (XGBoost)
      </h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={topFeatures}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
        >
          <defs>
            <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="hsl(217, 91%, 60%)" />
              <stop offset="100%" stopColor="hsl(280, 100%, 70%)" />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            type="number"
            stroke="rgba(255,255,255,0.5)"
            style={{ fontSize: "12px" }}
          />
          <YAxis
            type="category"
            dataKey="feature"
            stroke="rgba(255,255,255,0.5)"
            style={{ fontSize: "12px" }}
            width={110}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar
            dataKey="score"
            fill="url(#barGradient)"
            radius={[0, 8, 8, 0]}
            animationDuration={800}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
