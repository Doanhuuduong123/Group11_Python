import streamlit as st
import sys
import os

# Thêm thư mục gốc dự án vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src import DataLoader

# === Cấu hình trang ===
st.set_page_config(
    page_title="DT04 - Retail BI Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Custom CSS ===
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stMetric"] {
        background-color: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 15px 20px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
    }
    div[data-testid="stExpander"] {
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_and_process_data():
    """Tải và xử lý dữ liệu, cache để tối ưu hiệu năng."""
    loader = DataLoader()
    loader.load_data()
    clean_df = loader.preprocess()
    return clean_df


def main():
    # === Header ===
    st.title("🏪 DT04 - Retail Business Intelligence Dashboard")
    st.markdown(
        "**Phân Tích Doanh Số Bán Lẻ Chuỗi Siêu Thị** | "
        "*Đại học Sư Phạm - Khoa Toán - Tin*"
    )
    st.markdown("---")

    # === Load Data ===
    try:
        with st.spinner("🔄 Đang tải và xử lý dữ liệu..."):
            clean_df = load_and_process_data()
            st.session_state['clean_data'] = clean_df
        
        st.success(f"✅ Dữ liệu đã sẵn sàng: **{len(clean_df):,}** bản ghi | **{clean_df['Order ID'].nunique():,}** đơn hàng")
    except Exception as e:
        st.error(f"❌ Lỗi khi tải dữ liệu: {e}")
        st.info("Hãy đảm bảo file `data/raw/Superstore.csv` tồn tại.")
        st.stop()

    # === Hướng dẫn điều hướng ===
    st.markdown("### 📌 Điều Hướng")
    st.markdown("""
    Sử dụng **sidebar bên trái** để chuyển giữa các trang phân tích:
    
    | Trang | Mô tả |
    |---|---|
    | 📊 **Overview** | Tổng quan doanh thu, lợi nhuận, biểu đồ phân tích |
    | 👥 **Customer RFM** | Phân tích phân khúc khách hàng theo mô hình RFM |
    | 🔮 **Sales Forecast** | Dự báo doanh số bán hàng (SMA, EMA, Linear Regression) |
    """)
    
    # === Thông tin nhanh ===
    st.markdown("### 📊 Thông Tin Nhanh")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Tổng Doanh Thu", f"${clean_df['Sales'].sum():,.0f}")
    with col2:
        st.metric("📈 Tổng Lợi Nhuận", f"${clean_df['Profit'].sum():,.0f}")
    with col3:
        st.metric("🛒 Tổng Đơn Hàng", f"{clean_df['Order ID'].nunique():,}")
    with col4:
        st.metric("👤 Khách Hàng", f"{clean_df['Customer ID'].nunique():,}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 12px;'>"
        "DT04 - Phân Tích Doanh Số Bán Lẻ | Đề tài BTL Python | 2025-2026"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
