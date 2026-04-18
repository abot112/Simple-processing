"""
图像处理核心模块
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional
import os


class ImageProcessor:
    """图像处理基础类"""
    
    @staticmethod
    def load_image(path: str) -> Optional[Image.Image]:
        """加载图像"""
        try:
            return Image.open(path).convert('RGB')
        except Exception as e:
            print(f"加载图像失败: {e}")
            return None
    
    @staticmethod
    def save_image(image: Image.Image, path: str, quality: int = 85) -> bool:
        """保存图像"""
        try:
            if path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
                image.save(path, quality=quality)
            else:
                image.save(path)
            return True
        except Exception as e:
            print(f"保存图像失败: {e}")
            return False
    
    @staticmethod
    def resize_to_fit(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
        """缩放图像以适应最大尺寸（保持比例）"""
        image.thumbnail(max_size, Image.LANCZOS)
        return image
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """创建缩略图（填充模式）"""
        img = image.copy()
        img.thumbnail(size, Image.LANCZOS)
        
        # 创建背景并居中粘贴
        background = Image.new('RGB', size, (245, 243, 239))
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        background.paste(img, (x, y))
        
        return background
