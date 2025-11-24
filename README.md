# ⛽ FuelCast

**AI-Powered Predictive Analytics for Fuel Price Forecasting**

FuelCast is a state-of-the-art dashboard that leverages hybrid machine learning models (SARIMAX + XGBoost) to forecast US gasoline prices. It provides real-time insights, model performance metrics, and explainable AI features to help stakeholders make data-driven decisions.

## Features

🚀 **Advanced Forecasting**
- Hybrid AI Model (SARIMAX + XGBoost)
- Real-time price predictions
- Interactive time-range filtering
- Responsive Recharts components

🎨 **Premium Design**
- Dark mode optimized
- Glassmorphism effects
- Smooth micro-animations
- Vibrant gradient accents

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript (Strict mode)
- **Charts**: Recharts
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Backend**: FastAPI (Python)

## Prerequisites

- Node.js 18+ installed
- FastAPI backend running on `http://localhost:8000`

## Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Requirements

The dashboard expects the following FastAPI endpoints:

### GET `/forecast`
Returns forecast data points:
```json
[
  {"date": "2024-01-01", "actual": 3.45, "sarima": 3.44, "xgboost": 3.46},
  {"date": "2024-01-08", "actual": null, "sarima": 3.50, "xgboost": 3.52}
]
```

### GET `/metrics`
Returns model performance metrics:
```json
{
  "sarima_rmse": 0.04,
  "xgboost_rmse": 0.02,
  "current_price": 3.45
}
```

### GET `/importance`
Returns feature importance scores:
```json
[
  {"feature": "Crude Price Lag-4", "score": 0.8},
  {"feature": "Seasonality", "score": 0.6}
]
```

## Project Structure

```
FuelCast/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── Dashboard.tsx       # Main dashboard component
│   ├── KPICards.tsx        # Metrics cards
│   ├── ForecastChart.tsx   # Line chart
│   ├── FeatureImportance.tsx # Bar chart
│   └── TimeRangeSelector.tsx # Filter control
├── lib/
│   ├── api.ts              # API client
│   └── utils.ts            # Utility functions
└── package.json
```

## Time Range Filters

- **All Time**: Shows complete historical and forecast data
- **Last Year**: Displays data from the past 12 months
- **Forecast Only**: Shows only future predictions

## License

MIT
