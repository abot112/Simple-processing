"""
工具函数
"""
import os
from typing import List, Optional


def get_supported_images(folder: str) -> List[str]:
    """获取文件夹中所有支持的图像文件"""
    supported = ['.png', '.jpg', '.jpeg', '.bmp']
    images = []
    
    for file in os.listdir(folder):
        if any(file.lower().endswith(ext) for ext in supported):
            images.append(os.path.join(folder, file))
    
    return sorted(images)


def validate_image_path(path: str) -> bool:
    """验证图像路径是否有效"""
    if not os.path.exists(path):
        return False
    
    supported = ['.png', '.jpg', '.jpeg', '.bmp']
    return any(path.lower().endswith(ext) for ext in supported)


def generate_filename(prefix: str, original_name: str = "", suffix: str = ".png") -> str:
    """生成输出文件名"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if original_name:
        base = os.path.splitext(os.path.basename(original_name))[0]
        return f"{prefix}_{timestamp}_{base}{suffix}"
    else:
        return f"{prefix}_{timestamp}{suffix}"
