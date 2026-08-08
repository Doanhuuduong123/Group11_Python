import pandas as pd
import numpy as np
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Lớp chịu trách nhiệm tải, kiểm tra và tiền xử lý dữ liệu giao dịch bán lẻ.
    Hỗ trợ đọc từ data/raw/ và lưu dữ liệu sạch ra data/processed/.
    """
    def __init__(self, file_path: str = None):
        """
        Khởi tạo DataLoader với đường dẫn file dữ liệu.
        
        :param file_path: Đường dẫn tới file dữ liệu (.csv, .xlsx, .json hoặc .xml)
                          Mặc định: data/raw/Superstore.csv
        """
        if file_path is None:
            # Tự động tìm file từ thư mục gốc dự án
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', 'raw', 'Superstore.csv')
        self.file_path = file_path
        self.raw_df: Optional[pd.DataFrame] = None
        self.clean_df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """
        Đọc dữ liệu từ file đĩa với xử lý ngoại lệ.
        
        :return: DataFrame dữ liệu thô
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Không tìm thấy file tại đường dẫn: {self.file_path}")
            
            if self.file_path.endswith('.csv'):
                self.raw_df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xls', '.xlsx')):
                self.raw_df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.json'):
                self.raw_df = pd.read_json(self.file_path)
            elif self.file_path.endswith('.xml'):
                self.raw_df = pd.read_xml(self.file_path)
                # Nếu file XML sử dụng tên thẻ an toàn (underscore thay vì khoảng trắng),
                # chuyển lại tên cột để phù hợp với các cột tiêu chuẩn trong bộ dữ liệu.
                if 'Order Date' not in self.raw_df.columns and 'Order_Date' in self.raw_df.columns:
                    self.raw_df.columns = [col.replace('_', ' ') for col in self.raw_df.columns]
            else:
                raise ValueError("Định dạng file không hỗ trợ. Vui lòng sử dụng CSV, Excel, JSON hoặc XML.")
            
            logger.info(f"Tải dữ liệu thành công: {self.raw_df.shape[0]} dòng, {self.raw_df.shape[1]} cột.")
            print(f"[DataLoader] Tải dữ liệu thành công: {self.raw_df.shape[0]} dòng, {self.raw_df.shape[1]} cột.")
            return self.raw_df
        except Exception as e:
            logger.error(f"Lỗi khi tải dữ liệu: {e}")
            print(f"[DataLoader Error] Lỗi khi tải dữ liệu: {e}")
            raise e

    def preprocess(self) -> pd.DataFrame:
        """
        Tiền xử lý dữ liệu: làm sạch thiếu (NaN), ép kiểu datetime, loại bỏ dòng trùng lặp,
        và trích xuất các trường thời gian (Năm, Tháng, Quý, Thứ trong tuần).
        
        :return: DataFrame đã làm sạch
        """
        if self.raw_df is None:
            self.load_data()

        df = self.raw_df.copy()

        # 1. Xử lý trùng lặp
        initial_count = len(df)
        df.drop_duplicates(inplace=True)
        dropped_duplicates = initial_count - len(df)

        # 2. Xử lý giá trị bị thiếu (Imputation / Removal)
        if 'Sales' in df.columns:
            if 'Sub-Category' in df.columns:
                df['Sales'] = df.groupby('Sub-Category')['Sales'].transform(lambda x: x.fillna(x.median()))
            df['Sales'] = df['Sales'].fillna(df['Sales'].median())
            
        if 'Profit' in df.columns:
            df['Profit'] = df['Profit'].fillna(0.0)

        # 3. Chuẩn hóa ngày tháng
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Year'] = df['Order Date'].dt.year
            df['Month'] = df['Order Date'].dt.month
            df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
            df['Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
            df['DayOfWeek'] = df['Order Date'].dt.day_name()

        if 'Ship Date' in df.columns:
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])

        self.clean_df = df
        logger.info(f"Tiền xử lý hoàn tất! Loại bỏ {dropped_duplicates} trùng lặp. Tổng dòng sạch: {len(self.clean_df)}")
        print(f"[DataLoader] Tiền xử lý hoàn tất! Đã loại bỏ {dropped_duplicates} trùng lặp. Tổng số dòng sạch: {len(self.clean_df)}")
        return self.clean_df

    def save_processed(self, output_path: str = None) -> str:
        """
        Lưu dữ liệu đã làm sạch ra thư mục data/processed/.
        
        :param output_path: Đường dẫn file output. Mặc định: data/processed/Superstore_clean.csv
        :return: Đường dẫn file đã lưu
        """
        if self.clean_df is None:
            raise ValueError("Chưa có dữ liệu đã xử lý. Hãy gọi preprocess() trước.")
        
        if output_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base_dir, 'data', 'processed')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'Superstore_clean.csv')
        
        self.clean_df.to_csv(output_path, index=False)
        logger.info(f"Đã lưu dữ liệu sạch tại: {output_path}")
        print(f"[DataLoader] Đã lưu dữ liệu sạch tại: {output_path}")
        return output_path

    def get_data_summary(self) -> Dict[str, Any]:
        """
        Trả về thông tin tổng quan về dữ liệu đã xử lý.
        
        :return: Dictionary chứa các thông tin tổng quan
        """
        df = self.clean_df if self.clean_df is not None else self.raw_df
        if df is None:
            return {}
        
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        }
        
        if 'Sales' in df.columns:
            summary['total_sales'] = round(df['Sales'].sum(), 2)
        if 'Profit' in df.columns:
            summary['total_profit'] = round(df['Profit'].sum(), 2)
        if 'Order ID' in df.columns:
            summary['unique_orders'] = df['Order ID'].nunique()
        if 'Customer ID' in df.columns:
            summary['unique_customers'] = df['Customer ID'].nunique()
            
        return summary
