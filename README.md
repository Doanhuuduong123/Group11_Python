# BÀI TẬP LỚN PYTHON: DT04 - PHÂN TÍCH DOANH SỐ BÁN LẺ CHUỖI SIÊU THỊ

**Học phần:** Lập trình Python cho phân tích dữ liệu  
**Ngành:** Công nghệ thông tin - Học kỳ 3, năm học 2025–2026  
**Trường:** Đại học Sư phạm - Đại học Đà Nẵng - Khoa Toán - Tin  
**Mức độ đề tài:** Cơ bản (mở rộng RFM, giỏ hàng, dự báo bán hàng)

## Nhóm thực hiện

| STT | Họ và tên | Mã sinh viên | Lớp |
| --- | --- | --- | --- |
| 1 | **Đoàn Hữu Dương** | 3120225034 | 25CNTT3 |
| 2 | **Nguyễn Huy Bình** | 3120225014 | 25CNTT3 |
| 3 | **Nguyễn Hồ Đại Phong** | 3120225117 | 25CNTT3 |
| 4 | **Nguyễn Bình An** | 3120225003 | 25CNTT3 |
| 5 | **Đỗ Đức Dũng** | 3120225031 | 25CNTT3 |

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Tính năng chính](#tính-năng-chính)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn chạy](#hướng-dẫn-chạy)
- [Dữ liệu và đầu ra](#dữ-liệu-và-đầu-ra)
- [Kiểm thử](#kiểm-thử)
- [Ghi chú quan trọng](#ghi-chú-quan-trọng)

---

## Giới thiệu

Dự án này là một hệ thống phân tích doanh số bán lẻ dành cho chuỗi siêu thị, xây dựng bằng Python.
Nó bao gồm:
- pipeline CLI để xử lý dữ liệu và báo cáo nhanh,
- Streamlit dashboard để trực quan hóa,
- giao diện desktop CustomTkinter,
- logic phân tích OOP tách biệt trong `src/`.

---

## Cấu trúc dự án

```
old_code/
├── README.md
├── requirements.txt
├── main.py
├── gui.py
├── notebook.ipynb
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── kpi_cards.py
│   │   └── sidebar.py
│   └── pages/
│       ├── 1_Overview.py
│       ├── 2_Customer_RFM.py
│       └── 3_Sales_Forecast.py
│
├── data/
│   ├── README.md
│   ├── generate_data.py
│   ├── raw/
│   │   ├── Superstore.csv
│   │   └── Superstore.json
│   ├── processed/
│   └── output/
│
├── outputs/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── retail_analyzer.py
│   └── sales_forecaster.py
│
└── tests/
    ├── __init__.py
    ├── test_data_loader.py
    └── test_retail_analyzer.py
```

---

## Tính năng chính

- Đọc dữ liệu từ `data/raw/Superstore.csv` (hỗ trợ CSV/Excel/JSON/XML)
- Tiền xử lý dữ liệu:
  - xóa trùng lặp,
  - xử lý giá trị thiếu cho `Sales` và `Profit`,
  - chuyển đổi `Order Date` và `Ship Date` sang datetime,
  - trích xuất `Year`, `Month`, `YearMonth`, `Quarter`, `DayOfWeek`
- Phân tích doanh thu/lợi nhuận theo `Category`, `Region`, `YearMonth`, `Quarter`
- Lấy Top sản phẩm và Top khách hàng
- Phân tích RFM và phân khúc khách hàng
- Phân tích giỏ hàng (Market Basket Analysis)
- Phân tích mùa vụ và tác động giảm giá đến lợi nhuận
- Dự báo doanh số theo tháng bằng:
  - SMA (Simple Moving Average),
  - EMA (Exponential Moving Average),
  - Hồi quy tuyến tính (Linear Regression)
- Giao diện sử dụng:
  - CLI (pipeline),
  - Streamlit dashboard,
  - GUI desktop CustomTkinter,
  - Jupyter Notebook hỗ trợ phân tích thêm.

---

## Cài đặt

### Yêu cầu Python
- Python 3.8 hoặc mới hơn

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Thư viện bổ sung nếu dùng GUI

```bash
pip install customtkinter
```

> Lưu ý: `customtkinter` không nằm trong `requirements.txt` hiện tại nên cần cài riêng nếu bạn chạy `python main.py --gui`.

---

## Hướng dẫn chạy

### 1. Chạy pipeline phân tích CLI

```bash
python main.py
```

Kết quả sẽ:
- tải dữ liệu từ `data/raw/Superstore.csv`,
- tiền xử lý và lưu dữ liệu sạch tại `data/processed/Superstore_clean.csv`,
- hiển thị tổng quan, phân tích doanh thu, top sản phẩm, phân tích RFM và phân tích giỏ hàng.

### 2. Chạy Streamlit dashboard

```bash
python main.py --web
```

Hoặc:

```bash
streamlit run app/app.py
```

Menu Streamlit hiện thông tin tổng quan và điều hướng giữa:
- Overview,
- Customer RFM,
- Sales Forecast.

### 3. Chạy giao diện desktop

```bash
python main.py --gui
```

### 4. Chạy Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

### 5. Chạy kiểm thử unit

```bash
python -m pytest tests/ -v
```

---

## Dữ liệu và đầu ra

### Dữ liệu thô

- `data/raw/Superstore.csv`: dữ liệu gốc chính
- `data/raw/Superstore.json`: dữ liệu mẫu JSON tương ứng

### Dữ liệu đã xử lý

- `data/processed/Superstore_clean.csv`: kết quả sau tiền xử lý

### Sinh dữ liệu mẫu

Nếu cần tái tạo dữ liệu, chạy:

```bash
python data/generate_data.py
```

Script này sẽ tạo dataset với 650 bản ghi và lưu về `data/raw/Superstore.csv`.

---

## Kiểm thử

`tests/` gồm các unit test chính:

- `tests/test_data_loader.py`
- `tests/test_retail_analyzer.py`

Chạy tất cả test:

```bash
python -m pytest tests/ -v
```

---

## Mô tả chi tiết từng module

### `main.py`
- Entry point chính của dự án.
- Nếu không truyền tùy chọn, chạy pipeline CLI.
- `--web` khởi chạy Streamlit dashboard.
- `--gui` khởi chạy giao diện desktop.

### `src/data_loader.py`
- Đọc dữ liệu từ file hỗ trợ CSV/Excel/JSON/XML.
- Tiền xử lý, xóa trùng lặp, xử lý NaN, trích xuất trường thời gian.
- Lưu dữ liệu sạch về `data/processed`.
- Cung cấp hàm tóm tắt dữ liệu.

### `src/retail_analyzer.py`
- Phân tích doanh thu, lợi nhuận và số lượng theo nhiều chiều.
- Lấy Top sản phẩm và khách hàng.
- Phân tích seasonality và tác động discount.
- Phân tích khách hàng theo RFM.
- Market Basket Analysis cặp `Sub-Category`.
- Tạo pivot table và phát hiện ngoại lai bằng IQR.

### `src/sales_forecaster.py`
- Dự báo doanh số theo thời gian tháng.
- Gồm SMA, EMA và hồi quy tuyến tính.
- Tính chỉ số MAE, MAPE, RMSE cho đánh giá mô hình.

### `app/app.py`
- Streamlit dashboard chính.
- Load và cache dữ liệu sạch.
- Hiển thị các chỉ số KPI và điều hướng các trang phân tích.

### `gui.py`
- Giao diện desktop CustomTkinter.
- Cho phép lọc theo `Region` và `Category`.
- Hiển thị KPI và biểu đồ nội bộ.

---

## Ghi chú quan trọng

- Nếu `data/raw/Superstore.csv` không tồn tại, hãy tạo lại bằng `python data/generate_data.py` hoặc cung cấp file dữ liệu chính xác.
- Nếu chạy Streamlit mà gặp lỗi, kiểm tra lại đường dẫn `app/app.py` và cài đặt `streamlit`.
- Nếu cần thêm package GUI, cài `customtkinter`.
- `requirements.txt` hiện tại không bao gồm `customtkinter` nên cài riêng cho GUI.

---

## Các lệnh hữu ích

```bash
pip install -r requirements.txt
python main.py
python main.py --web
python main.py --gui
python data/generate_data.py
python -m pytest tests/ -v
```
