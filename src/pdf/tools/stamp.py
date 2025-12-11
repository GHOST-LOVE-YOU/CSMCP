"""
印章处理工具
"""

import os
from io import BytesIO
from typing import Optional

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from pdf.app import mcp


@mcp.tool()
def add_stamp_to_pdf(
    pdf_path: str,
    stamp_image_path: str = "./assets/stamps/default.png",
    x: float = 150,
    y: float = 200,
    size: float = 40,
    output_path: Optional[str] = None,
) -> str:
    """
    为已有PDF添加印章图片

    Args:
        pdf_path: 原PDF文件路径
        stamp_image_path: 印章图片路径（可选）
        x: 印章X坐标 (mm)
        y: 印章Y坐标 (mm)
        size: 印章大小 (mm)
        output_path: 输出路径（可选，默认覆盖原文件）

    Returns:
        处理后的PDF路径
    """
    MM_TO_PT = 2.834645
    PAGE_HEIGHT_MM = 297

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    if os.path.exists(stamp_image_path):
        # 用PIL预处理图片，确保透明度正确
        img = Image.open(stamp_image_path)

        # 如果有透明通道，转换为RGBA确保正确处理
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            # 保持RGBA模式
            img = img.convert("RGBA")

            # 保存到临时BytesIO，使用PNG格式保留透明度
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # 使用ImageReader处理透明PNG
            from reportlab.lib.utils import ImageReader

            img_reader = ImageReader(img_buffer)
        else:
            img_reader = stamp_image_path

        # 坐标转换
        x_pt = x * MM_TO_PT
        size_pt = size * MM_TO_PT
        y_pt = (PAGE_HEIGHT_MM - y - size) * MM_TO_PT

        # 绘制图片，mask='auto' 自动处理透明度
        c.drawImage(img_reader, x_pt, y_pt, width=size_pt, height=size_pt, mask="auto")

    c.save()
    packet.seek(0)

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    stamp_pdf = PdfReader(packet)
    stamp_page = stamp_pdf.pages[0]

    for page in reader.pages:
        page.merge_page(stamp_page)
        writer.add_page(page)

    output = output_path or pdf_path
    with open(output, "wb") as f:
        writer.write(f)

    return f"印章已添加: {output}"
