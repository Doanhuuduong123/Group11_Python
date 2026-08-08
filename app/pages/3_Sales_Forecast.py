import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src import RetailAnalyzer, SalesForecaster
from app.components.charts import COLOR_PALETTE

st.set_page_config(page_title="Dự Báo Bán Hàng", page_icon="🔮", layout="wide")

st.title("🔮 Dự Báo Doanh Số Bán Hàng")
st.markdown("*Dự báo xu hướng doanh thu sử dụng Moving Average & Linear Regression*")
st.markdown("---")

if 'clean_data' not in st.session_state:
    st.warning("⚠️ Vui lòng quay lại trang chính (app.py) để tải dữ liệu trước.")
    st.stop()

df = st.session_state['clean_data']
analyzer = RetailAnalyzer(df)
monthly = analyzer.get_monthly_sales()

if len(monthly) < 3:
    st.error("Không đủ dữ liệu để dự báo (cần ít nhất 3 tháng).")
    st.stop()

forecaster = SalesForecaster(monthly)

# === Cấu hình dự báo ===
st.subheader("⚙️ Cấu Hình Dự Báo")
col1, col2, col3 = st.columns(3)

with col1:
    method = st.selectbox("Phương pháp dự báo", ['SMA (Trung bình trượt)', 'EMA (Trung bình mũ)', 'Linear Regression'])

with col2:
    if 'SMA' in method:
        window = st.slider("Cửa sổ SMA (tháng)", 2, min(12, len(monthly)), 3)
    elif 'EMA' in method:
        alpha = st.slider("Hệ số Alpha", 0.1, 0.9, 0.3, 0.05)

with col3:
    n_forecast = st.slider("Số tháng dự báo", 1, 6, 3)

st.markdown("---")

# === Tính toán ===
if 'SMA' in method:
    method_key = 'sma'
    historical = forecaster.simple_moving_average(window)
    forecast = forecaster.forecast_next_periods(n_forecast, 'sma', window=window)
    metrics = forecaster.get_forecast_metrics('sma', window=window)
    pred_col = 'SMA'
elif 'EMA' in method:
    method_key = 'ema'
    historical = forecaster.exponential_moving_average(alpha)
    forecast = forecaster.forecast_next_periods(n_forecast, 'ema', alpha=alpha)
    metrics = forecaster.get_forecast_metrics('ema', alpha=alpha)
    pred_col = 'EMA'
else:
    method_key = 'linear'
    historical, forecast = forecaster.linear_regression_forecast(n_forecast)
    metrics = forecaster.get_forecast_metrics('linear')
    pred_col = 'Trend'
    forecast = forecast.rename(columns={'Forecast_Sales': 'Forecast'})

# === KPI Metrics ===
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("📊 MAE", f"${metrics['MAE']:,.0f}", help="Mean Absolute Error - Sai số tuyệt đối trung bình")
with col_b:
    st.metric("📉 MAPE", f"{metrics['MAPE']:.1f}%", help="Mean Absolute Percentage Error - Sai số phần trăm trung bình")
with col_c:
    st.metric("📏 RMSE", f"${metrics['RMSE']:,.0f}", help="Root Mean Square Error - Căn bậc hai sai số bình phương trung bình")

st.markdown("---")

# === Biểu đồ dự báo ===
st.subheader("📈 Biểu Đồ Doanh Thu Thực Tế & Dự Báo")

fig = go.Figure()

# Doanh thu thực tế
fig.add_trace(go.Scatter(
    x=historical['Order Date'], y=historical['Sales'],
    name='Doanh thu thực tế', mode='lines+markers',
    line=dict(color=COLOR_PALETTE[0], width=2.5),
    marker=dict(size=6)
))

# Đường dự báo trên dữ liệu lịch sử
fig.add_trace(go.Scatter(
    x=historical['Order Date'], y=historical[pred_col],
    name=f'{method.split(" (")[0]} (Fitted)', mode='lines',
    line=dict(color=COLOR_PALETTE[1], width=2, dash='dash')
))

# Dự báo tương lai
forecast_col = 'Forecast' if 'Forecast' in forecast.columns else 'Forecast_Sales'
fig.add_trace(go.Scatter(
    x=forecast['Order Date'], y=forecast[forecast_col],
    name='Dự báo tương lai', mode='lines+markers',
    line=dict(color=COLOR_PALETTE[2], width=2.5, dash='dot'),
    marker=dict(size=8, symbol='star')
))

fig.update_layout(
    title=f'Dự Báo Doanh Thu - {method}',
    xaxis_title='Thời gian',
    yaxis_title='Doanh thu ($)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# === Bảng dự báo ===
st.subheader("📋 Bảng Kết Quả Dự Báo")
col_x, col_y = st.columns(2)

with col_x:
    st.markdown("**Dữ liệu lịch sử (5 tháng gần nhất)**")
    recent = historical[['Order Date', 'Sales', pred_col]].tail(5).copy()
    recent['Order Date'] = recent['Order Date'].dt.strftime('%Y-%m')
    recent.columns = ['Tháng', 'Doanh Thu Thực', f'Dự Báo ({pred_col})']
    st.dataframe(recent.reset_index(drop=True), use_container_width=True)

with col_y:
    st.markdown("**Dự báo các tháng tới**")
    forecast_display = forecast.copy()
    forecast_display['Order Date'] = forecast_display['Order Date'].dt.strftime('%Y-%m')
    forecast_display = forecast_display.rename(columns={
        'Order Date': 'Tháng',
        forecast_col: 'Doanh Thu Dự Báo'
    })
    display_cols = ['Tháng', 'Doanh Thu Dự Báo']
    st.dataframe(forecast_display[display_cols].reset_index(drop=True), use_container_width=True)

# === Giải thích phương pháp ===
with st.expander("ℹ️ Giải thích các phương pháp dự báo"):
    st.markdown("""
    ### Simple Moving Average (SMA)
    - Tính trung bình cộng của N tháng gần nhất
    - **Ưu điểm:** Đơn giản, dễ hiểu
    - **Nhược điểm:** Phản ứng chậm với thay đổi
    
    ### Exponential Moving Average (EMA)
    - Trung bình có trọng số, dữ liệu mới có trọng số cao hơn
    - **Alpha cao** → phản ứng nhanh, **Alpha thấp** → mượt mà hơn
    
    ### Linear Regression
    - Tìm đường thẳng xu hướng tốt nhất (best fit line)
    - **Ưu điểm:** Phát hiện xu hướng dài hạn
    - **Nhược điểm:** Giả định xu hướng tuyến tính
    """)
