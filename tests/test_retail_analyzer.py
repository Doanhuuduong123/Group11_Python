import pytest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.retail_analyzer import RetailAnalyzer


class TestRetailAnalyzer:
    """Unit tests cho lớp RetailAnalyzer."""
    
    @pytest.fixture
    def sample_df(self):
        """Tạo DataFrame mẫu đã xử lý."""
        np.random.seed(42)
        n = 50
        data = {
            'Order ID': [f'CA-{1000 + i % 20}' for i in range(n)],
            'Order Date': pd.date_range('2024-01-01', periods=n, freq='3D'),
            'Customer ID': [f'C{100 + i % 15}' for i in range(n)],
            'Customer Name': [f'Customer {i % 15}' for i in range(n)],
            'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], n),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
            'Category': np.random.choice(['Technology', 'Furniture', 'Office Supplies'], n),
            'Sub-Category': np.random.choice(['Phones', 'Chairs', 'Paper', 'Binders', 'Tables'], n),
            'Product Name': [f'Product {i}' for i in range(n)],
            'Sales': np.random.uniform(50, 500, n).round(2),
            'Quantity': np.random.randint(1, 10, n),
            'Discount': np.random.choice([0.0, 0.1, 0.2, 0.3], n),
            'Profit': np.random.uniform(-50, 200, n).round(2),
            'Year': [2024] * n,
            'Month': [(i % 12) + 1 for i in range(n)],
            'YearMonth': [f'2024-{str((i % 12) + 1).zfill(2)}' for i in range(n)],
            'DayOfWeek': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], n)
        }
        return pd.DataFrame(data)
    
    def test_analyze_sales_by_category(self, sample_df):
        """Test phân tích doanh số theo danh mục."""
        analyzer = RetailAnalyzer(sample_df)
        result = analyzer.analyze_sales_by_dimension('Category')
        assert 'Total_Sales' in result.columns
        assert 'Profit_Margin_%' in result.columns
        assert len(result) > 0
    
    def test_analyze_sales_by_region(self, sample_df):
        """Test phân tích doanh số theo khu vực."""
        analyzer = RetailAnalyzer(sample_df)
        result = analyzer.analyze_sales_by_dimension('Region')
        assert len(result) > 0
    
    def test_analyze_invalid_dimension(self, sample_df):
        """Test xử lý chiều phân tích không tồn tại."""
        analyzer = RetailAnalyzer(sample_df)
        with pytest.raises(KeyError):
            analyzer.analyze_sales_by_dimension('NonExistent')
    
    def test_get_top_performers(self, sample_df):
        """Test lấy Top sản phẩm/khách hàng."""
        analyzer = RetailAnalyzer(sample_df)
        top_products, top_customers = analyzer.get_top_performers(5)
        assert len(top_products) <= 5
        assert len(top_customers) <= 5
        assert 'Total_Sales' in top_products.columns
        assert 'Total_Spent' in top_customers.columns
    
    def test_analyze_seasonality_and_discount(self, sample_df):
        """Test phân tích mùa vụ và giảm giá."""
        analyzer = RetailAnalyzer(sample_df)
        seasonality, discount_impact = analyzer.analyze_seasonality_and_discount()
        assert 'Avg_Sales' in seasonality.columns
        assert 'Discount_Band' in discount_impact.columns
    
    def test_create_pivot_table(self, sample_df):
        """Test tạo Pivot Table."""
        analyzer = RetailAnalyzer(sample_df)
        pivot = analyzer.create_multidimensional_pivot('Category', 'Region')
        assert pivot.shape[0] > 0
        assert pivot.shape[1] > 0
    
    def test_calculate_rfm(self, sample_df):
        """Test tính toán RFM."""
        analyzer = RetailAnalyzer(sample_df)
        rfm = analyzer.calculate_rfm()
        assert 'Recency' in rfm.columns
        assert 'Frequency' in rfm.columns
        assert 'Monetary' in rfm.columns
        assert 'Customer_Segment' in rfm.columns
        assert len(rfm) > 0
    
    def test_market_basket_analysis(self, sample_df):
        """Test phân tích giỏ hàng."""
        analyzer = RetailAnalyzer(sample_df)
        pairs = analyzer.market_basket_analysis(5)
        assert 'Product 1' in pairs.columns
        assert 'Product 2' in pairs.columns
    
    def test_get_monthly_sales(self, sample_df):
        """Test tính doanh số theo tháng."""
        analyzer = RetailAnalyzer(sample_df)
        monthly = analyzer.get_monthly_sales()
        assert 'Sales' in monthly.columns
        assert 'Order Date' in monthly.columns
        assert len(monthly) > 0
    
    def test_detect_outliers_iqr(self, sample_df):
        """Test phát hiện ngoại lai bằng IQR cho Sales và Profit."""
        analyzer = RetailAnalyzer(sample_df)
        outlier_summary = analyzer.detect_outliers_iqr(columns=['Sales', 'Profit'])

        assert 'Sales' in outlier_summary.index
        assert 'Profit' in outlier_summary.index
        assert 'Lower_Bound' in outlier_summary.columns
        assert 'Upper_Bound' in outlier_summary.columns
        assert 'Outlier_Count' in outlier_summary.columns

    def test_get_region_breakdown(self, sample_df):
        """Test phân tích theo khu vực."""
        analyzer = RetailAnalyzer(sample_df)
        result = analyzer.get_region_breakdown()
        assert len(result) > 0
