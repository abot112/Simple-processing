from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import COLORS


class StyledButton(QPushButton):
    """自定义样式的按钮组件"""
    
    def __init__(self, text, button_type='primary', parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.apply_style()
        
    def apply_style(self):
        if self.button_type == 'primary':
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color: {COLORS['secondary_bg']};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['hover']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['accent']};
                }}
                QPushButton:disabled {{
                    background-color: {COLORS['disabled']};
                    color: {COLORS['muted_text']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['secondary_bg']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 6px;
                    padding: 10px 24px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['background']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['border']};
                }}
            """)
