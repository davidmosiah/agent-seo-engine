"""Catch SDK major-version drift using local tools, without a transport."""
import asyncio
import pytest

pytest.importorskip('mcp')
from agent_seo_engine.mcp_server import create_mcp


def test_real_sdk_registers_and_calls_local_tools():
    async def check():
        mcp = create_mcp()
        names = {tool.name for tool in await mcp.list_tools()}
        assert 'agent_seo_detect_intent' in names
        result = await mcp.call_tool('agent_seo_detect_intent', {'keyword': 'how to test'})
        assert result
    asyncio.run(check())
