# Mô Tả Dữ Liệu - DT04 (Superstore Sales)

Bộ dữ liệu `Superstore.csv` chứa các thông tin chi tiết về đơn hàng bán lẻ của chuỗi siêu thị.

## Các Trường Dữ Liệu (Columns)

| Tên Cột | Mô Tả | Kiểu Dữ Liệu |
| :--- | :--- | :--- |
| `Order ID` | Mã định danh đơn hàng | Chuỗi (Object) |
| `Order Date` | Ngày đặt hàng | Ngày tháng (YYYY-MM-DD) |
| `Ship Date` | Ngày giao hàng | Ngày tháng (YYYY-MM-DD) |
| `Customer ID` | Mã định danh khách hàng | Chuỗi (Object) |
| `Customer Name` | Tên khách hàng | Chuỗi (Object) |
| `Segment` | Phân khúc khách hàng (Consumer, Corporate, Home Office) | Chuỗi (Object) |
| `Region` | Khu vực địa lý (North, South, East, West) | Chuỗi (Object) |
| `Category` | Danh mục sản phẩm (Furniture, Office Supplies, Technology) | Chuỗi (Object) |
| `Sub-Category` | Danh mục con của sản phẩm | Chuỗi (Object) |
| `Product Name` | Tên cụ thể của sản phẩm | Chuỗi (Object) |
| `Sales` | Tổng doanh số đơn hàng ($) | Số thực (Float) |
| `Quantity` | Số lượng sản phẩm mua | Số nguyên (Integer) |
| `Discount` | Mức tỷ lệ giảm giá (0.0 đến 0.5) | Số thực (Float) |
| `Profit` | Lợi nhuận thu được từ đơn hàng ($) | Số thực (Float) |

## Đánh giá Chất lượng Dữ liệu & Tiền xử lý
- **Quy mô**: Tối thiểu 500+ bản ghi giao dịch (mô phỏng theo Kaggle Superstore Sales).
- **Vấn đề tiềm ẩn**: Giá trị khuyết thiếu (missing values) ở `Sales` và `Profit`, trùng lặp đơn hàng, cần chuẩn hóa kiểu dữ liệu datetime.
