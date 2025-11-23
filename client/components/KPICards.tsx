import { TrendingUp, DollarSign, Target } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import type { Metrics } from "@/lib/api";

interface KPICardsProps {
  metrics: Metrics | null;
  predictedPrice: number | null;
}

export function KPICards({ metrics, predictedPrice }: KPICardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Current Gasoline Price */}
      <div className="glass-strong rounded-xl p-6 hover:scale-105 transition-transform duration-300 animate-slide-up">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-primary/20 to-primary/5">
            <DollarSign className="w-6 h-6 text-primary" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground mb-1">Current Gasoline Price</p>
        <p className="text-3xl font-bold">
          {metrics ? formatCurrency(metrics.current_price) : "—"}
        </p>
        <p className="text-xs text-muted-foreground mt-2">Per gallon</p>
      </div>

      {/* Predicted Price */}
      <div className="glass-strong rounded-xl p-6 hover:scale-105 transition-transform duration-300 animate-slide-up" style={{ animationDelay: "0.1s" }}>
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-secondary/20 to-secondary/5">
            <TrendingUp className="w-6 h-6 text-secondary" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground mb-1">Predicted (Next Week)</p>
        <p className="text-3xl font-bold">
          {predictedPrice ? formatCurrency(predictedPrice) : "—"}
        </p>
        <p className="text-xs text-muted-foreground mt-2">XGBoost model</p>
      </div>

      {/* SARIMA RMSE */}
      <div className="glass-strong rounded-xl p-6 hover:scale-105 transition-transform duration-300 animate-slide-up" style={{ animationDelay: "0.2s" }}>
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-accent/20 to-accent/5">
            <Target className="w-6 h-6 text-accent" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground mb-1">SARIMA Accuracy</p>
        <p className="text-3xl font-bold">
          {metrics ? metrics.sarima_rmse.toFixed(3) : "—"}
        </p>
        <p className="text-xs text-muted-foreground mt-2">RMSE</p>
      </div>

      {/* XGBoost RMSE */}
      <div className="glass-strong rounded-xl p-6 hover:scale-105 transition-transform duration-300 animate-slide-up" style={{ animationDelay: "0.3s" }}>
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-secondary/20 to-secondary/5">
            <Target className="w-6 h-6 text-secondary" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground mb-1">XGBoost Accuracy</p>
        <p className="text-3xl font-bold">
          {metrics ? metrics.xgboost_rmse.toFixed(3) : "—"}
        </p>
        <p className="text-xs text-muted-foreground mt-2">RMSE</p>
      </div>
    </div>
  );
}
