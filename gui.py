import os
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Import mô-đun phân tích từ dự án
try:
    from src.retail_analyzer import RetailAnalyzer
except ImportError:
    RetailAnalyzer = None

# Thiết lập theme mặc định
ctk.set_appearance_mode("Dark")  # Mặc định giao diện Tối hiện đại
ctk.set_default_color_theme("blue")

class SuperstoreGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Superstore Business Intelligence Dashboard")
        self.geometry("1280x800")
        self.minsize(1100, 700)

        # Đường dẫn file dữ liệu (Cập nhật đọc dữ liệu đã làm sạch)
        self.data_path = os.path.join("data", "processed", "Superstore_clean.csv")
        self.df_raw = None
        self.df_filtered = None
        self.current_canvas = None
        self.current_view = "kpi"  # kpi, chart_cat, chart_top, chart_trend, chart_discount, data

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Cấu hình Layout 2 cột chính (Sidebar & Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================== 1. SIDEBAR ====================
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text=" RETAIL BI", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 20), sticky="w")

        # Subtitle
        sub_label = ctk.CTkLabel(self.sidebar, text="Menu Điều Hướng", font=ctk.CTkFont(size=12), text_color="gray")
        sub_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # Navigation Buttons
        self.btn_kpi = ctk.CTkButton(
            self.sidebar, text=" Tổng Quan KPI", anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=lambda: self.switch_view("kpi")
        )
        self.btn_kpi.grid(row=2, column=0, padx=15, pady=6, sticky="ew")

        self.btn_cat = ctk.CTkButton(
            self.sidebar, text=" Doanh Thu Ngành Hàng", anchor="w",
            font=ctk.CTkFont(size=14), height=38, fg_color="transparent", text_color=("gray10", "gray90"),
            command=lambda: self.switch_view("chart_cat")
        )
        self.btn_cat.grid(row=3, column=0, padx=15, pady=6, sticky="ew")

        self.btn_top = ctk.CTkButton(
            self.sidebar, text=" Top 10 Sản Phẩm", anchor="w",
            font=ctk.CTkFont(size=14), height=38, fg_color="transparent", text_color=("gray10", "gray90"),
            command=lambda: self.switch_view("chart_top")
        )
        self.btn_top.grid(row=4, column=0, padx=15, pady=6, sticky="ew")

        self.btn_trend = ctk.CTkButton(
            self.sidebar, text=" Xu Hướng Theo Thời Gian", anchor="w",
            font=ctk.CTkFont(size=14), height=38, fg_color="transparent", text_color=("gray10", "gray90"),
            command=lambda: self.switch_view("chart_trend")
        )
        self.btn_trend.grid(row=5, column=0, padx=15, pady=6, sticky="ew")

        self.btn_disc = ctk.CTkButton(
            self.sidebar, text=" Phân Tích Giảm Giá", anchor="w",
            font=ctk.CTkFont(size=14), height=38, fg_color="transparent", text_color=("gray10", "gray90"),
            command=lambda: self.switch_view("chart_discount")
        )
        self.btn_disc.grid(row=6, column=0, padx=15, pady=6, sticky="ew")

        self.btn_data = ctk.CTkButton(
            self.sidebar, text=" Tra Cứu Dữ Liệu", anchor="w",
            font=ctk.CTkFont(size=14), height=38, fg_color="transparent", text_color=("gray10", "gray90"),
            command=lambda: self.switch_view("data")
        )
        self.btn_data.grid(row=7, column=0, padx=15, pady=6, sticky="ew")

        # Theme Selector at Bottom Sidebar
        self.theme_label = ctk.CTkLabel(self.sidebar, text="Giao diện:", font=ctk.CTkFont(size=12))
        self.theme_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="sw")
        
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar, values=["Dark", "Light", "System"],
            command=self.change_theme
        )
        self.theme_menu.grid(row=10, column=0, padx=15, pady=(5, 20), sticky="ew")

        # ==================== 2. MAIN CONTAINER ====================
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # --- Top Filter Bar ---
        self.filter_bar = ctk.CTkFrame(self.main_container, height=60, corner_radius=12)
        self.filter_bar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.filter_bar.grid_columnconfigure(5, weight=1)

        ctk.CTkLabel(self.filter_bar, text=" Bộ Lọc:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=(15, 5), pady=12)

        # Region Filter
        ctk.CTkLabel(self.filter_bar, text="Khu vực:").grid(row=0, column=1, padx=(10, 5))
        self.region_opt = ctk.CTkOptionMenu(self.filter_bar, values=["Tất cả"], width=130, command=self.apply_filter)
        self.region_opt.grid(row=0, column=2, padx=(0, 15))

        # Category Filter
        ctk.CTkLabel(self.filter_bar, text="Danh mục:").grid(row=0, column=3, padx=(10, 5))
        self.category_opt = ctk.CTkOptionMenu(self.filter_bar, values=["Tất cả"], width=150, command=self.apply_filter)
        self.category_opt.grid(row=0, column=4, padx=(0, 15))

        # Reset Filter Button
        self.btn_reset = ctk.CTkButton(self.filter_bar, text="Đặt lại", width=80, fg_color="gray40", hover_color="gray30", command=self.reset_filter)
        self.btn_reset.grid(row=0, column=5, padx=15, sticky="e")

        # --- Dynamic View Area ---
        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def load_data(self):
        """Tải dữ liệu bằng pandas"""
        try:
            if not os.path.exists(self.data_path):
                # Thử tìm ở thư mục cha nếu chạy từ góc khác
                self.data_path = os.path.join("..", "data", "processed", "Superstore_clean.csv")

            self.df_raw = pd.read_csv(self.data_path)
            self.df_filtered = self.df_raw.copy()

            # Nạp dữ liệu cho combobox bộ lọc
            if 'Region' in self.df_raw.columns:
                regions = ["Tất cả"] + sorted(list(self.df_raw['Region'].dropna().unique()))
                self.region_opt.configure(values=regions)

            if 'Category' in self.df_raw.columns:
                categories = ["Tất cả"] + sorted(list(self.df_raw['Category'].dropna().unique()))
                self.category_opt.configure(values=categories)

            self.render_current_view()

        except Exception as e:
            messagebox.showerror("Lỗi dữ liệu", f"Không thể đọc file Superstore.csv:\n{e}")

    def apply_filter(self, _=None):
        """Lọc dữ liệu dựa trên các lựa chọn"""
        if self.df_raw is None:
            return

        df = self.df_raw.copy()
        selected_region = self.region_opt.get()
        selected_cat = self.category_opt.get()

        if selected_region != "Tất cả" and 'Region' in df.columns:
            df = df[df['Region'] == selected_region]

        if selected_cat != "Tất cả" and 'Category' in df.columns:
            df = df[df['Category'] == selected_cat]

        self.df_filtered = df
        self.render_current_view()

    def reset_filter(self):
        self.region_opt.set("Tất cả")
        self.category_opt.set("Tất cả")
        self.apply_filter()

    def change_theme(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        # Re-render để cập nhật màu đồ thị theo theme mới
        self.after(200, self.render_current_view)

    def switch_view(self, view_name):
        self.current_view = view_name
        
        # Reset màu button sidebar
        buttons = [
            ("kpi", self.btn_kpi),
            ("chart_cat", self.btn_cat),
            ("chart_top", self.btn_top),
            ("chart_trend", self.btn_trend),
            ("chart_discount", self.btn_disc),
            ("data", self.btn_data)
        ]

        for v_id, btn in buttons:
            if v_id == view_name:
                btn.configure(fg_color=("tab_accent", "brand_blue") if hasattr(ctk, "brand_blue") else "#1F6AA5", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"), font=ctk.CTkFont(size=14))

        self.render_current_view()

    def clear_content(self):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def render_current_view(self):
        self.clear_content()

        if self.df_filtered is None or self.df_filtered.empty:
            ctk.CTkLabel(self.content_frame, text="Không có dữ liệu phù hợp với bộ lọc!", font=ctk.CTkFont(size=16)).pack(expand=True)
            return

        if self.current_view == "kpi":
            self.show_kpi_dashboard()
        elif self.current_view == "chart_cat":
            self.plot_category_sales()
        elif self.current_view == "chart_top":
            self.plot_top_products()
        elif self.current_view == "chart_trend":
            self.plot_sales_trend()
        elif self.current_view == "chart_discount":
            self.plot_discount_profit()
        elif self.current_view == "data":
            self.show_data_table()

    # ==================== VIEW 1: KPI DASHBOARD ====================
    def show_kpi_dashboard(self):
        df = self.df_filtered

        # Tính toán các chỉ số
        total_sales = df['Sales'].sum() if 'Sales' in df.columns else 0
        total_profit = df['Profit'].sum() if 'Profit' in df.columns else 0
        total_orders = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
        profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

        # Title
        header = ctk.CTkLabel(self.content_frame, text="TỔNG QUAN HIỆU SUẤT KINH DOANH", font=ctk.CTkFont(size=20, weight="bold"))
        header.pack(pady=(25, 10))

        # Grid chứa các Card KPI
        kpi_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        kpi_grid.pack(fill="x", padx=30, pady=20)
        kpi_grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")

        # Utility tạo Card
        def create_kpi_card(col, title, value, subtext, color_theme):
            card = ctk.CTkFrame(kpi_grid, corner_radius=15, border_width=1, border_color=("gray70", "gray30"))
            card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="normal"), text_color="gray").pack(pady=(18, 5))
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"), text_color=color_theme).pack(pady=2)
            ctk.CTkLabel(card, text=subtext, font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(2, 18))

        create_kpi_card(0, "Tổng Doanh Thu", f"${total_sales:,.2f}", " Toàn bộ đơn hàng", "#3B82F6")
        create_kpi_card(1, "Tổng Lợi Nhuận", f"${total_profit:,.2f}", " Lợi nhuận ròng", "#10B981" if total_profit >= 0 else "#EF4444")
        create_kpi_card(2, "Tỷ Lệ Lợi Nhuận", f"{profit_margin:.1f}%", " Profit / Sales", "#8B5CF6")
        create_kpi_card(3, "Tổng Đơn Hàng", f"{total_orders:,}", " Mã đơn duy nhất", "#F59E0B")

        # Thêm bảng thông tin tóm tắt nhanh bên dưới
        summary_box = ctk.CTkFrame(self.content_frame, corner_radius=12)
        summary_box.pack(fill="both", expand=True, padx=40, pady=(10, 30))

        ctk.CTkLabel(summary_box, text=" Thông Tin Phân Tích Nhanh", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        avg_order_value = total_sales / total_orders if total_orders > 0 else 0
        discount_avg = df['Discount'].mean() * 100 if 'Discount' in df.columns else 0

        info_text = (
            f"• Giá trị trung bình mỗi đơn hàng (AOV): ${avg_order_value:,.2f}\n"
            f"• Mức giảm giá trung bình đang áp dụng: {discount_avg:.1f}%\n"
            f"• Tổng số mặt hàng kinh doanh ghi nhận trong bộ lọc: {len(df):,} dòng dữ liệu."
        )
        ctk.CTkLabel(summary_box, text=info_text, font=ctk.CTkFont(size=14), justify="left", anchor="w").pack(anchor="w", padx=20, pady=10)

    # ==================== HOÀN THIỆN ĐỒ THỊ MATPLOTLIB ====================
    def get_matplotlib_theme(self):
        """Lấy cấu hình màu sắc Matplotlib khớp với Theme ứng dụng"""
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return {
                'bg': '#2B2B2B',
                'fg': '#FFFFFF',
                'grid': '#404040',
                'accent': '#3B82F6',
                'bar_colors': ['#3B82F6', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6']
            }
        else:
            return {
                'bg': '#F9FAFB',
                'fg': '#111827',
                'grid': '#E5E7EB',
                'accent': '#2563EB',
                'bar_colors': ['#2563EB', '#059669', '#D97706', '#DB2777', '#7C3AED']
            }

    def render_fig(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        self.current_canvas = canvas

    def plot_category_sales(self):
        df = self.df_filtered
        if 'Category' not in df.columns or 'Sales' not in df.columns:
            return

        theme = self.get_matplotlib_theme()
        data = df.groupby('Category')['Sales'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=theme['bg'])
        ax.set_facecolor(theme['bg'])

        bars = ax.bar(data['Category'], data['Sales'], color=theme['bar_colors'][:len(data)], width=0.5)

        # Annotations
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'${height:,.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', color=theme['fg'], fontsize=10, fontweight='bold')

        ax.set_title("DOANH THU THEO DANH MỤC SẢN PHẨM", color=theme['fg'], fontsize=14, pad=15, fontweight='bold')
        ax.tick_params(colors=theme['fg'], labelsize=11)
        ax.spines['bottom'].set_color(theme['grid'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.yaxis.grid(True, linestyle='--', color=theme['grid'], alpha=0.7)

        fig.tight_layout()
        self.render_fig(fig)

    def plot_top_products(self):
        df = self.df_filtered
        if 'Product Name' not in df.columns or 'Sales' not in df.columns:
            return

        theme = self.get_matplotlib_theme()
        top_p = df.groupby('Product Name')['Sales'].sum().nlargest(10).sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=theme['bg'])
        ax.set_facecolor(theme['bg'])

        top_p.plot(kind='barh', ax=ax, color=theme['accent'], width=0.6)

        ax.set_title("TOP 10 SẢN PHẨM CÓ DOANH THU CAO NHẤT", color=theme['fg'], fontsize=14, pad=15, fontweight='bold')
        ax.tick_params(colors=theme['fg'], labelsize=10)
        ax.xaxis.grid(True, linestyle='--', color=theme['grid'], alpha=0.7)
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout()
        self.render_fig(fig)

    def plot_sales_trend(self):
        df = self.df_filtered.copy()
        if 'Order Date' not in df.columns or 'Sales' not in df.columns:
            return

        theme = self.get_matplotlib_theme()
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        monthly = df.resample('ME', on='Order Date')['Sales'].sum()

        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=theme['bg'])
        ax.set_facecolor(theme['bg'])

        ax.plot(monthly.index, monthly.values, marker='o', color='#10B981', linewidth=2.5, markersize=6)
        ax.fill_between(monthly.index, monthly.values, color='#10B981', alpha=0.15)

        ax.set_title("XU HƯỚNG DOANH THU THEO THỜI GIAN", color=theme['fg'], fontsize=14, pad=15, fontweight='bold')
        ax.tick_params(colors=theme['fg'], labelsize=10)
        ax.grid(True, linestyle='--', color=theme['grid'], alpha=0.7)
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout()
        self.render_fig(fig)

    def plot_discount_profit(self):
        df = self.df_filtered
        if 'Discount' not in df.columns or 'Profit' not in df.columns:
            return

        theme = self.get_matplotlib_theme()

        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=theme['bg'])
        ax.set_facecolor(theme['bg'])

        ax.scatter(df['Discount'], df['Profit'], alpha=0.5, color='#F59E0B', edgecolors='none', s=30)
        ax.axhline(0, color='#EF4444', linestyle='--', linewidth=1, label="Ranh giới hòa vốn")

        ax.set_title("TÁC ĐỘNG CỦA GIẢM GIÁ (DISCOUNT) ĐẾN LỢI NHUẬN", color=theme['fg'], fontsize=14, pad=15, fontweight='bold')
        ax.set_xlabel("Mức Giảm Giá (Discount)", color=theme['fg'])
        ax.set_ylabel("Lợi Nhuận ($)", color=theme['fg'])
        ax.tick_params(colors=theme['fg'])
        ax.grid(True, linestyle='--', color=theme['grid'], alpha=0.7)
        ax.legend(facecolor=theme['bg'], edgecolor='none', labelcolor=theme['fg'])
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout()
        self.render_fig(fig)

    # ==================== VIEW 3: DATA TABLE WITH SEARCH ====================
    def show_data_table(self):
        df = self.df_filtered

        # Search Bar Header
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(search_frame, text="Tìm kiếm sản phẩm/đơn hàng:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 10))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Nhập từ khóa...", width=250)
        search_entry.pack(side="left")

        # Container Bảng
        table_container = ctk.CTkFrame(self.content_frame)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Cấu hình Treeview Style
        style = ttk.Style()
        style.theme_use("clam")
        
        mode = ctk.get_appearance_mode()
        bg_color = "#1E1E1E" if mode == "Dark" else "#FFFFFF"
        fg_color = "#FFFFFF" if mode == "Dark" else "#000000"
        header_bg = "#2D2D2D" if mode == "Dark" else "#E5E7EB"

        style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=28)
        style.configure("Treeview.Heading", background=header_bg, foreground=fg_color, font=('Arial', 10, 'bold'))

        # Chọn các cột hiển thị chính
        display_cols = [c for c in ['Order ID', 'Order Date', 'Customer Name', 'Category', 'Sub-Category', 'Sales', 'Profit'] if c in df.columns]
        if not display_cols:
            display_cols = list(df.columns[:6])

        tree = ttk.Treeview(table_container, columns=display_cols, show='headings')
        
        for col in display_cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        def populate_tree(data_df):
            tree.delete(*tree.get_children())
            for _, row in data_df.head(200).iterrows():  # Giới hạn 200 dòng để tối ưu hiệu năng
                vals = [row[c] for c in display_cols]
                tree.insert("", "end", values=vals)

        populate_tree(df)

        # Lọc dữ liệu real-time khi gõ từ khóa
        def on_search(_):
            query = search_entry.get().lower()
            if not query:
                populate_tree(df)
            else:
                filtered_df = df[df.astype(str).apply(lambda row: row.str.lower().str.contains(query).any(), axis=1)]
                populate_tree(filtered_df)

        search_entry.bind("<KeyRelease>", on_search)

if __name__ == "__main__":
    app = SuperstoreGUI()
    app.mainloop()