import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Render sidebar với bộ lọc dữ liệu.
    
    :param df: DataFrame gốc
    :return: Dictionary chứa các giá trị bộ lọc đã chọn
    """
    with st.sidebar:
        st.markdown("### 🏪 RETAIL BI")
        st.markdown("**Phân Tích Doanh Số Bán Lẻ**")
        st.markdown("---")
        
        st.markdown("#### 🔍 Bộ Lọc Dữ Liệu")
        
        # Lọc theo khu vực
        regions = ['Tất cả'] + sorted(df['Region'].dropna().unique().tolist()) if 'Region' in df.columns else ['Tất cả']
        selected_region = st.selectbox("🌍 Khu vực", regions, key="filter_region")
        
        # Lọc theo danh mục
        categories = ['Tất cả'] + sorted(df['Category'].dropna().unique().tolist()) if 'Category' in df.columns else ['Tất cả']
        selected_category = st.selectbox("📦 Danh mục", categories, key="filter_category")
        
        # Lọc theo phân khúc
        segments = ['Tất cả'] + sorted(df['Segment'].dropna().unique().tolist()) if 'Segment' in df.columns else ['Tất cả']
        selected_segment = st.selectbox("👥 Phân khúc", segments, key="filter_segment")
        
        # Lọc theo thời gian
        if 'Order Date' in df.columns:
            df_dates = pd.to_datetime(df['Order Date'])
            min_date = df_dates.min().date()
            max_date = df_dates.max().date()
            date_range = st.date_input(
                "📅 Khoảng thời gian",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="filter_dates"
            )
        else:
            date_range = None
        
        st.markdown("---")
        st.markdown("*DT04 - Retail Analysis*")
        st.markdown("*Đại học Sư Phạm*")
    
    return {
        'region': selected_region,
        'category': selected_category,
        'segment': selected_segment,
        'date_range': date_range
    }


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Áp dụng các bộ lọc lên DataFrame.
    
    :param df: DataFrame gốc
    :param filters: Dictionary bộ lọc từ render_sidebar()
    :return: DataFrame đã lọc
    """
    filtered = df.copy()
    
    if filters['region'] != 'Tất cả' and 'Region' in filtered.columns:
        filtered = filtered[filtered['Region'] == filters['region']]
    
    if filters['category'] != 'Tất cả' and 'Category' in filtered.columns:
        filtered = filtered[filtered['Category'] == filters['category']]
    
    if filters['segment'] != 'Tất cả' and 'Segment' in filtered.columns:
        filtered = filtered[filtered['Segment'] == filters['segment']]
    
    if filters['date_range'] and 'Order Date' in filtered.columns:
        filtered['Order Date'] = pd.to_datetime(filtered['Order Date'])
        if isinstance(filters['date_range'], tuple) and len(filters['date_range']) == 2:
            start, end = filters['date_range']
            filtered = filtered[
                (filtered['Order Date'].dt.date >= start) & 
                (filtered['Order Date'].dt.date <= end)
            ]
    
    return filtered
