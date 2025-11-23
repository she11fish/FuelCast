import { Dashboard } from "@/components/Dashboard";
import { Fuel } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 rounded-xl bg-gradient-to-br from-primary/20 to-accent/20">
              <Fuel className="w-8 h-8 text-primary" />
            </div>
            <h1 className="text-5xl md:text-6xl font-bold gradient-text">
              FuelCast
            </h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            AI-powered gasoline price forecasting using advanced SARIMA and XGBoost models.
            Predict future prices with confidence and explore the key factors driving market trends.
          </p>
        </div>

        {/* Dashboard */}
        <Dashboard />

        {/* Footer */}
        <div className="mt-16 text-center text-sm text-muted-foreground">
          <p>
            Data powered by FastAPI backend • Models: SARIMA & XGBoost
          </p>
        </div>
      </div>
    </main>
  );
}
