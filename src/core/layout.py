"""
图像排版模块
"""
from PIL import Image, ImageDraw, ImageFont
from typing import List, Optional, Dict
from .image_processor import ImageProcessor


class ImageLayout(ImageProcessor):
    """图像排版处理器"""
    
    @staticmethod
    def create_layout(images: List[Image.Image],
                     rows: int, 
                     cols: int,
                     spacing: int = 10,
                     margin: int = 20,
                     dpi: int = 300,
                     title: str = "",
                     row_labels: Optional[List[str]] = None,
                     col_labels: Optional[List[str]] = None) -> Optional[Image.Image]:
        """
        创建图像拼图
        
        Args:
            images: 图像列表（按行优先排列）
            rows: 行数
            cols: 列数
            spacing: 图像间距（像素）
            margin: 边距（像素）
            dpi: 输出分辨率
            title: 总标题
            row_labels: 行标签列表
            col_labels: 列标签列表
        
        Returns:
            排版后的图像
        """
        try:
            # 计算总尺寸（假设每个格子300x300像素作为基础）
            cell_size = 300
            total_width = margin * 2 + cols * cell_size + (cols - 1) * spacing
            total_height = margin * 2 + rows * cell_size + (rows - 1) * spacing
            
            # 添加标题空间
            title_height = 60 if title else 0
            total_height += title_height
            
            # 创建画布
            canvas = Image.new('RGB', (total_width, total_height), (250, 246, 241))
            draw = ImageDraw.Draw(canvas)
            
            # 绘制标题
            if title:
                try:
                    font = ImageFont.truetype("arial.ttf", 32)
                except:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), title, font=font)
                text_width = bbox[2] - bbox[0]
                x = (total_width - text_width) // 2
                draw.text((x, 20), title, fill='#2D2A26', font=font)
            
            # 放置图像
            for idx, img in enumerate(images[:rows * cols]):
                if img is None:
                    continue
                    
                row = idx // cols
                col = idx % cols
                
                x = margin + col * (cell_size + spacing)
                y = margin + row * (cell_size + spacing) + title_height
                
                # 调整图像大小并居中
                resized = ImageLayout._resize_for_cell(img, cell_size)
                canvas.paste(resized, (x, y))
                
                # 绘制标签
                if row_labels and col == 0 and row < len(row_labels):
                    try:
                        label_font = ImageFont.truetype("arial.ttf", 16)
                    except:
                        label_font = ImageFont.load_default()
                    draw.text((5, y + cell_size // 2), row_labels[row], 
                             fill='#D97757', font=label_font)
                
                if col_labels and row == 0 and col < len(col_labels):
                    try:
                        label_font = ImageFont.truetype("arial.ttf", 16)
                    except:
                        label_font = ImageFont.load_default()
                    bbox = draw.textbbox((0, 0), col_labels[col], font=label_font)
                    text_width = bbox[2] - bbox[0]
                    draw.text((x + (cell_size - text_width) // 2, title_height + 5), 
                             col_labels[col], fill='#D97757', font=label_font)
            
            return canvas
            
        except Exception as e:
            print(f"图像排版失败: {e}")
            return None
    
    @staticmethod
    def _resize_for_cell(image: Image.Image, cell_size: int) -> Image.Image:
        """调整图像大小以适应格子（保持比例，居中填充）"""
        img = image.copy()
        img.thumbnail((cell_size, cell_size), Image.LANCZOS)
        
        # 创建背景
        background = Image.new('RGB', (cell_size, cell_size), (255, 255, 255))
        x = (cell_size - img.width) // 2
        y = (cell_size - img.height) // 2
        background.paste(img, (x, y))
        
        return background
