import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional

# Bảng màu thống nhất cho toàn dashboard
COLOR_PALETTE = [
    '#3B82F6', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6',
    '#06B6D4', '#EF4444', '#84CC16', '#F97316', '#6366F1'
]

LAYOUT_DEFAULTS = dict(
    font=dict(family='Arial, sans-serif'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=40, r=40, t=50, b=40),
    hoverlabel=dict(bgcolor='white', font_size=13),
)


class ChartHelper:
    """Lớp hỗ trợ tạo các biểu đồ Plotly tương tác với theme thống nhất."""
    
    @staticmethod
    def bar_chart(df: pd.DataFrame, x: str, y: str, title: str,
                  color: Optional[str] = None, orientation: str = 'v',
                  text_auto: bool = True) -> go.Figure:
        """Tạo biểu đồ cột."""
        if orientation == 'h':
            fig = px.bar(df, x=y, y=x, title=title, color=color,
                        color_discrete_sequence=COLOR_PALETTE, orientation='h',
                        text_auto='.2s' if text_auto else False)
        else:
            fig = px.bar(df, x=x, y=y, title=title, color=color,
                        color_discrete_sequence=COLOR_PALETTE,
                        text_auto='.2s' if text_auto else False)
        fig.update_layout(**LAYOUT_DEFAULTS)
        fig.update_traces(textposition='outside')
        return fig
    
    @staticmethod
    def line_chart(df: pd.DataFrame, x: str, y: str, title: str,
                   color: Optional[str] = None, markers: bool = True) -> go.Figure:
        """Tạo biểu đồ đường."""
        fig = px.line(df, x=x, y=y, title=title, color=color,
                     color_discrete_sequence=COLOR_PALETTE, markers=markers)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
    
    @staticmethod
    def pie_chart(df: pd.DataFrame, names: str, values: str, title: str,
                  hole: float = 0.4) -> go.Figure:
        """Tạo biểu đồ tròn / donut."""
        fig = px.pie(df, names=names, values=values, title=title,
                    color_discrete_sequence=COLOR_PALETTE, hole=hole)
        fig.update_layout(**LAYOUT_DEFAULTS)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def scatter_chart(df: pd.DataFrame, x: str, y: str, title: str,
                      color: Optional[str] = None, size: Optional[str] = None) -> go.Figure:
        """Tạo biểu đồ phân tán."""
        fig = px.scatter(df, x=x, y=y, title=title, color=color, size=size,
                        color_discrete_sequence=COLOR_PALETTE, opacity=0.7)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
    
    @staticmethod
    def heatmap(df: pd.DataFrame, title: str) -> go.Figure:
        """Tạo biểu đồ nhiệt từ pivot table."""
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns.tolist(),
            y=df.index.tolist(),
            colorscale='Blues',
            text=df.values.round(0),
            texttemplate='$%{text:,.0f}',
            textfont={'size': 11},
            hoverongaps=False
        ))
        fig.update_layout(title=title, **LAYOUT_DEFAULTS)
        return fig
    
    @staticmethod
    def area_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
        """Tạo biểu đồ vùng."""
        fig = px.area(df, x=x, y=y, title=title,
                     color_discrete_sequence=COLOR_PALETTE)
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig
