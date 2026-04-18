from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFileDialog, QMessageBox, QFrame, QSpinBox, QComboBox,
                             QStackedWidget, QPushButton, QScrollArea, QGridLayout,
                             QProgressDialog, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap, QImage
from PyQt6.QtWidgets import QColorDialog
from src.ui.components.styled_button import StyledButton
from src.ui.components.selectable_image_area import SelectableImageArea
from src.ui.components.preview_window import PreviewWindow
from src.core.magnify import ImageMagnify
from src.utils.file_utils import generate_filename, get_supported_images
from PIL import Image
import os


class ImageGalleryWidget(QWidget):
    imageSelected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_paths = []
        self.thumbnail_labels = []
        self.selected_index = 0
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题和信息
        info_layout = QHBoxLayout()
        self.info_label = QLabel("图像列表: 0 张")
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()
        
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #D97757;
                color: #D97757;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D97757;
                color: white;
            }
        """)
        self.select_all_btn.clicked.connect(self.select_all)
        info_layout.addWidget(self.select_all_btn)
        
        self.select_none_btn = QPushButton("取消全选")
        self.select_none_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #9B9590;
                color: #9B9590;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #9B9590;
                color: white;
            }
        """)
        self.select_none_btn.clicked.connect(self.select_none)
        info_layout.addWidget(self.select_none_btn)
        
        layout.addLayout(info_layout)
        
        # 滚动区域用于缩略图
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFixedHeight(140)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #F5F3EF;
                border: 1px solid #E8E0D5;
                border-radius: 8px;
            }
        """)
        
        self.gallery_container = QWidget()
        self.gallery_layout = QHBoxLayout(self.gallery_container)
        self.gallery_layout.setSpacing(10)
        self.gallery_layout.setContentsMargins(10, 10, 10, 10)
        self.gallery_layout.addStretch()
        
        scroll.setWidget(self.gallery_container)
        layout.addWidget(scroll)
        
        # 选中状态跟踪
        self.selected_indices = set()
    
    def load_images(self, image_paths):
        """加载图像列表并生成缩略图"""
        self.image_paths = image_paths
        self.selected_indices = set(range(len(image_paths)))  # 默认全选
        self.selected_index = 0 if image_paths else -1
        
        # 清除现有缩略图
        for label in self.thumbnail_labels:
            label.deleteLater()
        self.thumbnail_labels.clear()
        
        self.info_label.setText(f"图像列表: {len(image_paths)} 张")
        
        # 生成缩略图
        for i, path in enumerate(image_paths):
            thumbnail_widget = self.create_thumbnail_widget(path, i)
            self.gallery_layout.insertWidget(self.gallery_layout.count() - 1, thumbnail_widget)
            self.thumbnail_labels.append(thumbnail_widget)
        
        self.update_selection_display()
    
    def create_thumbnail_widget(self, image_path, index):
        """创建单个缩略图组件"""
        container = QFrame()
        container.setFixedSize(100, 100)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E8E0D5;
                border-radius: 4px;
            }
            QFrame:hover {
                border-color: #D97757;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(2)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # 缩略图标签
        img_label = QLabel()
        img_label.setFixedSize(88, 68)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("background-color: #F5F3EF; border-radius: 2px;")
        
        # 加载并缩放图像
        try:
            img = Image.open(image_path)
            img.thumbnail((88, 68))
            
            # 转换为QPixmap
            img_rgb = img.convert('RGB')
            data = img_rgb.tobytes('raw', 'RGB')
            qimage = QImage(data, img_rgb.width, img_rgb.height, img_rgb.width * 3, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            
            img_label.setPixmap(pixmap)
        except Exception as e:
            img_label.setText("加载失败")
        
        layout.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 文件名标签
        name_label = QLabel(os.path.basename(image_path)[:12] + "..." if len(os.path.basename(image_path)) > 12 else os.path.basename(image_path))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 10px; color: #6B6560; background: transparent;")
        layout.addWidget(name_label)
        
        # 复选框
        checkbox = QCheckBox()
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(lambda state, idx=index: self.on_checkbox_changed(idx, state))
        layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 点击事件
        container.mousePressEvent = lambda event, idx=index: self.on_thumbnail_clicked(idx)
        
        # 保存引用
        container.checkbox = checkbox
        container.index = index
        
        return container
    
    def on_thumbnail_clicked(self, index):
        """点击缩略图"""
        self.selected_index = index
        self.imageSelected.emit(index)
        self.update_selection_display()
    
    def on_checkbox_changed(self, index, state):
        """复选框状态改变"""
        if state == Qt.CheckState.Checked.value:
            self.selected_indices.add(index)
        else:
            self.selected_indices.discard(index)
    
    def update_selection_display(self):
        """更新选中状态的视觉显示"""
        for i, widget in enumerate(self.thumbnail_labels):
            if i == self.selected_index:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border: 3px solid #D97757;
                        border-radius: 4px;
                    }
                """)
            else:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border: 2px solid #E8E0D5;
                        border-radius: 4px;
                    }
                    QFrame:hover {
                        border-color: #D97757;
                    }
                """)
    
    def select_all(self):
        """全选"""
        self.selected_indices = set(range(len(self.image_paths)))
        for widget in self.thumbnail_labels:
            widget.checkbox.setChecked(True)
    
    def select_none(self):
        """取消全选"""
        self.selected_indices.clear()
        for widget in self.thumbnail_labels:
            widget.checkbox.setChecked(False)
    
    def get_selected_images(self):
        """获取选中的图像路径列表"""
        return [self.image_paths[i] for i in sorted(self.selected_indices) if i < len(self.image_paths)]
    
    def get_selected_count(self):
        """获取选中的图像数量"""
        return len(self.selected_indices)


class BatchMagnifyWidget(QWidget):
    """批量处理组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_paths = []
        self.current_preview_index = 0
        self.folder_path = ""
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 文件夹选择区域
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("文件夹: 未选择")
        self.folder_label.setStyleSheet("color: #6B6560;")
        folder_layout.addWidget(self.folder_label)
        
        folder_btn = StyledButton("选择文件夹...", "secondary")
        folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(folder_btn)
        
        folder_layout.addStretch()
        layout.addLayout(folder_layout)
        
        # 主内容区域 - 左右布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        
        # 左侧：首张图像预览（用于样式确认）
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        self.preview_info = QLabel("请选择一个文件夹，将加载第一张图像用于样式确认")
        self.preview_info.setStyleSheet("color: #9B9590; font-size: 13px;")
        left_layout.addWidget(self.preview_info)
        
        self.source_area = SelectableImageArea("拖拽或点击选择文件夹")
        self.source_area.imageDropped.connect(self.on_folder_dropped)
        self.source_area.selectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.source_area, stretch=1)
        
        main_layout.addLayout(left_layout, stretch=1)
        
        # 右侧：控制面板
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 图像数量信息
        self.count_label = QLabel("已加载: 0 张图像")
        self.count_label.setStyleSheet("font-size: 14px; color: #2D2A26; font-weight: bold;")
        right_layout.addWidget(self.count_label)
        
        right_layout.addSpacing(10)
        
        # 框选边长控制（与单图模式共享样式）
        right_layout.addWidget(QLabel("框选边长 (像素):"))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(10, 1000)
        self.size_spinbox.setValue(50)
        self.size_spinbox.setSuffix(" px")
        self.size_spinbox.valueChanged.connect(self.on_size_changed)
        right_layout.addWidget(self.size_spinbox)
        right_layout.addSpacing(10)
        
        # 边框颜色控制
        right_layout.addWidget(QLabel("边框颜色:"))
        color_layout = QHBoxLayout()
        
        self.border_color = "#D97757"
        self.color_preview = QFrame()
        self.color_preview.setFixedSize(40, 30)
        self.color_preview.setStyleSheet(f"background-color: {self.border_color}; border: 1px solid #ccc;")
        color_layout.addWidget(self.color_preview)
        
        color_btn = StyledButton("选择颜色...", "secondary")
        color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(color_btn)
        color_layout.addStretch()
        
        right_layout.addLayout(color_layout)
        right_layout.addSpacing(20)
        
        # 操作按钮
        self.preview_btn = StyledButton("预览当前图像", "secondary")
        self.preview_btn.clicked.connect(self.preview_current)
        self.preview_btn.setEnabled(False)
        right_layout.addWidget(self.preview_btn)
        
        self.process_btn = StyledButton("批量处理并保存...", "primary")
        self.process_btn.clicked.connect(self.batch_process)
        self.process_btn.setEnabled(False)
        right_layout.addWidget(self.process_btn)
        
        right_layout.addStretch()
        main_layout.addLayout(right_layout)
        
        layout.addLayout(main_layout, stretch=1)
        
        # 画廊区域
        self.gallery = ImageGalleryWidget()
        self.gallery.imageSelected.connect(self.on_gallery_image_selected)
        layout.addWidget(self.gallery)
    
    def select_folder(self):
        """选择文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择包含图像的文件夹")
        if folder_path:
            self.load_folder(folder_path)
    
    def on_folder_dropped(self, path):
        """处理拖拽的文件夹"""
        if os.path.isdir(path):
            self.load_folder(path)
        else:
            # 如果是文件，使用其父文件夹
            folder_path = os.path.dirname(path)
            self.load_folder(folder_path)
    
    def load_folder(self, folder_path):
        """加载文件夹中的所有图像"""
        self.folder_path = folder_path
        self.image_paths = get_supported_images(folder_path)
        
        if not self.image_paths:
            QMessageBox.warning(self, "警告", "所选文件夹中没有支持的图像文件（.png, .jpg, .jpeg, .bmp）")
            return
        
        self.folder_label.setText(f"文件夹: {folder_path}")
        self.count_label.setText(f"已加载: {len(self.image_paths)} 张图像")
        self.preview_info.setText(f"首张图像 (共{len(self.image_paths)}张) - 调整选区以确认样式")
        
        # 加载第一张图像作为预览
        self.current_preview_index = 0
        self.load_preview_image(self.image_paths[0], is_first_load=True)
        
        # 加载画廊
        self.gallery.load_images(self.image_paths)
        
        # 启用按钮
        self.preview_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
    
    def load_preview_image(self, image_path, is_first_load=False):
        image = Image.open(image_path)
        self.source_area.set_border_color(self.border_color)
        self.source_area.load_image(image_path)
        
        if is_first_load:
            img_size = min(image.size)
            default_size = max(10, img_size // 16)
            self.size_spinbox.setValue(default_size)
    
    def on_selection_changed(self, x1, y1, x2, y2):
        """选区改变"""
        size = x2 - x1
        self.size_spinbox.blockSignals(True)
        self.size_spinbox.setValue(size)
        self.size_spinbox.blockSignals(False)
    
    def on_size_changed(self, value):
        """大小改变"""
        self.source_area.set_selection_size(value)
    
    def choose_color(self):
        """选择颜色"""
        color = QColorDialog.getColor(QColor(self.border_color), self, "选择边框颜色")
        if color.isValid():
            self.border_color = color.name()
            self.color_preview.setStyleSheet(f"background-color: {self.border_color}; border: 1px solid #ccc;")
            self.source_area.set_border_color(self.border_color)
    
    def on_gallery_image_selected(self, index):
        if 0 <= index < len(self.image_paths):
            self.current_preview_index = index
            self.load_preview_image(self.image_paths[index], is_first_load=False)
            self.preview_info.setText(f"图像 {index + 1}/{len(self.image_paths)} - 用于样式确认")
    
    def preview_current(self):
        """预览当前图像的效果"""
        if not self.image_paths or self.current_preview_index >= len(self.image_paths):
            QMessageBox.warning(self, "警告", "请先选择文件夹")
            return
        
        image = Image.open(self.image_paths[self.current_preview_index])
        selection = self.source_area.get_selection()
        
        if not selection:
            QMessageBox.warning(self, "警告", "请先在图像上框选要放大的区域")
            return
        
        x1, y1, x2, y2 = selection
        
        result = ImageMagnify.magnify_region(
            image, x1, y1, x2, y2,
            border_color=self.source_area.border_color
        )
        
        if result:
            preview = PreviewWindow(result, f"图像 {self.current_preview_index + 1} 预览", self)
            preview.exec()
    
    def batch_process(self):
        """批量处理所有选中的图像"""
        selected_images = self.gallery.get_selected_images()
        
        if not selected_images:
            QMessageBox.warning(self, "警告", "请至少选择一张图像进行处理")
            return
        
        # 选择输出文件夹
        output_folder = QFileDialog.getExistingDirectory(self, "选择保存结果的文件夹")
        if not output_folder:
            return
        
        # 获取选区参数
        selection = self.source_area.get_selection()
        if not selection:
            QMessageBox.warning(self, "警告", "请先在预览图像上框选要放大的区域")
            return
        
        x1, y1, x2, y2 = selection
        
        # 进度对话框
        progress = QProgressDialog("正在处理图像...", "取消", 0, len(selected_images), self)
        progress.setWindowTitle("批量处理中")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        
        success_count = 0
        failed_count = 0
        failed_files = []
        
        for i, image_path in enumerate(selected_images):
            if progress.wasCanceled():
                break
            
            progress.setValue(i)
            progress.setLabelText(f"正在处理: {os.path.basename(image_path)}")
            
            try:
                image = Image.open(image_path)
                
                result = ImageMagnify.magnify_region(
                    image, x1, y1, x2, y2,
                    border_color=self.source_area.border_color
                )
                
                if result:
                    # 生成输出文件名
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    output_path = os.path.join(output_folder, f"{base_name}_magnified.png")
                    
                    # 如果文件已存在，添加数字后缀
                    counter = 1
                    while os.path.exists(output_path):
                        output_path = os.path.join(output_folder, f"{base_name}_magnified_{counter}.png")
                        counter += 1
                    
                    result.save(output_path)
                    success_count += 1
                else:
                    failed_count += 1
                    failed_files.append(os.path.basename(image_path))
            except Exception as e:
                failed_count += 1
                failed_files.append(f"{os.path.basename(image_path)} ({str(e)})")
        
        progress.setValue(len(selected_images))
        
        # 显示结果
        msg = f"处理完成！\n\n成功: {success_count} 张\n失败: {failed_count} 张"
        if failed_files:
            msg += f"\n\n失败的文件:\n" + "\n".join(failed_files[:5])
            if len(failed_files) > 5:
                msg += f"\n... 还有 {len(failed_files) - 5} 个文件"
        
        QMessageBox.information(self, "处理完成", msg)


class MagnifyTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.selection_coords = None
        self.border_color = "#D97757"
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题和模式选择
        header_layout = QHBoxLayout()
        
        title = QLabel("局部放大")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D2A26;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # 模式选择
        mode_label = QLabel("处理模式:")
        mode_label.setStyleSheet("color: #6B6560;")
        header_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("单图模式", "single")
        self.mode_combo.addItem("批量处理模式", "batch")
        self.mode_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #E8E0D5;
                border-radius: 4px;
                padding: 8px 12px;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #D97757;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #E8E0D5;
                selection-background-color: #E8C4B8;
            }
        """)
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        header_layout.addWidget(self.mode_combo)
        
        layout.addLayout(header_layout)

        # 堆叠部件用于切换模式
        self.stacked_widget = QStackedWidget()
        
        # 单图模式页面
        self.single_mode_widget = self.create_single_mode_widget()
        self.stacked_widget.addWidget(self.single_mode_widget)
        
        # 批量处理模式页面
        self.batch_mode_widget = BatchMagnifyWidget()
        self.stacked_widget.addWidget(self.batch_mode_widget)
        
        layout.addWidget(self.stacked_widget, stretch=1)

    def create_single_mode_widget(self):
        """创建单图模式的UI"""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        info_layout = QHBoxLayout()
        self.selection_info = QLabel("选中区域: 未选择")
        info_layout.addWidget(self.selection_info)
        info_layout.addStretch()
        left_layout.addLayout(info_layout)

        self.source_area = SelectableImageArea("拖拽或点击选择图像")
        self.source_area.imageDropped.connect(self.on_image_dropped)
        self.source_area.selectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.source_area, stretch=1)

        main_layout.addLayout(left_layout, stretch=1)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_layout.addWidget(QLabel("框选边长 (像素):"))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(10, 1000)
        self.size_spinbox.setValue(50)
        self.size_spinbox.setSuffix(" px")
        self.size_spinbox.valueChanged.connect(self.on_size_changed)
        right_layout.addWidget(self.size_spinbox)
        right_layout.addSpacing(10)

        right_layout.addWidget(QLabel("边框颜色:"))
        color_layout = QHBoxLayout()

        self.color_preview = QFrame()
        self.color_preview.setFixedSize(40, 30)
        self.color_preview.setStyleSheet(f"background-color: {self.border_color}; border: 1px solid #ccc;")
        color_layout.addWidget(self.color_preview)

        color_btn = StyledButton("选择颜色...", "secondary")
        color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(color_btn)
        color_layout.addStretch()

        right_layout.addLayout(color_layout)
        right_layout.addSpacing(20)

        preview_btn = StyledButton("预览效果", "secondary")
        preview_btn.clicked.connect(self.preview_result)
        right_layout.addWidget(preview_btn)

        process_btn = StyledButton("生成并保存...", "primary")
        process_btn.clicked.connect(self.process_and_save)
        right_layout.addWidget(process_btn)

        right_layout.addStretch()
        main_layout.addLayout(right_layout)

        return widget

    def on_mode_changed(self, index):
        """处理模式切换"""
        self.stacked_widget.setCurrentIndex(index)
    
    def on_selection_changed(self, x1, y1, x2, y2):
        self.selection_coords = (x1, y1, x2, y2)
        size = x2 - x1
        self.selection_info.setText(f"选中区域: ({x1}, {y1}) - ({x2}, {y2})  大小: {size}x{size}像素")
        self.size_spinbox.blockSignals(True)
        self.size_spinbox.setValue(size)
        self.size_spinbox.blockSignals(False)

    def on_size_changed(self, value):
        if self.image and self.source_area:
            self.source_area.set_selection_size(value)

    def choose_color(self):
        color = QColorDialog.getColor(QColor(self.border_color), self, "选择边框颜色")
        if color.isValid():
            self.border_color = color.name()
            self.color_preview.setStyleSheet(f"background-color: {self.border_color}; border: 1px solid #ccc;")
            self.source_area.set_border_color(self.border_color)

    def on_image_dropped(self, path):
        self.image = Image.open(path)
        self.source_area.set_border_color(self.border_color)
        self.source_area.load_image(path)
        self.selection_coords = None
        self.selection_info.setText("选中区域: 已自动在左上角生成，可拖动调整位置")
        img_size = min(self.image.size)
        default_size = max(10, img_size // 16)
        self.size_spinbox.setValue(default_size)

    def get_selection(self):
        if self.selection_coords:
            return self.selection_coords

        if self.image:
            w, h = self.image.size
            size = self.size_spinbox.value()
            return (0, 0, size, size)
        return None

    def preview_result(self):
        if not self.image:
            QMessageBox.warning(self, "警告", "请先选择图像")
            return

        selection = self.get_selection()
        if not selection:
            QMessageBox.warning(self, "警告", "请先框选要放大的区域")
            return

        x1, y1, x2, y2 = selection

        result = ImageMagnify.magnify_region(
            self.image, x1, y1, x2, y2,
            border_color=self.source_area.border_color,
        )

        if result:
            preview = PreviewWindow(result, "局部放大预览", self)
            preview.exec()

    def process_and_save(self):
        if not self.image:
            QMessageBox.warning(self, "警告", "请先选择图像")
            return

        selection = self.get_selection()
        if not selection:
            QMessageBox.warning(self, "警告", "请先框选要放大的区域")
            return

        x1, y1, x2, y2 = selection

        result = ImageMagnify.magnify_region(
            self.image, x1, y1, x2, y2,
            border_color=self.source_area.border_color,
        )

        if result:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存结果", generate_filename("magnify"),
                "PNG文件 (*.png);;JPEG文件 (*.jpg)"
            )
            if save_path:
                result.save(save_path)
                QMessageBox.information(self, "成功", "图像已保存")
