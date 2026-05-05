from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .agent import build_agent_manifest, build_connection_status, build_privacy_audit
from .intent import SearchIntentAnalyzer
from .opportunity import prioritize_opportunity
from .quality import score_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-seo-engine")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    sub = parser.add_subparsers(dest="command", required=True)

    manifest = sub.add_parser("manifest")
    manifest.add_argument("--client", default="generic")

    sub.add_parser("doctor")
    sub.add_parser("privacy-audit")

    intent = sub.add_parser("intent")
    intent.add_argument("keyword")

    score = sub.add_parser("score")
    score.add_argument("--file", required=True)
    score.add_argument("--primary-keyword", default="")
    score.add_argument("--min-words", type=int, default=900)

    opp = sub.add_parser("opportunity")
    opp.add_argument("--impressions", type=int, default=0)
    opp.add_argument("--clicks", type=int, default=0)
    opp.add_argument("--position", type=float, default=100.0)
    opp.add_argument("--conversions", type=float, default=0.0)
    opp.add_argument("--commercial-intent", type=float, default=0.5)

    args = parser.parse_args(argv)

    if args.command == "manifest":
      payload = build_agent_manifest(args.client)
    elif args.command == "doctor":
      payload = build_connection_status(os.environ)
    elif args.command == "privacy-audit":
      payload = build_privacy_audit()
    elif args.command == "intent":
      payload = SearchIntentAnalyzer().analyze(args.keyword)
    elif args.command == "score":
      payload = score_markdown(Path(args.file).read_text(encoding="utf-8"), args.primary_keyword, args.min_words)
    elif args.command == "opportunity":
      payload = prioritize_opportunity(args.impressions, args.clicks, args.position, args.conversions, args.commercial_intent)
    else:
      parser.error("unknown command")

    print(_format(payload, args.format))
    return 0


def _format(payload: dict, response_format: str) -> str:
    if response_format == "markdown":
        return "# Agent SEO Engine\n\n```json\n" + json.dumps(payload, indent=2, ensure_ascii=False) + "\n```"
    return json.dumps(payload, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    raise SystemExit(main())
