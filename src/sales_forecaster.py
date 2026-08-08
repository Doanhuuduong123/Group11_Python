import pandas as pd
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SalesForecaster:
    """
    Lớp dự báo doanh số bán hàng sử dụng các phương pháp đơn giản:
    - Simple Moving Average (SMA)
    - Exponential Moving Average (EMA)  
    - Linear Regression
    """
    def __init__(self, monthly_sales: pd.DataFrame):
        """
        Khởi tạo SalesForecaster.
        
        :param monthly_sales: DataFrame với cột 'Order Date' và 'Sales' (dữ liệu theo tháng)
        """
        self.monthly_sales = monthly_sales.copy()
        self.monthly_sales = self.monthly_sales.sort_values('Order Date').reset_index(drop=True)
    
    def simple_moving_average(self, window: int = 3) -> pd.DataFrame:
        """
        Tính Simple Moving Average (SMA) cho doanh số.
        
        :param window: Kích thước cửa sổ trung bình (số tháng)
        :return: DataFrame với cột SMA đã thêm
        """
        df = self.monthly_sales.copy()
        df['SMA'] = df['Sales'].rolling(window=window, min_periods=1).mean()
        return df
    
    def exponential_moving_average(self, alpha: float = 0.3) -> pd.DataFrame:
        """
        Tính Exponential Moving Average (EMA) cho doanh số.
        
        :param alpha: Hệ số làm mượt (0 < alpha <= 1). Alpha lớn = phản ứng nhanh hơn.
        :return: DataFrame với cột EMA đã thêm
        """
        df = self.monthly_sales.copy()
        df['EMA'] = df['Sales'].ewm(alpha=alpha, adjust=False).mean()
        return df
    
    def linear_regression_forecast(self, n_periods: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Dự báo doanh số bằng hồi quy tuyến tính đơn giản.
        
        :param n_periods: Số tháng dự báo phía trước
        :return: Tuple (historical_with_trend, forecast_df)
        """
        from sklearn.linear_model import LinearRegression
        
        df = self.monthly_sales.copy()
        df['Period_Num'] = range(1, len(df) + 1)
        
        X = df[['Period_Num']].values
        y = df['Sales'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Trend trên dữ liệu lịch sử
        df['Trend'] = model.predict(X)
        
        # Dự báo tương lai
        last_period = len(df)
        future_periods = np.arange(last_period + 1, last_period + 1 + n_periods).reshape(-1, 1)
        future_sales = model.predict(future_periods)
        
        # Tạo ngày tương lai
        last_date = df['Order Date'].max()
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=n_periods, freq='ME')
        
        forecast_df = pd.DataFrame({
            'Order Date': future_dates,
            'Forecast_Sales': future_sales,
            'Period_Num': range(last_period + 1, last_period + 1 + n_periods)
        })
        
        return df, forecast_df
    
    def forecast_next_periods(self, n_periods: int = 3, method: str = 'sma', **kwargs) -> pd.DataFrame:
        """
        Dự báo N tháng tiếp theo bằng phương pháp được chỉ định.
        
        :param n_periods: Số tháng dự báo
        :param method: Phương pháp ('sma', 'ema', 'linear')
        :return: DataFrame chứa dự báo
        """
        if method == 'linear':
            _, forecast = self.linear_regression_forecast(n_periods)
            return forecast
        
        # Với SMA/EMA, dùng giá trị cuối cùng làm dự báo
        if method == 'sma':
            window = kwargs.get('window', 3)
            result = self.simple_moving_average(window)
            forecast_value = result['SMA'].iloc[-1]
        elif method == 'ema':
            alpha = kwargs.get('alpha', 0.3)
            result = self.exponential_moving_average(alpha)
            forecast_value = result['EMA'].iloc[-1]
        else:
            raise ValueError(f"Phương pháp '{method}' không được hỗ trợ. Sử dụng 'sma', 'ema', hoặc 'linear'.")
        
        last_date = self.monthly_sales['Order Date'].max()
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=n_periods, freq='ME')
        
        forecast_df = pd.DataFrame({
            'Order Date': future_dates,
            'Forecast_Sales': [forecast_value] * n_periods
        })
        
        return forecast_df
    
    def get_forecast_metrics(self, method: str = 'sma', **kwargs) -> dict:
        """
        Tính các chỉ số đánh giá mô hình dự báo (trên dữ liệu lịch sử).
        
        :param method: Phương pháp dự báo
        :return: Dictionary chứa MAE, MAPE, RMSE
        """
        df = self.monthly_sales.copy()
        
        if method == 'sma':
            window = kwargs.get('window', 3)
            result = self.simple_moving_average(window)
            predicted = result['SMA']
        elif method == 'ema':
            alpha = kwargs.get('alpha', 0.3)
            result = self.exponential_moving_average(alpha)
            predicted = result['EMA']
        elif method == 'linear':
            result, _ = self.linear_regression_forecast()
            predicted = result['Trend']
        else:
            raise ValueError(f"Phương pháp '{method}' không được hỗ trợ.")
        
        actual = df['Sales'].values
        pred = predicted.values
        
        # Loại bỏ giá trị NaN
        mask = ~(np.isnan(actual) | np.isnan(pred))
        actual = actual[mask]
        pred = pred[mask]
        
        if len(actual) == 0:
            return {'MAE': 0, 'MAPE': 0, 'RMSE': 0}
        
        mae = np.mean(np.abs(actual - pred))
        mape = np.mean(np.abs((actual - pred) / np.where(actual == 0, 1, actual))) * 100
        rmse = np.sqrt(np.mean((actual - pred) ** 2))
        
        return {
            'MAE': round(mae, 2),
            'MAPE': round(mape, 2),
            'RMSE': round(rmse, 2)
        }
