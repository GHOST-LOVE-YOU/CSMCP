"""
官方文档生成工具
"""

from typing import Optional
from pydantic import BaseModel, Field

from pdf.app import mcp
from pdf.generators.official_doc import OfficialDocumentGenerator


class DocumentParams(BaseModel):
    """文档参数"""
    document_number: str = Field(description="文档编号，如 '2024-001'")
    title: str = Field(description="文档标题，如 '依法履职处理意见书'")
    recipient_name: str = Field(description="收件人姓名")
    recipient_gender: str = Field(description="称呼：先生 或 女士")
    content: str = Field(description="正文内容，支持\\n换行分段")
    handler_name: str = Field(description="经办人姓名")
    contact_phone: str = Field(description="联系电话")
    stamp_image_path: Optional[str] = Field(default=None, description="印章图片路径（可选）")
    output_dir: str = Field(default="/tmp", description="输出目录")


@mcp.tool()
def generate_official_document(
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
    生成中文官方文档PDF（如依法履职处理意见书）

    Args:
        document_number: 文档编号，如 '2024-001'
        title: 文档标题，如 '依法履职处理意见书'
        recipient_name: 收件人姓名
        recipient_gender: 称呼（先生/女士）
        content: 正文内容，支持\\n换行分段
        handler_name: 经办人姓名
        contact_phone: 联系电话
        stamp_image_path: 印章图片路径（可选，留空显示占位符）
        output_dir: 输出目录，默认 /tmp

    Returns:
        生成的PDF文件路径
    """
    generator = OfficialDocumentGenerator()

    output_path, stamp_pos = generator.generate(
        document_number=document_number,
        title=title,
        recipient_name=recipient_name,
        recipient_gender=recipient_gender,
        content=content,
        handler_name=handler_name,
        contact_phone=contact_phone,
        stamp_image_path=stamp_image_path,
        output_dir=output_dir
    )

    return f"PDF文档已生成: {output_path}, 印章位置:{stamp_pos}"
