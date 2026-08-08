import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src import RetailAnalyzer
from app.components.charts import ChartHelper, COLOR_PALETTE

st.set_page_config(page_title="Phân Tích RFM", page_icon="👥", layout="wide")

st.title("👥 Phân Tích Phân Khúc Khách Hàng (RFM)")
st.markdown("*Phân tích Recency - Frequency - Monetary để phân loại khách hàng*")
st.markdown("---")

if 'clean_data' not in st.session_state:
    st.warning("⚠️ Vui lòng quay lại trang chính (app.py) để tải dữ liệu trước.")
    st.stop()

df = st.session_state['clean_data']

# Giải thích RFM
with st.expander("ℹ️ Mô hình RFM là gì?", expanded=False):
    st.markdown("""
    **RFM** là mô hình phân khúc khách hàng dựa trên 3 chỉ số:
    - **R (Recency):** Số ngày kể từ lần mua gần nhất → Càng nhỏ càng tốt
    - **F (Frequency):** Số lần mua hàng → Càng lớn càng tốt  
    - **M (Monetary):** Tổng giá trị chi tiêu → Càng lớn càng tốt
    
    | Phân Khúc | Điểm RFM | Mô tả |
    |---|---|---|
    | 🏆 VIP / Champions | ≥ 10 | Khách hàng tốt nhất, mua thường xuyên |
    | 💎 Loyal Customers | 7-9 | Khách hàng trung thành |
    | ⚠️ At Risk / Potential | 5-6 | Có nguy cơ rời bỏ hoặc tiềm năng phát triển |
    | ❌ Lost / Inactive | < 5 | Khách hàng đã ngừng mua |
    """)

# Tính toán RFM
analyzer = RetailAnalyzer(df)
rfm = analyzer.calculate_rfm()

# === KPI ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👤 Tổng Khách Hàng", f"{len(rfm):,}")
with col2:
    vip_count = len(rfm[rfm['Customer_Segment'] == 'VIP / Champions'])
    st.metric("🏆 Khách VIP", f"{vip_count:,}")
with col3:
    avg_monetary = rfm['Monetary'].mean()
    st.metric("💰 TB Chi Tiêu", f"${avg_monetary:,.0f}")
with col4:
    at_risk = len(rfm[rfm['Customer_Segment'] == 'At Risk / Potential'])
    st.metric("⚠️ Có Nguy Cơ", f"{at_risk:,}")

st.markdown("---")

# === Charts ===
col_a, col_b = st.columns(2)

with col_a:
    segment_counts = rfm['Customer_Segment'].value_counts().reset_index()
    segment_counts.columns = ['Phân Khúc', 'Số Lượng']
    fig = ChartHelper.pie_chart(segment_counts, names='Phân Khúc', values='Số Lượng',
                                title='📊 Phân Bổ Tỷ Lệ Các Phân Khúc Khách Hàng')
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig = px.scatter(rfm, x='Recency', y='Monetary', size='Frequency',
                    color='Customer_Segment', title='🔍 Scatter: Recency vs Monetary',
                    color_discrete_sequence=COLOR_PALETTE,
                    hover_data=['Customer ID'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# === Phân tích theo từng nhóm ===
st.subheader("📋 Chi Tiết Từng Phân Khúc")

segments = rfm['Customer_Segment'].unique()
selected_segment = st.selectbox("Chọn phân khúc để xem chi tiết:", segments)

seg_data = rfm[rfm['Customer_Segment'] == selected_segment]

col_c, col_d, col_e = st.columns(3)
with col_c:
    st.metric("Số khách hàng", f"{len(seg_data):,}")
with col_d:
    st.metric("TB Recency (ngày)", f"{seg_data['Recency'].mean():.0f}")
with col_e:
    st.metric("TB Monetary ($)", f"${seg_data['Monetary'].mean():,.0f}")

# Bảng chi tiết
st.dataframe(
    seg_data[['Customer ID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Segment']]
    .sort_values('RFM_Score', ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
    height=400
)
