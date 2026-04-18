from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image
from src.config import COLORS


class PreviewWindow(QDialog):
    def __init__(self, image, title="预览", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        self.image = image
        self.setup_ui()
        self.display_image()
        
    def setup_ui(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['secondary_bg']};
            }}
        """)
        
        scroll.setWidget(self.image_label)
        layout.addWidget(scroll)
        
        info_label = QLabel(f"图像尺寸: {self.image.width} x {self.image.height}")
        info_label.setStyleSheet("color: #9B9590; font-size: 12px;")
        layout.addWidget(info_label)
        
    def display_image(self):
        image = self.image.convert('RGB')
        data = image.tobytes('raw', 'RGB')
        qimage = QImage(data, image.width, image.height, image.width * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        
        scaled_pixmap = pixmap.scaled(
            760, 540,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
