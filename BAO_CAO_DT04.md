# CẤU TRÚC VÀ NỘI DUNG BÁO CÁO BÀI TẬP LỚN (BTL)
## ĐỀ TÀI DT04: PHÂN TÍCH DOANH SỐ BÁN LẺ CỦA CHUỖI SIÊU THỊ

---

### TRANG BÌA (Cover Page)
- **TÊN TRƯỜNG:** ĐẠI HỌC SƯ PHẠM - KHOA TOÁN - TIN
- **BÁO CÁO BÀI TẬP LỚN:** LẬP TRÌNH PYTHON CHO PHÂN TÍCH DỮ LIỆU
- **TÊN ĐỀ TÀI (DT04):** PHÂN TÍCH DOANH SỐ BÁN LẺ CỦA CHUỖI SIÊU THỊ
- **GIẢNG VIÊN HƯỚNG DẪN:** [Tên Giảng Viên]
- **DANH SÁCH NHÓM SV:**
  1. Nguyễn Văn A - MSSV: 12345678 (Nhóm trưởng)
  2. Trần Thị B - MSSV: 12345679
  3. Lê Văn C - MSSV: 12345680
- **LỚP HỌC PHẦN:** K7X - CNTT
- **NĂM HỌC:** 2025 - 2026

---

### MỤC LỤC & DANH MỤC HÌNH ẢNH / BẢNG BIỂU

---

### CHƯƠNG 1. GIỚI THIỆU
#### 1.1 Lý do chọn đề tài
Trong thời đại kinh doanh bán lẻ cạnh tranh khốc liệt, việc phân tích dữ liệu bán hàng đóng vai trò sống còn giúp các chuỗi siêu thị tối ưu hóa doanh thu, kiểm soát chi phí và duy trì lòng trung thành của khách hàng. Đề tài DT04 tập trung phân tích bộ dữ liệu bán lẻ nhằm tìm ra các quy luật kinh doanh, tính mùa vụ, và hiệu quả của các chính sách chiết khấu.

#### 1.2 Mục tiêu nghiên cứu
- Tìm hiểu cơ cấu doanh thu và lợi nhuận theo danh mục sản phẩm, khu vực địa lý.
- Phân tích xu hướng mua sắm theo thời gian (tháng, quý, các ngày trong tuần).
- Đánh giá tác động của mức giảm giá (Discount) tới lợi nhuận ròng (Profit).
- Áp dụng các mô hình nâng cao: Phân khúc khách hàng RFM và Phân tích giỏ hàng (Market Basket Analysis).

#### 1.3 Phạm vi nghiên cứu
- Dữ liệu giao dịch siêu thị với hơn 600 bản ghi chi tiết từ năm 2023 - 2024.

#### 1.4 Các câu hỏi phân tích chính
1. *Danh mục sản phẩm nào mang lại doanh thu và lợi nhuận cao nhất?*
2. *Top 10 sản phẩm bán chạy nhất và Top 10 khách hàng VIP là ai?*
3. *Doanh số bán hàng biến động như thế nào theo ngày trong tuần và theo tháng?*
4. *Chính sách giảm giá (Discount) có tác động tích cực hay tiêu cực đến lợi nhuận trung bình?*
5. *Doanh số phân bổ ra sao theo sự kết hợp giữa Danh mục sản phẩm và Khu vực địa lý (Pivot Table)?*
6. *(Nâng cao) Phân khúc khách hàng theo mô hình RFM được thực hiện như thế nào?*
7. *(Nâng cao) Những cặp sản phẩm nào thường được khách hàng mua cùng nhau trong một đơn hàng?*

#### 1.5 Phân công công việc (Bảng phân công nhiệm vụ nhóm)

---

### CHƯƠNG 2. DỮ LIỆU VÀ PHƯƠNG PHÁP NGHIÊN CỨU
#### 2.1 Nguồn dữ liệu & Mô tả các trường dữ liệu
- Nguồn: Tập dữ liệu Superstore Sales (tương đương Kaggle / UCI Online Retail).
- Gồm 14 trường thông tin: `Order ID`, `Order Date`, `Ship Date`, `Customer ID`, `Customer Name`, `Segment`, `Region`, `Category`, `Sub-Category`, `Product Name`, `Sales`, `Quantity`, `Discount`, `Profit`.

#### 2.2 Quy trình Tiền xử lý dữ liệu (Data Preprocessing)
- Lọc bỏ dòng trùng lặp bằng `pandas.drop_duplicates()`.
- Xử lý giá trị khuyết thiếu (NaN) ở cột `Sales` và `Profit`.
- Ép kiểu dữ liệu `Order Date` sang dạng `datetime64`, trích xuất các cột tính toán: `Year`, `Month`, `YearMonth`, `Quarter`, `DayOfWeek`.

