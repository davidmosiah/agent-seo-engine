from __future__ import annotations

from collections.abc import Mapping

SUPPORTED_CLIENTS = ["generic", "claude", "codex", "cursor", "windsurf", "hermes", "openclaw"]


def _safe_client(client: str = "generic") -> str:
    return client if client in SUPPORTED_CLIENTS else "generic"


def _present(env: Mapping[str, str], key: str) -> bool:
    return bool(str(env.get(key, "")).strip())


def build_agent_manifest(client: str = "generic") -> dict:
    return {
        "project": "agent-seo-engine",
        "mcp_name": "io.github.davidmosiah/agent-seo-engine",
        "client": _safe_client(client),
        "package": {
            "pip": "pipx install agent-seo-engine[mcp]",
            "cli": "agent-seo-engine",
            "mcp": "agent-seo-mcp",
        },
        "supported_clients": SUPPORTED_CLIENTS,
        "standard_tools": [
            "agent_seo_manifest",
            "agent_seo_connection_status",
            "agent_seo_privacy_audit",
            "agent_seo_detect_intent",
            "agent_seo_score_content",
            "agent_seo_prioritize_opportunity",
        ],
        "recommended_first_calls": ["agent_seo_connection_status", "agent_seo_privacy_audit"],
        "default_mode": "local_offline",
        "hermes": {
            "config_path": "~/.hermes/config.yaml",
            "tool_name_prefix": "mcp_agent_seo_",
            "recommended_config": (
                "mcp_servers:\n"
                "  agent_seo:\n"
                "    command: agent-seo-mcp\n"
                "    args: []\n"
                "    sampling:\n"
                "      enabled: false"
            ),
        },
        "agent_rules": [
            "Start with connection status before content operations.",
            "Use local content paths or explicit text from the user.",
            "Do not send drafts to analytics providers unless the user asks.",
            "Return exact checks and next actions, not generic SEO advice.",
        ],
    }


def build_connection_status(env: Mapping[str, str] | None = None) -> dict:
    env = env or {}
    services = []
    if _present(env, "GEMINI_API_KEY") or _present(env, "GOOGLE_API_KEY"):
        services.append("gemini")
    if _present(env, "GA4_PROPERTY_ID"):
        services.append("ga4")
    if _present(env, "GSC_SITE_URL"):
        services.append("google_search_console")

    return {
        "ok": True,
        "mode": "offline" if not services else "offline_plus_optional_integrations",
        "external_services_configured": services,
        "ready_for_content_scoring": True,
        "ready_for_mcp": True,
        "next_steps": [
            "Run agent-seo-engine score --file <markdown> --primary-keyword <keyword>.",
            "Use optional analytics environment only for reports that require it.",
        ],
    }


def build_privacy_audit() -> dict:
    return {
        "project": "agent-seo-engine",
        "secrets_returned_to_agent": False,
        "local_files_ignored": [".env", "credentials/", "node_modules/", ".agent-data/", "coverage/"],
        "external_services": ["optional: Gemini", "optional: GA4", "optional: Google Search Console"],
        "data_boundary": "Content scoring, intent detection and opportunity scoring run locally by default.",
        "safety_rules": [
            "Keep drafts local unless an optional integration is explicitly requested.",
            "Do not commit credentials, analytics exports or unpublished content plans.",
            "Prefer structured JSON output for agents and markdown only for human review.",
            "Treat generated recommendations as editorial suggestions, not automatic publishing approval.",
        ],
    }
