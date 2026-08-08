import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional


class RetailAnalyzer:
    """
    Lớp xử lý nghiệp vụ phân tích dữ liệu bán lẻ siêu thị.
    Cung cấp các hàm phân tích doanh số, lợi nhuận, phân khúc khách hàng RFM và giỏ hàng.
    """
    def __init__(self, df: pd.DataFrame):
        """
        Khởi tạo RetailAnalyzer với DataFrame đã được tiền xử lý.
        
        :param df: DataFrame chứa dữ liệu bán lẻ sạch
        """
        self.df = df.copy()
        self._cache = {}

    def _get_cached(self, key: str):
        return self._cache.get(key)

    def _set_cached(self, key: str, value):
        self._cache[key] = value
        return value

    def _clear_cache(self):
        self._cache.clear()

    def analyze_sales_by_dimension(self, dimension: str = 'Category') -> pd.DataFrame:
        """
        Tính tổng doanh số và lợi nhuận theo từng chiều dữ liệu.
        
        :param dimension: Tên cột cần gom nhóm (vd: 'Category', 'Region', 'YearMonth', 'Quarter')
        :return: DataFrame tổng hợp doanh số, lợi nhuận, tỷ suất lợi nhuận
        """
        if dimension not in self.df.columns:
            raise KeyError(f"Chiều phân tích '{dimension}' không tồn tại trong dữ liệu.")

        cache_key = f"sales_by_dimension::{dimension}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached.copy()
            
        summary = self.df.groupby(dimension).agg(
            Total_Sales=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Total_Quantity=('Quantity', 'sum'),
            Order_Count=('Order ID', 'nunique')
        ).reset_index()

        summary['Profit_Margin_%'] = round((summary['Total_Profit'] / summary['Total_Sales']) * 100, 2)
        summary = summary.sort_values(by='Total_Sales', ascending=False)
        return self._set_cached(cache_key, summary.copy())

    def get_top_performers(self, top_n: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Lấy danh sách Top N Sản phẩm và Top N Khách hàng mang lại doanh số cao nhất.
        
        :param top_n: Số lượng sản phẩm/khách hàng hàng đầu
        :return: Tuple gồm (Top Products DataFrame, Top Customers DataFrame)
        """
        top_products = self.df.groupby('Product Name').agg(
            Total_Sales=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Quantity_Sold=('Quantity', 'sum')
        ).reset_index().sort_values(by='Total_Sales', ascending=False).head(top_n)

        cache_key = f"top_performers::{top_n}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        top_customers = self.df.groupby(['Customer ID', 'Customer Name']).agg(
            Total_Spent=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Total_Orders=('Order ID', 'nunique')
        ).reset_index().sort_values(by='Total_Spent', ascending=False).head(top_n)

        result = (top_products, top_customers)
        return self._set_cached(cache_key, result)

    def analyze_seasonality_and_discount(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Phân tích tính mùa vụ và tác động của chính sách giảm giá đến lợi nhuận.
        
        :return: Tuple gồm (Seasonality DataFrame, Discount Impact DataFrame)
        """
        cache_key = "seasonality_and_discount"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        seasonality = self.df.groupby('DayOfWeek').agg(
            Avg_Sales=('Sales', 'mean'),
            Total_Sales=('Sales', 'sum'),
            Total_Orders=('Order ID', 'nunique')
        ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).dropna()

        df_copy = self.df.copy()
        bins = [-0.01, 0.0, 0.1, 0.2, 0.3, 0.5, 1.0]
        labels = ['0%', '1-10%', '11-20%', '21-30%', '31-50%', '>50%']
        df_copy['Discount_Band'] = pd.cut(df_copy['Discount'], bins=bins, labels=labels)

        discount_impact = df_copy.groupby('Discount_Band', observed=False).agg(
            Avg_Sales=('Sales', 'mean'),
            Avg_Profit=('Profit', 'mean'),
            Total_Profit=('Profit', 'sum'),
            Order_Count=('Order ID', 'count')
        ).reset_index()

        return self._set_cached(cache_key, (seasonality, discount_impact))

    def create_multidimensional_pivot(self, index: str = 'Category', columns: str = 'Region') -> pd.DataFrame:
        """
        Tạo Pivot Table đa chiều phân tích doanh số kết hợp giữa 2 trục.
        """
        cache_key = f"pivot::{index}::{columns}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached.copy()

        pivot = pd.pivot_table(
            self.df,
            values='Sales',
            index=index,
            columns=columns,
            aggfunc='sum',
            fill_value=0
        )
        return self._set_cached(cache_key, pivot.copy())

    def calculate_rfm(self, snapshot_date: pd.Timestamp = None) -> pd.DataFrame:
        """
        Phân tích phân khúc khách hàng RFM.
        
        :param snapshot_date: Ngày tham chiếu để tính Recency
        :return: DataFrame phân hạng khách hàng theo RFM
        """
        if snapshot_date is None:
            snapshot_date = self.df['Order Date'].max() + pd.Timedelta(days=1)

        cache_key = f"rfm::{snapshot_date.strftime('%Y-%m-%d')}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached.copy()

        rfm = self.df.groupby('Customer ID').agg({
            'Order Date': lambda x: (snapshot_date - x.max()).days,
            'Order ID': 'nunique',
            'Sales': 'sum'
        }).reset_index()

        rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

        # Đánh giá điểm RFM (1-4)
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop')

        rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(int).sum(axis=1)

        def segment_customer(row):
            if row['RFM_Score'] >= 10:
                return 'VIP / Champions'
            elif row['RFM_Score'] >= 7:
                return 'Loyal Customers'
            elif row['RFM_Score'] >= 5:
                return 'At Risk / Potential'
            else:
                return 'Lost / Inactive'

        rfm['Customer_Segment'] = rfm.apply(segment_customer, axis=1)
        return self._set_cached(cache_key, rfm.copy())

    def market_basket_analysis(self, top_pairs: int = 10) -> pd.DataFrame:
        """
        Phân tích giỏ hàng đơn giản (Market Basket Analysis).
        """
        from itertools import combinations
        from collections import Counter

        orders_baskets = self.df.groupby('Order ID')['Sub-Category'].apply(lambda x: list(set(x)))
        
        pair_counter = Counter()
        for basket in orders_baskets:
            if len(basket) > 1:
                pairs = combinations(sorted(basket), 2)
                pair_counter.update(pairs)

        cache_key = f"basket::{top_pairs}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached.copy()

        pairs_df = pd.DataFrame(pair_counter.most_common(top_pairs), columns=['Product Pair', 'Co_Occurrence_Count'])
        pairs_df['Product 1'] = pairs_df['Product Pair'].apply(lambda x: x[0])
        pairs_df['Product 2'] = pairs_df['Product Pair'].apply(lambda x: x[1])
        result = pairs_df[['Product 1', 'Product 2', 'Co_Occurrence_Count']]
        return self._set_cached(cache_key, result.copy())

    def get_monthly_sales(self) -> pd.DataFrame:
        """
        Tính doanh số gộp theo tháng cho biểu đồ xu hướng và dự báo.
        
        :return: DataFrame với cột 'Order Date' (monthly) và 'Sales'
        """
        df = self.df.copy()
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        cache_key = "monthly_sales"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached.copy()

        monthly = df.resample('ME', on='Order Date').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Orders=('Order ID', 'nunique')
        ).reset_index()
        monthly = monthly.sort_values('Order Date')
        monthly['Month'] = monthly['Order Date'].dt.strftime('%Y-%m')
        return self._set_cached(cache_key, monthly.copy())

    def detect_outliers_iqr(self, columns: Optional[list] = None, iqr_multiplier: float = 1.5) -> pd.DataFrame:
        """
        Phát hiện ngoại lai bằng phương pháp IQR cho một hoặc nhiều cột số.

        :param columns: Danh sách cột cần kiểm tra. Mặc định là ['Sales', 'Profit'] nếu có trong dữ liệu.
        :param iqr_multiplier: Hệ số nhân cho khoảng IQR.
        :return: DataFrame tóm tắt ngưỡng và số lượng ngoại lai cho từng cột.
        """
        if columns is None:
            columns = [col for col in ['Sales', 'Profit'] if col in self.df.columns]

        summary_rows = []
        for col in columns:
            if col not in self.df.columns:
                continue

            series = pd.to_numeric(self.df[col], errors='coerce').dropna()
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - iqr_multiplier * iqr
            upper_bound = q3 + iqr_multiplier * iqr
            outlier_mask = (series < lower_bound) | (series > upper_bound)
            summary_rows.append({
                'Column': col,
                'Q1': q1,
                'Q3': q3,
                'IQR': iqr,
                'Lower_Bound': lower_bound,
                'Upper_Bound': upper_bound,
                'Outlier_Count': int(outlier_mask.sum())
            })

        return pd.DataFrame(summary_rows).set_index('Column')

    def get_region_breakdown(self) -> pd.DataFrame:
        """
        Phân tích doanh số chi tiết theo khu vực.
        
        :return: DataFrame tổng hợp theo Region
        """
        return self.analyze_sales_by_dimension('Region')

    def get_segment_breakdown(self) -> pd.DataFrame:
        """
        Phân tích doanh số chi tiết theo phân khúc khách hàng.
        
        :return: DataFrame tổng hợp theo Segment
        """
        if 'Segment' not in self.df.columns:
            return pd.DataFrame()
        return self.analyze_sales_by_dimension('Segment')
