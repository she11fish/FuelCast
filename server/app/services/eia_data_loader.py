"""EIA API data loader for gas and crude oil prices"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Optional
import os

class EIADataLoader:
    """Loader for Energy Information Administration (EIA) API data"""
    
    # EIA Open Data API endpoints (no API key required for some endpoints)
    GAS_PRICE_URL = "https://api.eia.gov/v2/petroleum/pri/gnd/data/"
    CRUDE_PRICE_URL = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize EIA data loader
        
        Args:
            api_key: Optional EIA API key for higher rate limits
        """
        self.api_key = api_key
    
    def fetch_gas_prices(self, start_date: str = None, weeks: int = 156) -> pd.DataFrame:
        """
        Fetch US regular gasoline retail prices (weekly)
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: {weeks} weeks ago)
            weeks: Number of weeks of data to fetch
            
        Returns:
            DataFrame with columns: date, gas_price
        """
        try:
            # Calculate date range
            if start_date is None:
                end_date = datetime.now()
                start_date = end_date - timedelta(weeks=weeks)
                start_date = start_date.strftime('%Y-%m-%d')
            
            params = {
                'frequency': 'weekly',
                'data[0]': 'value',
                'facets[product][]': 'EPM0',  # Regular gasoline
                'facets[duoarea][]': 'NUS',    # US National
                'sort[0][column]': 'period',
                'sort[0][direction]': 'desc',
                'offset': 0,
                'length': weeks * 2  # Get extra to ensure coverage
            }
            
            if self.api_key:
                params['api_key'] = self.api_key
            
            response = requests.get(self.GAS_PRICE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'response' in data and 'data' in data['response']:
                records = data['response']['data']
                
                # Convert to DataFrame
                df = pd.DataFrame(records)
                df = df.rename(columns={'period': 'date', 'value': 'gas_price'})
                df = df[['date', 'gas_price']]
                
                # Convert date and sort
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                # Ensure numeric
                df['gas_price'] = pd.to_numeric(df['gas_price'], errors='coerce')
                df = df.dropna()
                
                return df
            else:
                raise ValueError("Unexpected API response format")
                
        except Exception as e:
            print(f"Error fetching gas prices from EIA: {e}")
            return self._get_fallback_gas_data(weeks)
    
    def fetch_crude_prices(self, start_date: str = None, weeks: int = 156) -> pd.DataFrame:
        """
        Fetch WTI crude oil spot prices (daily, will be aggregated to weekly)
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            weeks: Number of weeks of data to fetch
            
        Returns:
            DataFrame with columns: date, close
        """
        try:
            # Calculate date range
            if start_date is None:
                end_date = datetime.now()
                start_date = end_date - timedelta(weeks=weeks)
                start_date = start_date.strftime('%Y-%m-%d')
            
            params = {
                'frequency': 'daily',
                'data[0]': 'value',
                'facets[product][]': 'EPCWTI',  # WTI Crude
                'sort[0][column]': 'period',
                'sort[0][direction]': 'desc',
                'offset': 0,
                'length': weeks * 10  # Daily data, so need more records
            }
            
            if self.api_key:
                params['api_key'] = self.api_key
            
            response = requests.get(self.CRUDE_PRICE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'response' in data and 'data' in data['response']:
                records = data['response']['data']
                
                # Convert to DataFrame
                df = pd.DataFrame(records)
                df = df.rename(columns={'period': 'date', 'value': 'close'})
                df = df[['date', 'close']]
                
                # Convert date and sort
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                # Ensure numeric
                df['close'] = pd.to_numeric(df['close'], errors='coerce')
                df = df.dropna()
                
                # Resample to weekly (Monday-aligned to match EIA gas prices)
                df = df.set_index('date')
                df_weekly = df['close'].resample('W-MON').mean().to_frame()
                df_weekly = df_weekly.reset_index()
                
                return df_weekly
            else:
                raise ValueError("Unexpected API response format")
                
        except Exception as e:
            print(f"Error fetching crude prices from EIA: {e}")
            return self._get_fallback_crude_data(weeks)
    
    def get_aligned_data(self, weeks: int = 156) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetch both gas and crude prices and align them by date
        
        Args:
            weeks: Number of weeks of historical data
            
        Returns:
            Tuple of (gas_df, crude_df) with aligned dates
        """
        gas_df = self.fetch_gas_prices(weeks=weeks)
        crude_df = self.fetch_crude_prices(weeks=weeks)
        
        # Merge on date with inner join to get aligned data
        merged = pd.merge(gas_df, crude_df, on='date', how='inner')
        
        gas_aligned = merged[['date', 'gas_price']].copy()
        crude_aligned = merged[['date', 'close']].copy()
        
        return gas_aligned, crude_aligned
    
    @staticmethod
    def _get_fallback_gas_data(weeks: int) -> pd.DataFrame:
        """Fallback synthetic gas price data if API fails"""
        import numpy as np
        
        end_date = datetime.now()
        dates = [end_date - timedelta(weeks=i) for i in range(weeks, -1, -1)]
        
        # Generate realistic-looking data
        base = 3.50
        trend = np.linspace(-0.5, 0.5, len(dates))
        seasonal = 0.3 * np.sin(np.linspace(0, 4 * np.pi, len(dates)))
        noise = np.random.normal(0, 0.1, len(dates))
        prices = base + trend + seasonal + noise
        
        return pd.DataFrame({
            'date': dates,
            'gas_price': prices
        })
    
    @staticmethod
    def _get_fallback_crude_data(weeks: int) -> pd.DataFrame:
        """Fallback synthetic crude price data if API fails"""
        import numpy as np
        
        end_date = datetime.now()
        dates = [end_date - timedelta(weeks=i) for i in range(weeks, -1, -1)]
        
        # Generate realistic-looking data
        base = 75.0
        trend = np.linspace(-10, 10, len(dates))
        seasonal = 5 * np.sin(np.linspace(0, 4 * np.pi, len(dates)))
        noise = np.random.normal(0, 2, len(dates))
        prices = base + trend + seasonal + noise
        
        return pd.DataFrame({
            'date': dates,
            'close': prices
        })


# Create singleton instance
eia_loader = EIADataLoader(api_key=os.getenv("EIA_API_KEY"))
