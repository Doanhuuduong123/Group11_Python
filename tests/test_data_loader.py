import pytest
import pandas as pd
import os
import sys
import tempfile

# Thêm thư mục gốc dự án vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader


class TestDataLoader:
    """Unit tests cho lớp DataLoader."""
    
    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Tạo file CSV mẫu để test."""
        data = {
            'Order ID': ['CA-001', 'CA-001', 'CA-002', 'CA-003', 'CA-003'],
            'Order Date': ['2024-01-15', '2024-01-15', '2024-02-20', '2024-03-10', '2024-03-10'],
            'Ship Date': ['2024-01-18', '2024-01-18', '2024-02-23', '2024-03-13', '2024-03-13'],
            'Customer ID': ['C001', 'C001', 'C002', 'C003', 'C003'],
            'Customer Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie'],
            'Segment': ['Consumer', 'Consumer', 'Corporate', 'Home Office', 'Home Office'],
            'Region': ['North', 'North', 'South', 'East', 'East'],
            'Category': ['Technology', 'Furniture', 'Office Supplies', 'Technology', 'Furniture'],
            'Sub-Category': ['Phones', 'Chairs', 'Paper', 'Accessories', 'Tables'],
            'Product Name': ['Phone X', 'Chair A', 'Paper B', 'Accessory C', 'Table D'],
            'Sales': [500.0, 300.0, None, 200.0, 150.0],
            'Quantity': [2, 1, 5, 3, 1],
            'Discount': [0.0, 0.1, 0.2, 0.0, 0.3],
            'Profit': [100.0, 50.0, 30.0, None, -10.0]
        }
        df = pd.DataFrame(data)
        csv_path = os.path.join(str(tmp_path), 'test_data.csv')
        df.to_csv(csv_path, index=False)
        return csv_path
    
    def test_load_data_success(self, sample_csv):
        """Test tải dữ liệu thành công."""
        loader = DataLoader(sample_csv)
        df = loader.load_data()
        assert df is not None
        assert len(df) == 5
        assert 'Sales' in df.columns
    
    def test_load_data_file_not_found(self):
        """Test xử lý ngoại lệ khi file không tồn tại."""
        loader = DataLoader('nonexistent_file.csv')
        with pytest.raises(FileNotFoundError):
            loader.load_data()
    
    def test_load_data_unsuppported_format(self, tmp_path):
        """Test xử lý file định dạng không hỗ trợ."""
        txt_path = os.path.join(str(tmp_path), 'test.txt')
        with open(txt_path, 'w') as f:
            f.write('test data')
        loader = DataLoader(txt_path)
        with pytest.raises(ValueError):
            loader.load_data()

    @pytest.fixture
    def sample_json(self, tmp_path):
        """Tạo file JSON mẫu để test."""
        data = {
            'Order ID': ['CA-001', 'CA-001', 'CA-002', 'CA-003', 'CA-003'],
            'Order Date': ['2024-01-15', '2024-01-15', '2024-02-20', '2024-03-10', '2024-03-10'],
            'Ship Date': ['2024-01-18', '2024-01-18', '2024-02-23', '2024-03-13', '2024-03-13'],
            'Customer ID': ['C001', 'C001', 'C002', 'C003', 'C003'],
            'Customer Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie'],
            'Segment': ['Consumer', 'Consumer', 'Corporate', 'Home Office', 'Home Office'],
            'Region': ['North', 'North', 'South', 'East', 'East'],
            'Category': ['Technology', 'Furniture', 'Office Supplies', 'Technology', 'Furniture'],
            'Sub-Category': ['Phones', 'Chairs', 'Paper', 'Accessories', 'Tables'],
            'Product Name': ['Phone X', 'Chair A', 'Paper B', 'Accessory C', 'Table D'],
            'Sales': [500.0, 300.0, None, 200.0, 150.0],
            'Quantity': [2, 1, 5, 3, 1],
            'Discount': [0.0, 0.1, 0.2, 0.0, 0.3],
            'Profit': [100.0, 50.0, 30.0, None, -10.0]
        }
        df = pd.DataFrame(data)
        json_path = os.path.join(str(tmp_path), 'test_data.json')
        df.to_json(json_path, orient='records', date_format='iso')
        return json_path

    @pytest.fixture
    def sample_xml(self, tmp_path):
        """Tạo file XML mẫu để test."""
        data = {
            'Order ID': ['CA-001', 'CA-001', 'CA-002', 'CA-003', 'CA-003'],
            'Order Date': ['2024-01-15', '2024-01-15', '2024-02-20', '2024-03-10', '2024-03-10'],
            'Ship Date': ['2024-01-18', '2024-01-18', '2024-02-23', '2024-03-13', '2024-03-13'],
            'Customer ID': ['C001', 'C001', 'C002', 'C003', 'C003'],
            'Customer Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie'],
            'Segment': ['Consumer', 'Consumer', 'Corporate', 'Home Office', 'Home Office'],
            'Region': ['North', 'North', 'South', 'East', 'East'],
            'Category': ['Technology', 'Furniture', 'Office Supplies', 'Technology', 'Furniture'],
            'Sub-Category': ['Phones', 'Chairs', 'Paper', 'Accessories', 'Tables'],
            'Product Name': ['Phone X', 'Chair A', 'Paper B', 'Accessory C', 'Table D'],
            'Sales': [500.0, 300.0, None, 200.0, 150.0],
            'Quantity': [2, 1, 5, 3, 1],
            'Discount': [0.0, 0.1, 0.2, 0.0, 0.3],
            'Profit': [100.0, 50.0, 30.0, None, -10.0]
        }
        df = pd.DataFrame(data)
        xml_path = os.path.join(str(tmp_path), 'test_data.xml')
        df_sanitized = df.rename(columns=lambda c: c.replace(' ', '_'))
        df_sanitized.to_xml(xml_path, index=False)
        return xml_path

    def test_load_data_json(self, sample_json):
        """Test tải dữ liệu từ file JSON."""
        loader = DataLoader(sample_json)
        df = loader.load_data()
        assert df is not None
        assert len(df) == 5
        assert 'Sales' in df.columns

    def test_load_data_xml(self, sample_xml):
        """Test tải dữ liệu từ file XML."""
        loader = DataLoader(sample_xml)
        df = loader.load_data()
        assert df is not None
        assert len(df) == 5
        assert 'Order ID' in df.columns

    def test_preprocess_handles_missing(self, sample_csv):
        """Test tiền xử lý xử lý giá trị thiếu."""
        loader = DataLoader(sample_csv)
        loader.load_data()
        clean = loader.preprocess()
        assert clean['Sales'].isnull().sum() == 0
        assert clean['Profit'].isnull().sum() == 0
    
    def test_preprocess_extracts_time_columns(self, sample_csv):
        """Test tiền xử lý trích xuất các cột thời gian."""
        loader = DataLoader(sample_csv)
        loader.load_data()
        clean = loader.preprocess()
        assert 'Year' in clean.columns
        assert 'Month' in clean.columns
        assert 'YearMonth' in clean.columns
        assert 'Quarter' in clean.columns
        assert 'DayOfWeek' in clean.columns
    
    def test_preprocess_datetime_conversion(self, sample_csv):
        """Test chuyển đổi cột ngày tháng."""
        loader = DataLoader(sample_csv)
        loader.load_data()
        clean = loader.preprocess()
        assert pd.api.types.is_datetime64_any_dtype(clean['Order Date'])
    
    def test_save_processed(self, sample_csv, tmp_path):
        """Test lưu dữ liệu đã xử lý."""
        loader = DataLoader(sample_csv)
        loader.load_data()
        loader.preprocess()
        
        output_path = os.path.join(str(tmp_path), 'output', 'clean.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        saved_path = loader.save_processed(output_path)
        
        assert os.path.exists(saved_path)
        saved_df = pd.read_csv(saved_path)
        assert len(saved_df) > 0
    
    def test_get_data_summary(self, sample_csv):
        """Test lấy thông tin tổng quan dữ liệu."""
        loader = DataLoader(sample_csv)
        loader.load_data()
        loader.preprocess()
        summary = loader.get_data_summary()
        
        assert 'total_rows' in summary
        assert 'total_columns' in summary
        assert 'total_sales' in summary
        assert summary['total_rows'] > 0