#### 2.3 Các thư viện Python sử dụng
- **Pandas & NumPy:** Thao tác, biến đổi và tính toán dữ liệu.
- **Matplotlib & Seaborn:** Trực quan hóa dữ liệu với 5+ loại biểu đồ (Bar chart, Line plot, Heatmap, Pie chart).
- **Itertools & Collections:** Hỗ trợ phân tích tổ hợp giỏ hàng.

---

### CHƯƠNG 3. KẾT QUẢ PHÂN TÍCH DỮ LIỆU
*(Mục này trình bày chi tiết câu trả lời cho 7 câu hỏi phân tích, kèm các Bảng số liệu, Biểu đồ và Diễn giải ý nghĩa)*

#### 3.1 Cơ cấu Doanh thu & Lợi nhuận theo Danh mục Sản phẩm
- Bảng số liệu tổng hợp Doanh số - Lợi nhuận - Tỷ suất lợi nhuận.
- Hình 3.1: Biểu đồ cột tổng doanh số theo Danh mục.
- Diễn giải ý nghĩa kinh doanh.

#### 3.2 Phân tích Top Sản phẩm và Top Khách hàng
- Bảng Top 10 Sản phẩm và Top 10 Khách hàng.
- Hình 3.2: Biểu đồ thanh nằm ngang Top Sản phẩm & Khách hàng.

#### 3.3 Xu hướng Doanh số theo Thời gian & Mùa vụ
- Biến động theo Tháng trong năm và Ngày trong tuần.
- Hình 3.3: Biểu đồ đường (Line Chart) mô tả xu hướng thời gian.

#### 3.4 Đánh giá Tác động của Giảm giá đến Lợi nhuận
- Phân khoảng giảm giá (`0%`, `1-10%`, `11-20%`, `21-30%`, `>30%`).
- Hình 3.4: Biểu đồ tác động của giảm giá đến lợi nhuận ròng.

#### 3.5 Pivot Table Đa chiều & Heatmap
- Bảng Pivot Table gộp 2 chiều `Category` x `Region`.
- Hình 3.5: Heatmap trực quan mức độ tập trung doanh số.

#### 3.6 (Nâng cao) Phân khúc Khách hàng RFM
- Phương pháp tính điểm R (Recency), F (Frequency), M (Monetary).
- Phân nhóm khách hàng: VIP / Champions, Loyal, At Risk, Lost.
- Hình 3.6: Biểu đồ phân bổ tỷ lệ các nhóm khách hàng.

#### 3.7 (Nâng cao) Phân tích Giỏ hàng (Market Basket Analysis)
- Tần suất xuất hiện đồng thời của các cặp danh mục sản phẩm.
- Bảng Top cặp sản phẩm mua kèm nhiều nhất.

---

### CHƯƠNG 4. THIẾT KẾ CHƯƠNG TRÌNH VÀ KIẾN TRÚC MÃ NGUỒN
#### 4.1 Kiến trúc tổng thể hệ thống
Mã nguồn được tổ chức theo lập trình hướng đối tượng (OOP):
- **Lớp `DataLoader` (`src/data_loader.py`):** Đảm nhận việc đọc file, bắt ngoại lệ và tiền xử lý dữ liệu.
- **Lớp `RetailAnalyzer` (`src/retail_analyzer.py`):** Chứa các phương thức xử lý nghiệp vụ phân tích.
- **File `main.py`:** Điểm điều khiển chính chạy toàn bộ chương trình và xuất kết quả.

#### 4.2 Sơ đồ lớp (Class Diagram) & Các hàm chính

---

### CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
#### 5.1 Các phát hiện chính
- Chiết khấu >20% làm âm lợi nhuận.
- Nhóm sản phẩm Công nghệ đóng góp lợi nhuận cao nhất.
- Khách hàng VIP chiếm tỷ trọng doanh số đáng kể.

#### 5.2 Hạn chế của đề tài
- Bộ dữ liệu mô phỏng chưa có yếu tố chi phí vận chuyển chi tiết.

#### 5.3 Hướng phát triển nâng cao
- Xây dựng Dashboard tương tác bằng **Streamlit** hoặc **Plotly Dash**.
- Áp dụng các mô hình Học máy (Machine Learning) để dự báo doanh số (Time Series Forecasting / ARIMA / Prophet).

---

### TÀI LIỆU THAM KHẢO & PHỤ LỤC
1. Tài liệu hướng dẫn học phần Lập trình Python cho Phân tích Dữ liệu.
2. Pandas & Matplotlib Official Documentation.
3. Kaggle Superstore Sales Dataset.
