# Agent SEO Engine

[![CI](https://github.com/davidmosiah/agent-seo-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/davidmosiah/agent-seo-engine/actions/workflows/ci.yml)

Agent-first SEO scoring, search-intent detection and opportunity prioritization. It packages the useful parts of a production content pipeline into a clean local CLI plus an optional MCP server for Codex, Claude, Cursor, Hermes, OpenClaw and other agent runtimes.

## What It Does

- Classifies search intent: informational, navigational, transactional and commercial investigation
- Scores markdown articles for agent-readable SEO gaps
- Prioritizes GSC-style opportunities by impressions, position, CTR gap, conversions and commercial value
- Exposes `manifest`, `connection_status` and `privacy_audit` surfaces before content tools
- Runs locally by default with no required API keys

## Install

```bash
pipx install "git+https://github.com/davidmosiah/agent-seo-engine.git"
```

With MCP support:

```bash
pipx install "git+https://github.com/davidmosiah/agent-seo-engine.git#egg=agent-seo-engine[mcp]"
```

PyPI artifacts are build-ready. Registry publish is pending a PyPI API token or trusted-publishing setup.

## CLI

```bash
agent-seo-engine manifest --client codex
agent-seo-engine doctor
agent-seo-engine privacy-audit
agent-seo-engine intent "best ai agent framework"
agent-seo-engine score --file examples/article.md --primary-keyword "ai agent testing"
agent-seo-engine opportunity --impressions 4200 --clicks 80 --position 12.4 --commercial-intent 0.8
```

All commands return structured JSON by default. Use `--format markdown` for human review.

## MCP

```bash
agent-seo-mcp
```

Hermes-style config:

```yaml
mcp_servers:
  agent_seo:
    command: agent-seo-mcp
    args: []
    sampling:
      enabled: false
```

Recommended first calls:

1. `agent_seo_connection_status`
2. `agent_seo_privacy_audit`
3. `agent_seo_score_content`

## Agent Contract

Agents should not guess whether a draft is ready. They should call the scoring tool, read exact failed checks, then propose focused edits. The engine is intentionally deterministic and local so repeated agent runs can compare output over time.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m compileall -q src
```
