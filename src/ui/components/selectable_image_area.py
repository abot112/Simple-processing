from PyQt6.QtWidgets import QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QCursor
from PIL import Image
from src.config import COLORS


class SelectableImageArea(QLabel):

    imageDropped = pyqtSignal(str)
    selectionChanged = pyqtSignal(int, int, int, int)

    def __init__(self, placeholder_text="拖拽或点击选择图像", parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder_text
        self.image_path = None
        self.current_image = None
        self.pixmap_width = 0
        self.pixmap_height = 0
        self.pixmap_offset_x = 0
        self.pixmap_offset_y = 0

        self.selection_rect = None
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_selection = None
        self.selection_size = None
        self.selection_pixel_size = 50

        self.border_color = '#D97757'

        self.setup_ui()

    def set_border_color(self, color):
        self.border_color = color
        if self.current_image:
            self._apply_loaded_border_style()
            self.update_display_with_selection()

    def _apply_loaded_border_style(self):
        """预览区外框与选区矩形使用同一 border_color，避免与主题 accent 硬编码不一致。"""
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['light_bg']};
                border: 2px solid {self.border_color};
                border-radius: 8px;
            }}
        """)

    def set_selection_size(self, pixel_size):
        self.selection_pixel_size = pixel_size
        if not self.current_image or not self.selection_rect:
            return

        scale_x = self.pixmap_width / self.current_image.width
        scale_y = self.pixmap_height / self.current_image.height
        avg_scale = (scale_x + scale_y) / 2

        display_size = int(pixel_size * avg_scale)
        display_size = max(10, min(display_size, min(self.pixmap_width, self.pixmap_height) // 2))

        current_x = self.selection_rect.x()
        current_y = self.selection_rect.y()

        max_size_x = self.pixmap_width - current_x
        max_size_y = self.pixmap_height - current_y
        magnify_x = self.pixmap_width // 2
        magnify_y = self.pixmap_height // 2

        if current_x < magnify_x:
            max_size_x = min(max_size_x, magnify_x - current_x)
        if current_y < magnify_y:
            max_size_y = min(max_size_y, magnify_y - current_y)

        display_size = min(display_size, max_size_x, max_size_y)
        display_size = max(10, display_size)

        self.selection_size = (display_size, display_size)
        self.selection_rect.setWidth(display_size)
        self.selection_rect.setHeight(display_size)

        self.update_display_with_selection()
        self.emit_selection_changed()

    def setup_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 200)
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
        self.setMouseTracking(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.is_valid_image(file_path):
                self.load_image(file_path)
                self.imageDropped.emit(file_path)

    def is_valid_image(self, path):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        return path.lower().endswith(valid_extensions)

    def load_image(self, path):
        self.image_path = path
        image = Image.open(path)
        self.current_image = image
        self.display_image(image)

    def display_image(self, image):
        image = image.convert('RGB')
        data = image.tobytes('raw', 'RGB')
        qimage = QImage(data, image.width, image.height, image.width * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        label_width = self.width() - 20
        label_height = self.height() - 20

        scaled_pixmap = pixmap.scaled(
            label_width,
            label_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.pixmap_width = scaled_pixmap.width()
        self.pixmap_height = scaled_pixmap.height()
        self.pixmap_offset_x = (self.width() - self.pixmap_width) // 2
        self.pixmap_offset_y = (self.height() - self.pixmap_height) // 2

        scale_x = self.pixmap_width / self.current_image.width
        scale_y = self.pixmap_height / self.current_image.height
        avg_scale = (scale_x + scale_y) / 2

        display_size = int(self.selection_pixel_size * avg_scale)
        display_size = max(10, min(display_size, min(self.pixmap_width, self.pixmap_height) // 2))

        magnify_x = self.pixmap_width // 2
        magnify_y = self.pixmap_height // 2
        display_size = min(display_size, magnify_x, magnify_y)

        self.selection_size = (display_size, display_size)
        self.selection_rect = QRect(0, 0, display_size, display_size)

        self._apply_loaded_border_style()

        self.update_display_with_selection()
        self.emit_selection_changed()

    def update_display_with_selection(self):
        if not self.current_image:
            return

        image = self.current_image.convert('RGB')
        data = image.tobytes('raw', 'RGB')
        qimage = QImage(data, image.width, image.height, image.width * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        label_width = self.width() - 20
        label_height = self.height() - 20

        scaled_pixmap = pixmap.scaled(
            label_width,
            label_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        if self.selection_rect:
            painter = QPainter(scaled_pixmap)
            pen = QPen(QColor(self.border_color))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)
            painter.end()

        self.setPixmap(scaled_pixmap)

    def is_point_in_selection(self, pos):
        if not self.selection_rect:
            return False
        pixmap_x = pos.x() - self.pixmap_offset_x
        pixmap_y = pos.y() - self.pixmap_offset_y
        return self.selection_rect.contains(int(pixmap_x), int(pixmap_y))

    def constrain_selection_to_valid_area(self, x, y):
        if not self.selection_size:
            return x, y

        sw, sh = self.selection_size

        max_x = self.pixmap_width - sw
        max_y = self.pixmap_height - sh

        magnify_x = self.pixmap_width // 2
        magnify_y = self.pixmap_height // 2

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        if x >= magnify_x and y >= magnify_y:
            if x >= magnify_x:
                x = magnify_x - sw
                if x < 0:
                    x = 0
            if y >= magnify_y:
                y = magnify_y - sh
                if y < 0:
                    y = 0

        if x + sw > magnify_x and y + sh > magnify_y:
            if x >= magnify_x:
                x = magnify_x - sw
            if y >= magnify_y:
                y = magnify_y - sh

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        return x, y

    def mousePressEvent(self, event):
        if not self.current_image:
            if event.button() == Qt.MouseButton.LeftButton:
                self.browse_image()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            if (self.pixmap_offset_x <= pos.x() <= self.pixmap_offset_x + self.pixmap_width and
                self.pixmap_offset_y <= pos.y() <= self.pixmap_offset_y + self.pixmap_height):

                if self.is_point_in_selection(pos):
                    self.is_dragging = True
                    self.drag_start_pos = pos
                    self.drag_start_selection = QRect(self.selection_rect)

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.current_image and self.selection_rect:
            delta_x = event.pos().x() - self.drag_start_pos.x()
            delta_y = event.pos().y() - self.drag_start_pos.y()

            new_x = self.drag_start_selection.x() + delta_x
            new_y = self.drag_start_selection.y() + delta_y

            new_x, new_y = self.constrain_selection_to_valid_area(new_x, new_y)

            self.selection_rect.moveTo(int(new_x), int(new_y))
            self.update_display_with_selection()
            self.emit_selection_changed()
        elif self.current_image:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.drag_start_pos = None
            self.drag_start_selection = None

    def update_cursor(self, pos):
        if not self.current_image:
            return
        if (self.pixmap_offset_x <= pos.x() <= self.pixmap_offset_x + self.pixmap_width and
            self.pixmap_offset_y <= pos.y() <= self.pixmap_offset_y + self.pixmap_height):
            if self.is_point_in_selection(pos):
                self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def emit_selection_changed(self):
        if self.selection_rect:
            x1, y1, x2, y2 = self.get_selection_in_image_coords()
            self.selectionChanged.emit(x1, y1, x2, y2)

    def get_selection_in_image_coords(self):
        if not self.selection_rect or not self.current_image:
            return 0, 0, 0, 0

        scale_x = self.current_image.width / self.pixmap_width
        scale_y = self.current_image.height / self.pixmap_height

        x1 = int(self.selection_rect.x() * scale_x)
        y1 = int(self.selection_rect.y() * scale_y)
        x2 = int((self.selection_rect.x() + self.selection_rect.width()) * scale_x)
        y2 = int((self.selection_rect.y() + self.selection_rect.height()) * scale_y)

        return x1, y1, x2, y2

    def get_selection(self):
        if self.selection_rect:
            return self.get_selection_in_image_coords()
        return None

    def clear_selection(self):
        self.selection_rect = None
        if self.current_image:
            self.display_image(self.current_image)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图像", "", "图像文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.load_image(file_path)
            self.imageDropped.emit(file_path)

    def clear_image(self):
        self.image_path = None
        self.current_image = None
        self.clear()
        self.setText(self.placeholder_text)
        self.selection_rect = None
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
