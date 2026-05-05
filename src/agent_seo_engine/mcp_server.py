from __future__ import annotations

import os
from pathlib import Path

from .agent import build_agent_manifest, build_connection_status, build_privacy_audit
from .intent import SearchIntentAnalyzer
from .opportunity import prioritize_opportunity
from .quality import score_markdown


def create_mcp():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install MCP support with: pip install 'agent-seo-engine[mcp]'") from exc

    mcp = FastMCP("agent-seo-engine")

    @mcp.tool()
    def agent_seo_manifest(client: str = "generic") -> dict:
        return build_agent_manifest(client)

    @mcp.tool()
    def agent_seo_connection_status() -> dict:
        return build_connection_status(os.environ)

    @mcp.tool()
    def agent_seo_privacy_audit() -> dict:
        return build_privacy_audit()

    @mcp.tool()
    def agent_seo_detect_intent(keyword: str) -> dict:
        return SearchIntentAnalyzer().analyze(keyword)

    @mcp.tool()
    def agent_seo_score_content(markdown: str = "", file_path: str = "", primary_keyword: str = "") -> dict:
        text = markdown or Path(file_path).read_text(encoding="utf-8")
        return score_markdown(text, primary_keyword=primary_keyword)

    @mcp.tool()
    def agent_seo_prioritize_opportunity(
        impressions: int = 0,
        clicks: int = 0,
        position: float = 100.0,
        conversions: float = 0.0,
        commercial_intent: float = 0.5,
    ) -> dict:
        return prioritize_opportunity(impressions, clicks, position, conversions, commercial_intent)

    return mcp


def main() -> None:
    create_mcp().run()


if __name__ == "__main__":
    main()
