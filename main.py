"""
DT04 Retail Analysis - Entry Point Chính
Script thực thi toàn bộ quy trình: Tải dữ liệu → Tiền xử lý → Phân tích → Xuất kết quả.

Cách sử dụng:
    python main.py              # Chạy pipeline phân tích CLI
    python main.py --web        # Khởi chạy Streamlit Dashboard
    python main.py --gui        # Khởi chạy giao diện Desktop (CustomTkinter)
"""
import sys
import os
import argparse

# Đảm bảo thư mục gốc dự án trong sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def run_cli_pipeline():
    """Chạy pipeline phân tích dữ liệu qua CLI."""
    from src import DataLoader, RetailAnalyzer
    
    print("=" * 70)
    print("  DT04 - PHÂN TÍCH DOANH SỐ BÁN LẺ CHUỖI SIÊU THỊ")
    print("  Đại học Sư phạm - Khoa Toán - Tin")
    print("=" * 70)
    
    # 1. Tải dữ liệu
    print("\n[Bước 1/4] Tải dữ liệu...")
    data_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'Superstore.csv')
    loader = DataLoader(data_path)
    loader.load_data()
    
    # 2. Tiền xử lý
    print("\n[Bước 2/4] Tiền xử lý dữ liệu...")
    clean_df = loader.preprocess()
    
    # Lưu dữ liệu đã xử lý
    loader.save_processed()
    
    # Tóm tắt dữ liệu
    summary = loader.get_data_summary()
    print(f"\n Tóm tắt dữ liệu:")
    print(f"   - Tổng số dòng: {summary.get('total_rows', 'N/A')}")
    print(f"   - Tổng doanh thu: ${summary.get('total_sales', 0):,.2f}")
    print(f"   - Tổng lợi nhuận: ${summary.get('total_profit', 0):,.2f}")
    print(f"   - Số đơn hàng: {summary.get('unique_orders', 'N/A')}")
    print(f"   - Số khách hàng: {summary.get('unique_customers', 'N/A')}")
    
    # 3. Phân tích
    print("\n[Bước 3/4] Phân tích dữ liệu...")
    analyzer = RetailAnalyzer(clean_df)
    
    # Phân tích theo Category
    print("\n--- Doanh thu theo Danh mục ---")
    cat_analysis = analyzer.analyze_sales_by_dimension('Category')
    print(cat_analysis.to_string(index=False))
    
    # Top 10 sản phẩm
    print("\n--- Top 10 Sản Phẩm Doanh Thu Cao Nhất ---")
    top_products, top_customers = analyzer.get_top_performers(10)
    print(top_products[['Product Name', 'Total_Sales', 'Total_Profit']].to_string(index=False))
    
    # Phân tích RFM
    print("\n--- Phân Khúc Khách Hàng RFM ---")
    rfm = analyzer.calculate_rfm()
    rfm_summary = rfm['Customer_Segment'].value_counts()
    print(rfm_summary.to_string())
    
    # Phân tích giỏ hàng
    print("\n--- Top Cặp Sản Phẩm Thường Mua Cùng ---")
    basket = analyzer.market_basket_analysis(10)
    print(basket.to_string(index=False))
    
    # 4. Hoàn thành
    print("\n" + "=" * 70)
    print("[Bước 4/4] Phân tích hoàn tất!")
    print(f"   Dữ liệu sạch đã lưu tại: data/processed/Superstore_clean.csv")
    print(f"   Để xem Dashboard trực quan: streamlit run app/app.py")
    print("=" * 70)


def run_web_dashboard():
    """Khởi chạy Streamlit Dashboard."""
    import subprocess
    app_path = os.path.join(PROJECT_ROOT, 'app', 'app.py')
    print("Đang khởi chạy Streamlit Dashboard...")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path], cwd=PROJECT_ROOT)


def run_desktop_gui():
    """Khởi chạy giao diện Desktop CustomTkinter."""
    print("Đang khởi chạy giao diện Desktop...")
    from gui import SuperstoreGUI
    app = SuperstoreGUI()
    app.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description='DT04 - Phân Tích Doanh Số Bán Lẻ Chuỗi Siêu Thị'
    )
    parser.add_argument('--web', action='store_true',
                        help='Khởi chạy Streamlit Dashboard')
    parser.add_argument('--gui', action='store_true',
                        help='Khởi chạy giao diện Desktop (CustomTkinter)')
    
    args = parser.parse_args()
    
    if args.web:
        run_web_dashboard()
    elif args.gui:
        run_desktop_gui()
    else:
        run_cli_pipeline()


if __name__ == "__main__":
    main()