# BÀI TẬP LỚN PYTHON: ĐỀ TÀI DT04 - PHÂN TÍCH DOANH SỐ BÁN LẺ CHUỖI SIÊU THỊ

**Học phần:** Lập trình Python cho phân tích dữ liệu  
**Ngành:** Công nghệ thông tin - Học kỳ 3, năm học 2025–2026  
**Trường:** Đại học Sư phạm - Khoa Toán - Tin  
**Mức độ đề tài:** Cơ bản (có mở rộng Phân tích nâng cao RFM, Giỏ hàng & Dự báo bán hàng)

---

## 1. Cấu Trúc Mã Nguồn Dự Án

```
DT04_Retail_Analysis/
├── .gitignore
├── README.md                          # Hướng dẫn cài đặt và chạy chương trình
├── requirements.txt                   # Danh sách thư viện sử dụng
├── BAO_CAO_DT04.md                    # Dàn ý báo cáo BTL
│
├── app/                               # 🌐 Streamlit Dashboard (Web)
│   ├── app.py                         # Entry point: streamlit run app/app.py
│   ├── components/
│   │   ├── __init__.py                # Export các component chung
│   │   ├── sidebar.py                 # Bộ lọc dữ liệu
│   │   ├── kpi_cards.py               # Thẻ chỉ số KPI
│   │   └── charts.py                  # Hàm vẽ biểu đồ Plotly
│   └── pages/
│       ├── 1_Overview.py              # Tổng quan doanh thu
│       ├── 2_Customer_RFM.py          # Phân tích RFM khách hàng
│       └── 3_Sales_Forecast.py        # Dự báo bán hàng
│
├── src/                               # 🧠 Core Business Logic (OOP)
│   ├── __init__.py                    # Export classes
│   ├── data_loader.py                 # Lớp DataLoader: tải, làm sạch dữ liệu
│   ├── retail_analyzer.py             # Lớp RetailAnalyzer: phân tích nghiệp vụ
│   └── sales_forecaster.py            # Lớp SalesForecaster: dự báo bán hàng
│
├── data/
│   ├── raw/
│   │   ├── Superstore.csv             # Dữ liệu gốc (>600 bản ghi)
│   │   └── Superstore.json            # Dữ liệu đầu vào định dạng JSON
│   ├── processed/                     # Dữ liệu đã tiền xử lý
│   ├── output/                        # Kết quả xuất
│   ├── generate_data.py               # Script sinh dữ liệu
│   └── README.md                      # Mô tả các trường dữ liệu
│
├── outputs/                           # Biểu đồ matplotlib đã xuất
├── gui.py                             # 🖥️ Giao diện Desktop (CustomTkinter)
├── main.py                            # Entry point chính (CLI/Web/GUI)
├── notebook.ipynb                     # Jupyter Notebook phân tích
│
└── tests/                             # ✅ Unit Tests
    ├── test_data_loader.py
    └── test_retail_analyzer.py
```

---

## 2. Hướng Dẫn Cài Đặt & Chạy Chương Trình

### 2.1 Cài đặt môi trường & thư viện
Yêu cầu Python version >= 3.8:

```bash
pip install -r requirements.txt
```

### 2.2 Chạy Pipeline Phân Tích (CLI)
Thực thi toàn bộ quy trình tiền xử lý → phân tích → xuất kết quả:

```bash
python main.py
```

### 2.3 Khởi chạy Streamlit Dashboard (Web)
Mở dashboard trực quan trên trình duyệt:

```bash
python main.py --web
# hoặc 
streamlit run app/app.py trực tiếp:

```

### 2.4 Khởi chạy Giao Diện Desktop (CustomTkinter)
```bash
python main.py --gui
```

### 2.5 Chạy Jupyter Notebook
```bash
jupyter notebook notebook.ipynb
```

### 2.6 Chạy Unit Tests
```bash
python -m pytest tests/ -v
```

### 2.7 Định dạng dữ liệu được hỗ trợ
- CSV: `pd.read_csv`
- Excel: `pd.read_excel`
- JSON: `pd.read_json`
- XML: `pd.read_xml`

---

## 3. Tóm Tắt Kết Quả & Yêu Cầu Đã Hoàn Thành

| Yêu Cầu Đề Bài | Trạng Thái | Mô Tả Thực Hiện |
| :--- | :---: | :--- |
| Dữ liệu > 500 bản ghi | **✅ Hoàn thành** | Tập dữ liệu `Superstore.csv` có 650 bản ghi giao dịch. |
| Đọc & Tiền xử lý dữ liệu | **✅ Hoàn thành** | Ép kiểu Datetime, điền NaN, lọc trùng lặp qua lớp `DataLoader`. |
| Tối thiểu 5 câu hỏi & 5 biểu đồ | **✅ Hoàn thành** | 7 câu hỏi phân tích, 8+ biểu đồ tương tác (Plotly). |
| Tổ chức mã theo OOP | **✅ Hoàn thành** | 3 lớp: `DataLoader`, `RetailAnalyzer`, `SalesForecaster`. |
| Nâng cao 1: Phân tích RFM | **✅ Hoàn thành** | Phân khúc khách hàng: Champions, Loyal, At Risk, Lost. |
| Nâng cao 2: Giỏ hàng (Basket) | **✅ Hoàn thành** | Phân tích cặp sản phẩm thường mua cùng nhau. |
| Nâng cao 3: Dự báo bán hàng | **✅ Hoàn thành** | SMA, EMA, Linear Regression với metrics (MAE, MAPE, RMSE). |
| Dashboard tương tác | **✅ Hoàn thành** | Streamlit multi-page dashboard + Desktop GUI (CustomTkinter). |
| Unit Tests | **✅ Hoàn thành** | Pytest test suite cho DataLoader và RetailAnalyzer. |
