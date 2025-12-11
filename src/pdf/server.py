"""
PDF Document MCP Server - FastMCP Entry Point
"""

import sys
from pathlib import Path

# 当前文件: CSMCP/src/pdf/server.py
# 项目根目录的 src 目录路径 => CSMCP/src
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pdf.tools.document  # noqa: F401,E402
import pdf.tools.stamp  # noqa: F401,E402
from pdf.app import mcp  # 再导入 mcp


def main():
    """启动 MCP 服务器"""
    mcp.run()


if __name__ == "__main__":
    main()
