"""
全局配置文件
"""

# Claude暖色配色方案
COLORS = {
    # 主色调
    'background': '#FAF6F1',      # 米白/奶油色 - 主背景
    'accent': '#D97757',          # 暖橙/陶土色 - 强调色
    'text': '#2D2A26',            # 深炭色 - 文字
    'border': '#E8E0D5',          # 浅米灰 - 边框
    
    # 辅助色
    'secondary_bg': '#FFFFFF',    # 纯白 - 卡片/输入框
    'hover': '#E8C4B8',           # 浅暖橙 - 悬停
    'disabled': '#C9C3BA',        # 灰米色 - 禁用
    'success': '#6B8E6B',         # 柔和绿 - 成功
    'error': '#C75B5B',           # 柔和红 - 错误
    
    # 额外辅助色
    'light_bg': '#F5F3EF',        # 浅灰米 - 预览区背景
    'muted_text': '#9B9590',      # 浅灰 - 提示文字
    'tab_inactive': '#6B6560',    # 未选中标签文字
    'tab_hover': '#F0EBE3',       # 标签悬停背景
}

# 支持的图像格式
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']

# 默认设置
DEFAULT_SETTINGS = {
    'magnify_scale': 2.0,
    'layout_spacing': 10,
    'layout_margin': 20,
    'layout_dpi': 300,
    'output_quality': 85,
}

# 窗口尺寸
WINDOW_SIZE = (1200, 800)
MIN_WINDOW_SIZE = (900, 600)
