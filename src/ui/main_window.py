from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.config import COLORS, WINDOW_SIZE, MIN_WINDOW_SIZE
from src.ui.tabs.subtract_tab import SubtractTab
from src.ui.tabs.magnify_tab import MagnifyTab
from src.ui.tabs.layout_tab import LayoutTab


class MainWindow(QMainWindow):
    """应用程序主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageTool - 图像处理工具")
        self.setGeometry(100, 100, WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setMinimumSize(MIN_WINDOW_SIZE[0], MIN_WINDOW_SIZE[1])
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 添加三个功能标签页
        self.subtract_tab = SubtractTab()
        self.magnify_tab = MagnifyTab()
        self.layout_tab = LayoutTab()
        
        self.tab_widget.addTab(self.subtract_tab, "图像相减")
        self.tab_widget.addTab(self.magnify_tab, "局部放大")
        self.tab_widget.addTab(self.layout_tab, "图像排版")
        
        layout.addWidget(self.tab_widget)
        
    def apply_styles(self):
        """应用Claude暖色风格样式"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
            
            QWidget {{
                background-color: {COLORS['background']};
                color: {COLORS['text']};
                font-family: "Microsoft YaHei", "SimHei", sans-serif;
                font-size: 14px;
            }}
            
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['background']};
            }}
            
            QTabBar::tab {{
                background-color: {COLORS['background']};
                color: {COLORS['tab_inactive']};
                border: none;
                padding: 12px 30px;
                margin-right: 2px;
                font-size: 15px;
                font-weight: 500;
            }}
            
            QTabBar::tab:hover {{
                background-color: {COLORS['tab_hover']};
            }}
            
            QTabBar::tab:selected {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text']};
                border-bottom: 3px solid {COLORS['accent']};
            }}
            
            QLabel {{
                color: {COLORS['text']};
            }}
            
            QLineEdit {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px 12px;
                color: {COLORS['text']};
            }}
            
            QLineEdit:focus {{
                border-color: {COLORS['accent']};
            }}
            
            QComboBox {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px 12px;
                min-width: 100px;
            }}
            
            QComboBox:hover {{
                border-color: {COLORS['accent']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                selection-background-color: {COLORS['hover']};
            }}
            
            QSpinBox {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                min-width: 60px;
            }}
            
            QSpinBox:focus {{
                border-color: {COLORS['accent']};
            }}
            
            QRadioButton {{
                spacing: 8px;
                color: {COLORS['text']};
            }}
            
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {COLORS['border']};
                background-color: {COLORS['secondary_bg']};
            }}
            
            QRadioButton::indicator:checked {{
                background-color: {COLORS['accent']};
                border-color: {COLORS['accent']};
            }}
            
            QListWidget {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
            }}
            
            QListWidget::item {{
                padding: 6px;
                border-radius: 3px;
            }}
            
            QListWidget::item:selected {{
                background-color: {COLORS['hover']};
                color: {COLORS['text']};
            }}
            
            QScrollBar:vertical {{
                background-color: {COLORS['background']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {COLORS['border']};
                border-radius: 6px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['accent']};
            }}
            
            QMessageBox {{
                background-color: {COLORS['background']};
            }}
            
            QDialog {{
                background-color: {COLORS['background']};
            }}
        """)
