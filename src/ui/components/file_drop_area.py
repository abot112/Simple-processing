from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
from PIL import Image
from src.config import COLORS
import io
import numpy as np


class ImageDropArea(QLabel):
    """支持拖拽的图像显示区域"""
    
    imageDropped = pyqtSignal(str)
    
    def __init__(self, placeholder_text="拖拽或点击选择图像", parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder_text
        self.image_path = None
        self.current_image = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(200, 150)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['light_bg']};
                border: 2px dashed {COLORS['border']};
                border-radius: 8px;
                color: {COLORS['muted_text']};
                font-size: 13px;
            }}
            QLabel:hover {{
                border-color: {COLORS['accent']};
            }}
        """)
        self.setText(self.placeholder_text)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.is_valid_image(file_path):
                self.load_image(file_path)
                self.imageDropped.emit(file_path)
                
    def is_valid_image(self, path: str) -> bool:
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        return path.lower().endswith(valid_extensions)
        
    def load_image(self, path: str):
        self.image_path = path
        image = Image.open(path)
        self.current_image = image
        self.display_image(image)
        
    def display_image(self, image: Image.Image):
        # 转换为QPixmap显示
        image = image.convert('RGB')
        data = image.tobytes('raw', 'RGB')
        qimage = QImage(data, image.width, image.height, image.width * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        
        # 缩放以适应标签大小
        scaled_pixmap = pixmap.scaled(
            self.width() - 20, 
            self.height() - 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['light_bg']};
                border: 2px solid {COLORS['accent']};
                border-radius: 8px;
            }}
        """)
        
    def clear_image(self):
        self.image_path = None
        self.current_image = None
        self.clear()
        self.setText(self.placeholder_text)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['light_bg']};
                border: 2px dashed {COLORS['border']};
                border-radius: 8px;
                color: {COLORS['muted_text']};
                font-size: 13px;
            }}
            QLabel:hover {{
                border-color: {COLORS['accent']};
            }}
        """)
