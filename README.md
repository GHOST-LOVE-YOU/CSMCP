# PDF Document MCP Server

基于 FastMCP 的中文官方文档 PDF 生成服务。

## 项目结构

```
pdf-mcp-server/
├── pyproject.toml          # 项目配置
├── src/
│   └── pdf/
│       ├── server.py       # FastMCP 入口
│       ├── tools/          # MCP 工具定义
│       │   ├── document.py # 文档生成工具
│       │   └── stamp.py    # 印章处理工具
│       ├── generators/     # PDF 生成器
│       │   ├── base.py     # 基类
│       │   └── official_doc.py
│       ├── templates/      # 模板配置
│       └── utils/          # 工具函数
├── assets/                 # 静态资源
│   ├── fonts/
│   └── stamps/
└── tests/
```

## 安装

```bash
# 使用 uv
uv sync

# 或 pip
pip install -e .
```

## 运行

```bash
# 开发模式
uv run fastmcp dev src/pdf/server.py

# 生产模式
uv run fastmcp run src/pdf/server.py
```

## 可用工具

### generate_official_document

生成官方文档 PDF（如依法履职处理意见书）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| document_number | string | ✓ | 文档编号 |
| title | string | ✓ | 文档标题 |
| recipient_name | string | ✓ | 收件人姓名 |
| recipient_gender | string | ✓ | 先生/女士 |
| content | string | ✓ | 正文内容 |
| handler_name | string | ✓ | 经办人 |
| contact_phone | string | ✓ | 联系电话 |
| stamp_image_path | string | ✗ | 印章图片 |
| output_dir | string | ✗ | 输出目录 |

### add_stamp_to_pdf

为已有 PDF 添加印章

## 扩展指南

### 添加新工具

1. 在 `tools/` 下创建新文件
2. 使用 `@mcp.tool()` 装饰器
3. 在 `tools/__init__.py` 中导入

```python
# tools/my_tool.py
from pdf_mcp.server import mcp

@mcp.tool()
def my_new_tool(param: str) -> str:
    """工具描述"""
    return "result"
```

### 添加新生成器

1. 继承 `BasePDFGenerator`
2. 实现 `generate()` 方法

```python
from pdf_mcp.generators.base import BasePDFGenerator

class MyGenerator(BasePDFGenerator):
    def generate(self, **kwargs) -> str:
        self.add_page()
        # ... 生成逻辑
        return self.save(output_path)
```
