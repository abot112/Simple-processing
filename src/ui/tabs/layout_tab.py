from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QLineEdit, QSpinBox, QGridLayout,
                             QFileDialog, QMessageBox, QListWidget, QListWidgetItem,
                             QPushButton, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from src.ui.components.styled_button import StyledButton
from src.ui.components.preview_window import PreviewWindow
from src.core.layout import ImageLayout
from src.utils.file_utils import generate_filename
from PIL import Image


class LayoutTab(QWidget):
    """图像排版标签页"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.images = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("图像排版")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D2A26;")
        layout.addWidget(title)
        
        # 拼图设置
        settings_layout = QHBoxLayout()
        
        # 快速选择
        settings_layout.addWidget(QLabel("快速选择:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["自定义", "2×2", "2×3", "3×3", "3×4", "4×4"])
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        settings_layout.addWidget(self.preset_combo)
        
        settings_layout.addWidget(QLabel("或"))
        
        # 行数
        settings_layout.addWidget(QLabel("行:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 10)
        self.rows_spin.setValue(2)
        settings_layout.addWidget(self.rows_spin)
        
        # 列数
        settings_layout.addWidget(QLabel("列:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(2)
        settings_layout.addWidget(self.cols_spin)
        
        settings_layout.addStretch()
        layout.addLayout(settings_layout)
        
        # 标题设置
        title_layout = QVBoxLayout()
        
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(QLabel("总标题:"))
        self.title_input = QLineEdit()
        hlayout1.addWidget(self.title_input)
        title_layout.addLayout(hlayout1)
        
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(QLabel("行标题:"))
        self.row_label_num = QRadioButton("使用数字(1,2,3...)")
        self.row_label_num.setChecked(True)
        self.row_label_custom = QRadioButton("自定义")
        hlayout2.addWidget(self.row_label_num)
        hlayout2.addWidget(self.row_label_custom)
        hlayout2.addStretch()
        title_layout.addLayout(hlayout2)
        
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(QLabel("列标题:"))
        self.col_label_alpha = QRadioButton("使用字母(A,B,C...)")
        self.col_label_alpha.setChecked(True)
        self.col_label_custom = QRadioButton("自定义")
        hlayout3.addWidget(self.col_label_alpha)
        hlayout3.addWidget(self.col_label_custom)
        hlayout3.addStretch()
        title_layout.addLayout(hlayout3)
        
        layout.addLayout(title_layout)
        
        # 主内容区
        content_layout = QHBoxLayout()
        
        # 左侧：图像网格
        grid_container = QVBoxLayout()
        grid_container.addWidget(QLabel("拼图预览（点击添加图像）:"))
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.update_grid()
        grid_container.addWidget(self.grid_widget)
        content_layout.addLayout(grid_container, stretch=3)
        
        # 右侧：图像列表
        list_container = QVBoxLayout()
        list_container.addWidget(QLabel("已选图像列表:"))
        
        self.image_list = QListWidget()
        self.image_list.setMaximumWidth(250)
        list_container.addWidget(self.image_list)
        
        btn_layout = QHBoxLayout()
        add_btn = StyledButton("添加图像", "secondary")
        add_btn.clicked.connect(self.add_images)
        btn_layout.addWidget(add_btn)
        
        clear_btn = StyledButton("清空", "secondary")
        clear_btn.clicked.connect(self.clear_images)
        btn_layout.addWidget(clear_btn)
        
        list_container.addLayout(btn_layout)
        content_layout.addLayout(list_container, stretch=1)
        
        layout.addLayout(content_layout)
        
        # 操作按钮
        action_layout = QHBoxLayout()

        auto_fill_btn = StyledButton("自动填充", "secondary")
        auto_fill_btn.clicked.connect(self.auto_fill)
        action_layout.addWidget(auto_fill_btn)

        action_layout.addStretch()

        preview_btn = StyledButton("预览效果", "secondary")
        preview_btn.clicked.connect(self.preview_result)
        action_layout.addWidget(preview_btn)

        process_btn = StyledButton("生成并保存...", "primary")
        process_btn.clicked.connect(self.process_and_save)
        action_layout.addWidget(process_btn)

        layout.addLayout(action_layout)
        layout.addStretch()
        
    def on_preset_changed(self, text):
        if text == "2×2":
            self.rows_spin.setValue(2)
            self.cols_spin.setValue(2)
        elif text == "2×3":
            self.rows_spin.setValue(2)
            self.cols_spin.setValue(3)
        elif text == "3×3":
            self.rows_spin.setValue(3)
            self.cols_spin.setValue(3)
        elif text == "3×4":
            self.rows_spin.setValue(3)
            self.cols_spin.setValue(4)
        elif text == "4×4":
            self.rows_spin.setValue(4)
            self.cols_spin.setValue(4)
        self.update_grid()
        
    def update_grid(self):
        # 清空现有布局
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                label = QLabel(f"图{idx+1}")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setMinimumSize(80, 80)
                label.setStyleSheet("""
                    QLabel {
                        background-color: #F5F3EF;
                        border: 2px dashed #D0C8BD;
                        border-radius: 4px;
                        color: #9B9590;
                    }
                """)
                label.mousePressEvent = lambda e, i=idx: self.on_cell_clicked(i)
                self.grid_layout.addWidget(label, r, c)
                
    def on_cell_clicked(self, index):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图像", "", "图像文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.add_image_to_list(file_path)
            
    def add_image_to_list(self, path):
        if path not in self.images:
            self.images.append(path)
            item = QListWidgetItem(path.split('/')[-1])
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.image_list.addItem(item)
            
    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择图像", "", "图像文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        for f in files:
            self.add_image_to_list(f)
            
    def clear_images(self):
        self.images.clear()
        self.image_list.clear()
        
    def auto_fill(self):
        # 按列表顺序填充到网格
        pass
        
    def get_row_labels(self):
        if not self.row_label_num.isChecked():
            return None
        rows = self.rows_spin.value()
        return [str(i+1) for i in range(rows)]
        
    def get_col_labels(self):
        if not self.col_label_alpha.isChecked():
            return None
        cols = self.cols_spin.value()
        return [chr(65+i) for i in range(cols)]
        
    def load_and_create_layout(self):
        if len(self.images) == 0:
            return None

        loaded_images = []
        for path in self.images:
            try:
                img = Image.open(path)
                loaded_images.append(img)
            except:
                pass

        if not loaded_images:
            return None

        return ImageLayout.create_layout(
            loaded_images,
            rows=self.rows_spin.value(),
            cols=self.cols_spin.value(),
            title=self.title_input.text(),
            row_labels=self.get_row_labels(),
            col_labels=self.get_col_labels()
        )

    def preview_result(self):
        result = self.load_and_create_layout()
        if result:
            preview = PreviewWindow(result, "图像排版预览", self)
            preview.exec()
        else:
            QMessageBox.warning(self, "警告", "请先选择图像或无法加载图像")

    def process_and_save(self):
        result = self.load_and_create_layout()
        if result:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果",
                generate_filename("layout", suffix=f"_{self.rows_spin.value()}x{self.cols_spin.value()}.png"),
                "PNG文件 (*.png)"
            )
            if save_path:
                result.save(save_path)
                QMessageBox.information(self, "成功", "拼图已保存")
        else:
            QMessageBox.warning(self, "警告", "请先选择图像或无法加载图像")
