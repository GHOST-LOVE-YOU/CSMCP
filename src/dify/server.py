"""
Dify MCP Server - FastMCP Entry Point
"""

from pathlib import Path

from app import mcp
from dotenv import load_dotenv

# 明确指定项目根目录的 .env
ROOT = Path(__file__).resolve().parents[2]  # src/dify/server.py -> CSMCP
load_dotenv(ROOT / ".env")

# 导入工具模块，让 @mcp.tool() 装饰器执行注册
import penalty.query  # noqa: F401,E402


def main():
    """启动 MCP 服务器"""
    mcp.run()


if __name__ == "__main__":
    main()
