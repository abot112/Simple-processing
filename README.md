# ImageTool — 图像处理工具

基于 **PyQt6** 的桌面图像小工具，提供图像相减、局部放大与拼图排版三类常用操作，界面采用暖色配色与中文界面。

## 功能概览

| 模块 | 说明 |
|------|------|
| **图像相减** | 加载两张图像，在统一尺寸后进行像素级运算，支持多种相减方式（如绝对值差、简单相减、差分高亮等），便于对比前后差异。 |
| **局部放大** | 在图像上框选矩形区域，在原图一角叠加放大预览，并绘制选区边框，适合标注与说明局部细节。 |
| **图像排版** | 将多张图片按行列排成网格，可设置间距、边距、输出 DPI、标题及行列标签，生成单张拼图便于报告或展示。 |

支持的输入格式：**PNG、JPG/JPEG、BMP**（见 `src/config.py` 中的 `SUPPORTED_FORMATS`）。

## 环境要求

- **Python** 3.9+（建议 3.10 及以上）
- **操作系统**：Windows（项目内含 `start.bat`；其他系统可直接用命令行启动）

## 安装依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

主要依赖：**PyQt6**、**Pillow**、**numpy**、**opencv-python**。

## 运行方式

**Windows：** 双击根目录下的 `start.bat`，或在命令行中：

```bash
cd "项目根目录"
python src/main.py
```

**说明：** 程序从 `src/main.py` 启动，已配置高 DPI 与「微软雅黑」全局字体。

## 项目结构（简要）

```
├── start.bat              # Windows 快速启动
├── requirements.txt       # Python 依赖
├── src/
│   ├── main.py            # 程序入口
│   ├── config.py          # 配色、默认参数、窗口尺寸等
│   ├── core/              # 图像算法：相减、放大、排版
│   ├── ui/                # 主窗口与各功能标签页、组件
│   └── utils/             # 文件等工具函数
```

## 配置说明

可在 `src/config.py` 中调整：

- **COLORS**：界面配色
- **DEFAULT_SETTINGS**：如放大倍数、排版间距/边距/DPI、输出 JPEG 质量等
- **WINDOW_SIZE / MIN_WINDOW_SIZE**：主窗口默认与最小尺寸

## 许可证

若需对外分发，请自行补充许可证文件（本项目仓库未默认附带）。
