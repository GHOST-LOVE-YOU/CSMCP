"""
字体工具
"""

import os

from fpdf import FPDF

# 支持的中文字体路径（按优先级）
CHINESE_FONT_PATHS = [
    "/usr/share/fonts/MapleMono-NF-CN-unhinted/MapleMono-NF-CN-BoldItalic.ttf",  # Ubuntu/Debian
]


def find_chinese_font() -> str:
    """查找可用的中文字体"""
    for path in CHINESE_FONT_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("未找到可用的中文字体，请安装 fonts-wqy-zenhei")


def register_chinese_font(pdf: FPDF, font_name: str = "Chinese"):
    """为FPDF注册中文字体"""
    font_path = find_chinese_font()
    pdf.add_font(font_name, "", font_path)
