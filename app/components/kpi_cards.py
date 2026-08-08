import streamlit as st
import pandas as pd


def render_kpi_cards(df: pd.DataFrame):
    """
    Hiển thị 4 thẻ chỉ số KPI chính.
    
    :param df: DataFrame đã lọc
    """
    total_sales = df['Sales'].sum() if 'Sales' in df.columns else 0
    total_profit = df['Profit'].sum() if 'Profit' in df.columns else 0
    total_orders = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Tổng Doanh Thu",
            value=f"${total_sales:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="📈 Tổng Lợi Nhuận",
            value=f"${total_profit:,.0f}",
            delta=f"{profit_margin:.1f}% margin"
        )
    
    with col3:
        st.metric(
            label="🛒 Tổng Đơn Hàng",
            value=f"{total_orders:,}",
            delta=None
        )
    
    with col4:
        avg_order = total_sales / total_orders if total_orders > 0 else 0
        st.metric(
            label="💵 TB / Đơn Hàng",
            value=f"${avg_order:,.0f}",
            delta=None
        )
