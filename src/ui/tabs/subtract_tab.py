from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QRadioButton, QButtonGroup, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from src.ui.components.styled_button import StyledButton
from src.ui.components.file_drop_area import ImageDropArea
from src.ui.components.preview_window import PreviewWindow
from src.core.subtract import ImageSubtract
from src.utils.file_utils import generate_filename
from PIL import Image


class SubtractTab(QWidget):
    """图像相减标签页"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image1 = None
        self.image2 = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("图像相减")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D2A26;")
        layout.addWidget(title)
        
        # 图像选择区
        images_layout = QHBoxLayout()
        
        # 被减数
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(QLabel("被减数图像"))
        self.drop_area1 = ImageDropArea("拖拽或点击选择图像")
        self.drop_area1.imageDropped.connect(lambda path: self.on_image_dropped(1, path))
        self.drop_area1.mousePressEvent = lambda e: self.on_area_clicked(1, e)
        vlayout1.addWidget(self.drop_area1)
        images_layout.addLayout(vlayout1)
        
        # 交换按钮
        swap_btn = StyledButton("⇄ 交换", "secondary")
        swap_btn.setMaximumWidth(80)
        swap_btn.clicked.connect(self.swap_images)
        images_layout.addWidget(swap_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 减数
        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(QLabel("减数图像"))
        self.drop_area2 = ImageDropArea("拖拽或点击选择图像")
        self.drop_area2.imageDropped.connect(lambda path: self.on_image_dropped(2, path))
        self.drop_area2.mousePressEvent = lambda e: self.on_area_clicked(2, e)
        vlayout2.addWidget(self.drop_area2)
        images_layout.addLayout(vlayout2)
        
        layout.addLayout(images_layout)
        
        # 算法选择
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("算法:"))
        self.algo_group = QButtonGroup(self)
        
        self.radio_simple = QRadioButton("简单相减")
        self.radio_absolute = QRadioButton("绝对值相减")
        self.radio_absolute.setChecked(True)
        self.radio_diff = QRadioButton("差分显示")
        
        self.algo_group.addButton(self.radio_simple)
        self.algo_group.addButton(self.radio_absolute)
        self.algo_group.addButton(self.radio_diff)
        
        algo_layout.addWidget(self.radio_simple)
        algo_layout.addWidget(self.radio_absolute)
        algo_layout.addWidget(self.radio_diff)
        algo_layout.addStretch()
        layout.addLayout(algo_layout)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        preview_btn = StyledButton("预览结果", "secondary")
        preview_btn.clicked.connect(self.preview_result)
        btn_layout.addWidget(preview_btn)
        
        process_btn = StyledButton("处理并保存...", "primary")
        process_btn.clicked.connect(self.process_and_save)
        btn_layout.addWidget(process_btn)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
    def on_image_dropped(self, area_num, path):
        image = Image.open(path)
        if area_num == 1:
            self.image1 = image
            self.drop_area1.load_image(path)
        else:
            self.image2 = image
            self.drop_area2.load_image(path)
        
    def on_area_clicked(self, area_num, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.browse_image(area_num)
        
    def browse_image(self, area_num):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图像", "", "图像文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.on_image_dropped(area_num, file_path)
            
    def swap_images(self):
        self.image1, self.image2 = self.image2, self.image1
        self.drop_area1.clear_image()
        self.drop_area2.clear_image()
        if self.image1:
            self.drop_area1.display_image(self.image1)
        if self.image2:
            self.drop_area2.display_image(self.image2)
        
    def get_algorithm(self):
        if self.radio_simple.isChecked():
            return 'simple'
        elif self.radio_absolute.isChecked():
            return 'absolute'
        else:
            return 'diff'
            
    def preview_result(self):
        if not self.image1 or not self.image2:
            QMessageBox.warning(self, "警告", "请先选择两张图像")
            return
            
        result = ImageSubtract.subtract_images(
            self.image1, self.image2, self.get_algorithm()
        )
        if result:
            preview = PreviewWindow(result, "图像相减预览", self)
            preview.exec()
                
    def process_and_save(self):
        if not self.image1 or not self.image2:
            QMessageBox.warning(self, "警告", "请先选择两张图像")
            return
            
        result = ImageSubtract.subtract_images(
            self.image1, self.image2, self.get_algorithm()
        )
        
        if result:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果", generate_filename("subtract"),
                "PNG文件 (*.png);;JPEG文件 (*.jpg);;BMP文件 (*.bmp)"
            )
            if save_path:
                result.save(save_path)
                QMessageBox.information(self, "成功", "图像已保存")
