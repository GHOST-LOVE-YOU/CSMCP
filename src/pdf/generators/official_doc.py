"""
官方文档PDF生成器
"""

import os
import uuid
from datetime import datetime
from typing import Optional

from pdf.generators.base import BasePDFGenerator


class OfficialDocumentGenerator(BasePDFGenerator):
    """官方文档生成器（依法履职处理意见书等）"""

    # 页面配置
    LEFT_MARGIN = 25
    RIGHT_MARGIN = 185
    LINE_HEIGHT = 7

    def generate(
        self,
        document_number: str,
        title: str,
        recipient_name: str,
        recipient_gender: str,
        content: str,
        handler_name: str,
        contact_phone: str,
        stamp_image_path: Optional[str] = None,
        output_dir: str = "/tmp"
    ) -> str:
        """
        生成官方文档PDF
        """
        self.add_page()

        # 绘制红色边框装饰
        self._draw_border()

        # 1. 编号
        self._draw_document_number(document_number)

        # 2. 标题
        self._draw_title(title)

        # 3. 称呼
        y = self._draw_recipient(recipient_name, recipient_gender)

        # 4. 正文
        y = self._draw_content(content, y)

        # 5. 经办人和联系电话
        y = self._draw_contact_info(handler_name, contact_phone, y)

        # 6. 印章
        stamp_left, stamp_top, size = self._draw_stamp(stamp_image_path, y)
        stamp_pos = (stamp_left, stamp_top, size)

        # 7. 日期
        self._draw_date(y)

        # 保存
        filename = f"document_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(output_dir, filename)
        return self.save(output_path), stamp_pos

    def _draw_border(self):
        """绘制红色边框"""
        self.pdf.set_draw_color(220, 50, 50)
        self.pdf.set_line_width(3)
        self.pdf.line(8, 10, 8, 280)
        self.pdf.line(202, 10, 202, 280)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.2)

    def _draw_document_number(self, number: str):
        """绘制编号"""
        self.pdf.set_font('Chinese', '', 10)
        self.pdf.set_xy(150, 15)
        self.pdf.cell(40, 6, f'编号: {number}', align='R')

    def _draw_title(self, title: str):
        """绘制标题"""
        self.pdf.set_font('Chinese', '', 18)
        self.pdf.set_xy(self.LEFT_MARGIN, 30)
        self.pdf.cell(160, 10, title, align='C')

    def _draw_recipient(self, name: str, gender: str) -> float:
        """绘制收件人，返回下一行Y坐标"""
        self.pdf.set_font('Chinese', '', 11)
        self.pdf.set_xy(self.LEFT_MARGIN, 50)
        self.pdf.cell(0, self.LINE_HEIGHT, f'{name}{gender}：')
        return 62

    def _draw_content(self, content: str, start_y: float) -> float:
        """绘制正文内容，返回结束Y坐标"""
        y = start_y
        self.pdf.set_font('Chinese', '', 11)

        paragraphs = content.split('\n')
        for para in paragraphs:
            if para.strip():
                # 首行缩进
                self.pdf.set_xy(self.LEFT_MARGIN + 8, y)
                self.pdf.multi_cell(155, self.LINE_HEIGHT, para.strip(), align='L')
                y = self.pdf.get_y() + 2
            else:
                y += self.LINE_HEIGHT

        return y

    def _draw_contact_info(self, handler: str, phone: str, start_y: float) -> float:
        """绘制联系信息，返回结束Y坐标"""
        y = start_y + self.LINE_HEIGHT

        self.pdf.set_xy(self.LEFT_MARGIN, y)
        self.pdf.cell(0, self.LINE_HEIGHT, f'经办（联系）人：{handler}')

        y += self.LINE_HEIGHT
        self.pdf.set_xy(self.LEFT_MARGIN, y)
        self.pdf.cell(0, self.LINE_HEIGHT, f'联 系 电 话：{phone}')

        return y

    def _draw_stamp(self, stamp_path: Optional[str], y: float) -> tuple[float, float, float]:
        """
        绘制印章并返回印章位置信息

        Args:
            stamp_path: 印章图片路径
            y: 当前内容结束的Y坐标

        Returns:
            tuple: (left_x, top_y, size) 印章左上角坐标和尺寸，单位mm
        """
        # 印章配置
        stamp_center_x = 165  # 印章中心X坐标
        stamp_center_y = y + 25  # 印章中心Y坐标
        radius = 20  # 印章半径
        size = radius * 2  # 印章尺寸（宽=高）

        # 计算左上角坐标
        stamp_left = stamp_center_x - radius
        stamp_top = stamp_center_y - radius

        if stamp_path and os.path.exists(stamp_path):
            # 有印章图片，直接绘制
            self.pdf.image(stamp_path, stamp_left, stamp_top, size)
        else:
            # 无印章图片，绘制占位符
            self.pdf.set_draw_color(200, 200, 200)
            self.pdf.set_line_width(0.3)
            self.pdf.ellipse(stamp_left, stamp_top, size, size)

            # 占位文字
            self.pdf.set_font('Chinese', '', 8)
            self.pdf.set_text_color(150, 150, 150)
            self.pdf.set_xy(stamp_left, stamp_center_y - 3)
            self.pdf.cell(size, 6, '(盖章处)', align='C')

            # 恢复默认样式
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.set_draw_color(0, 0, 0)

        return stamp_left, stamp_top, size


    def _draw_date(self, y: float):
        """绘制日期"""
        self.pdf.set_font('Chinese', '', 10)
        today = datetime.now().strftime('%Y年%m月%d日')
        self.pdf.set_xy(140, y + 55)
        self.pdf.cell(50, 6, today, align='C')
