from agent_seo_engine.agent import build_agent_manifest, build_connection_status, build_privacy_audit
from agent_seo_engine.intent import SearchIntentAnalyzer
from agent_seo_engine.quality import score_markdown


def test_agent_manifest_is_agent_first_and_secret_free():
    manifest = build_agent_manifest(client="codex")

    assert manifest["project"] == "agent-seo-engine"
    assert manifest["client"] == "codex"
    assert "agent_seo_score_content" in manifest["standard_tools"]
    assert "hermes" in manifest["supported_clients"]
    assert "secret" not in str(manifest).lower()


def test_connection_status_defaults_to_local_offline_mode():
    status = build_connection_status(env={})

    assert status["ok"] is True
    assert status["mode"] == "offline"
    assert status["external_services_configured"] == []


def test_privacy_audit_keeps_content_and_keys_local():
    audit = build_privacy_audit()

    assert audit["secrets_returned_to_agent"] is False
    assert ".env" in audit["local_files_ignored"]
    assert any("local" in rule.lower() for rule in audit["safety_rules"])


def test_search_intent_uses_existing_seo_signal_model():
    analyzer = SearchIntentAnalyzer()

    assert analyzer.analyze("how to build an MCP server")["primary_intent"] == "informational"
    assert analyzer.analyze("best ai agent framework")["primary_intent"] == "commercial_investigation"
    assert analyzer.analyze("ai automation pricing")["primary_intent"] == "transactional"


def test_quality_score_flags_actionable_article_gaps():
    markdown = """---
title: AI Agent Testing
description: Short.
keywords:
  - ai agent testing
---

# AI Agent Testing

Short intro about ai agent testing.

## Checklist

Use tests before launching.
"""

    result = score_markdown(markdown, primary_keyword="ai agent testing")

    assert result["overall_score"] < 90
    assert result["publishing_ready"] is False
    assert "meta_description" in result["checks"]
    assert any("description" in item.lower() for item in result["recommendations"])
