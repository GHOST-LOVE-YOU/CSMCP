"""
PDF生成器基类
"""

from abc import ABC, abstractmethod
from fpdf import FPDF
from pdf.utils.fonts import register_chinese_font


class BasePDFGenerator(ABC):
    """PDF生成器基类"""
    
    def __init__(self):
        self.pdf = FPDF()
        self._setup_fonts()
    
    def _setup_fonts(self):
        """设置字体"""
        register_chinese_font(self.pdf)
    
    @abstractmethod
    def generate(self, **kwargs) -> str:
        """生成PDF，返回文件路径"""
        pass
    
    def add_page(self):
        """添加新页面"""
        self.pdf.add_page()
    
    def save(self, output_path: str):
        """保存PDF"""
        self.pdf.output(output_path)
        return output_path
