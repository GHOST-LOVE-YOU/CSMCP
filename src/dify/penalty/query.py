"""
行政处罚决定书查询工具
调用 Dify Workflow API
"""

import os
import httpx
from typing import Optional

from app import mcp

# 配置
DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/workflows/run")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")


@mcp.tool()
async def query_penalty(
    query: str,
    user_id: Optional[str] = None,
    timeout: int = 120
) -> str:
    """
    查询行政处罚决定书信息

    通过 Dify Workflow API 查询并生成行政处罚决定书摘要。
    输入案件相关信息，返回结构化的处罚决定书内容。

    Args:
        query: 查询内容，描述违法行为或案件信息
               例如："青岛花园大酒店有限公司在抽查时发现过期食品"
        user_id: 用户标识，用于追踪请求（可选，默认为 mcp-user）
        timeout: 请求超时时间（秒），默认120秒

    Returns:
        行政处罚决定
    """
    if not DIFY_API_KEY:
        return "错误: 未配置 DIFY_API_KEY 环境变量"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "query": query
        },
        "response_mode": "blocking",
        "user": user_id or "mcp-user"
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                DIFY_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()

            # 提取结果
            if "data" in data and "outputs" in data["data"]:
                result = data["data"]["outputs"].get("result", "")
                if result:
                    return result
                return f"Dify 返回空结果。原始响应: {data}"

            return f"Dify 响应格式异常: {data}"

    except httpx.TimeoutException:
        return f"错误: 请求超时（{timeout}秒）"
    except httpx.HTTPStatusError as e:
        return f"错误: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"错误: {type(e).__name__} - {str(e)}"
