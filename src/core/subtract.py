"""
图像相减模块
"""
import numpy as np
from PIL import Image
from typing import Optional
from .image_processor import ImageProcessor


class ImageSubtract(ImageProcessor):
    """图像相减处理器"""
    
    @staticmethod
    def subtract_images(img1: Image.Image, img2: Image.Image, 
                       method: str = 'absolute') -> Optional[Image.Image]:
        """
        相减两张图像
        
        Args:
            img1: 被减数图像
            img2: 减数图像
            method: 相减方法 ('absolute', 'simple', 'diff')
        
        Returns:
            相减后的图像
        """
        try:
            # 统一图像尺寸（以较大者为准）
            w1, h1 = img1.size
            w2, h2 = img2.size
            target_w, target_h = max(w1, w2), max(h1, h2)
            
            # 调整两张图像到相同尺寸
            img1_resized = img1.resize((target_w, target_h), Image.LANCZOS)
            img2_resized = img2.resize((target_w, target_h), Image.LANCZOS)
            
            # 转换为numpy数组
            arr1 = np.array(img1_resized).astype(np.float32)
            arr2 = np.array(img2_resized).astype(np.float32)
            
            # 根据方法计算
            if method == 'absolute':
                # 绝对值相减
                result = np.abs(arr1 - arr2)
            elif method == 'simple':
                # 简单相减（可能出现负值，需要归一化）
                result = arr1 - arr2
                result = (result - result.min()) / (result.max() - result.min()) * 255
            elif method == 'diff':
                # 差分显示（红色表示差异）
                diff = np.abs(arr1 - arr2)
                result = np.zeros_like(arr1)
                result[:, :, 0] = diff[:, :, 0]  # R通道
                result[:, :, 1] = arr1[:, :, 1] * 0.5  # G通道淡化
                result[:, :, 2] = arr1[:, :, 2] * 0.5  # B通道淡化
            else:
                result = np.abs(arr1 - arr2)
            
            # 确保值在0-255范围内
            result = np.clip(result, 0, 255).astype(np.uint8)
            
            # 转换回PIL Image
            return Image.fromarray(result)
            
        except Exception as e:
            print(f"图像相减失败: {e}")
            return None
