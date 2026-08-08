import streamlit as st
import pandas as pd
import sys
import os

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src import RetailAnalyzer
from app.components.sidebar import render_sidebar, apply_filters
from app.components.kpi_cards import render_kpi_cards
from app.components.charts import ChartHelper

st.set_page_config(page_title="Tổng Quan Doanh Thu", page_icon="📊", layout="wide")

st.title("📊 Tổng Quan Doanh Thu & Lợi Nhuận")
st.markdown("*Phân tích tổng thể hiệu suất kinh doanh chuỗi siêu thị*")
st.markdown("---")

# Load dữ liệu từ session state
if 'clean_data' not in st.session_state:
    st.warning("⚠️ Vui lòng quay lại trang chính (app.py) để tải dữ liệu trước.")
    st.stop()

df = st.session_state['clean_data']

# Bộ lọc
filters = render_sidebar(df)
df_filtered = apply_filters(df, filters)

if df_filtered.empty:
    st.error("Không có dữ liệu phù hợp với bộ lọc hiện tại!")
    st.stop()

# KPI Cards
render_kpi_cards(df_filtered)
st.markdown("---")

# Khởi tạo analyzer
analyzer = RetailAnalyzer(df_filtered)

# === Row 1: Doanh thu theo Category + Region ===
col1, col2 = st.columns(2)

with col1:
    cat_data = analyzer.analyze_sales_by_dimension('Category')
    fig = ChartHelper.bar_chart(cat_data, x='Category', y='Total_Sales',
                                title='📦 Doanh Thu Theo Danh Mục Sản Phẩm')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'Region' in df_filtered.columns:
        region_data = analyzer.get_region_breakdown()
        fig = ChartHelper.pie_chart(region_data, names='Region', values='Total_Sales',
                                    title='🌍 Phân Bổ Doanh Thu Theo Khu Vực')
        st.plotly_chart(fig, use_container_width=True)

# === Row 2: Xu hướng theo thời gian ===
st.subheader("📈 Xu Hướng Doanh Thu Theo Thời Gian")
monthly = analyzer.get_monthly_sales()
fig = ChartHelper.area_chart(monthly, x='Order Date', y='Sales',
                              title='Doanh Thu Hàng Tháng')
st.plotly_chart(fig, use_container_width=True)

# === Row 3: Top sản phẩm + Heatmap ===
col3, col4 = st.columns(2)

with col3:
    top_products, _ = analyzer.get_top_performers(10)
    fig = ChartHelper.bar_chart(top_products, x='Product Name', y='Total_Sales',
                                title='🏆 Top 10 Sản Phẩm Doanh Thu Cao Nhất',
                                orientation='h')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    if 'Region' in df_filtered.columns:
        pivot = analyzer.create_multidimensional_pivot('Category', 'Region')
        fig = ChartHelper.heatmap(pivot, title='🗺️ Heatmap Doanh Số: Category × Region')
        st.plotly_chart(fig, use_container_width=True)

# === Row 4: Tác động giảm giá ===
st.subheader("💸 Tác Động Của Giảm Giá Đến Lợi Nhuận")
if 'Discount' in df_filtered.columns and 'Profit' in df_filtered.columns:
    fig = ChartHelper.scatter_chart(df_filtered, x='Discount', y='Profit',
                                     title='Scatter: Giảm Giá vs Lợi Nhuận',
                                     color='Category' if 'Category' in df_filtered.columns else None)
    fig.add_hline(y=0, line_dash='dash', line_color='red',
                  annotation_text='Ranh giới hòa vốn')
    st.plotly_chart(fig, use_container_width=True)

# === Bảng dữ liệu chi tiết ===
with st.expander("📋 Xem Dữ Liệu Chi Tiết", expanded=False):
    display_cols = [c for c in ['Order ID', 'Order Date', 'Customer Name', 'Category',
                                'Sub-Category', 'Region', 'Sales', 'Profit', 'Discount']
                   if c in df_filtered.columns]
    st.dataframe(df_filtered[display_cols].head(200), use_container_width=True, height=400)
