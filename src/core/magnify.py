from PIL import Image, ImageDraw, ImageColor
from typing import Optional, Union, Tuple
from .image_processor import ImageProcessor


def _resolve_outline_color(border_color: Union[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """Normalize Qt/CSS hex or tuple to an RGB tuple for PIL drawing."""
    if isinstance(border_color, tuple) and len(border_color) >= 3:
        return int(border_color[0]), int(border_color[1]), int(border_color[2])
    s = str(border_color).strip()
    try:
        return ImageColor.getrgb(s)
    except ValueError:
        return ImageColor.getrgb("#D97757")


class ImageMagnify(ImageProcessor):

    @staticmethod
    def magnify_region(image: Image.Image,
                      x1: int, y1: int, x2: int, y2: int,
                      scale: float = 2.0,
                      border_color: str = '#D97757') -> Optional[Image.Image]:

        try:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(image.width, x2)
            y2 = min(image.height, y2)

            if x2 - x1 < 10 or y2 - y1 < 10:
                return None

            # 必须为 RGB：灰度/调色板图上 ImageDraw 的 outline 只能是 int，RGB 三元组会报错
            base = image.convert("RGB")
            result = base.copy()
            draw = ImageDraw.Draw(result)

            line_color = _resolve_outline_color(border_color)
            line_width = 3

            draw.rectangle([x1, y1, x2, y2], outline=line_color, width=line_width)

            region = base.crop((x1, y1, x2, y2))

            quarter_w = base.width // 2
            quarter_h = base.height // 2

            target_size = (quarter_w, quarter_h)
            magnified = region.resize(target_size, Image.LANCZOS)

            overlay_x = base.width - quarter_w
            overlay_y = base.height - quarter_h

            result.paste(magnified, (overlay_x, overlay_y))

            border_width = 4
            draw.rectangle(
                [overlay_x - border_width, overlay_y - border_width,
                 overlay_x + quarter_w + border_width, overlay_y + quarter_h + border_width],
                outline=line_color, width=border_width
            )

            return result

        except Exception as e:
            print(f"局部放大失败: {e}")
            return None
