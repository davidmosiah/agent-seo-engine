from __future__ import annotations

import re
from enum import Enum
from typing import Any


class SearchIntent(Enum):
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial_investigation"


class SearchIntentAnalyzer:
    INFORMATIONAL_SIGNALS = [
        "what", "why", "how", "when", "where", "who", "guide", "tutorial",
        "learn", "tips", "best practices", "explained", "definition", "meaning",
    ]
    NAVIGATIONAL_SIGNALS = [
        "login", "sign in", "website", "official", "home page", "account",
        "dashboard", "portal", "app",
    ]
    TRANSACTIONAL_SIGNALS = [
        "buy", "purchase", "order", "download", "get", "pricing", "cost",
        "free trial", "sign up", "subscribe", "install", "coupon", "deal",
        "discount", "cheap", "affordable", "hire",
    ]
    COMMERCIAL_SIGNALS = [
        "best", "top", "review", "vs", "versus", "compare", "comparison",
        "alternative", "alternatives", "like", "similar", "better than",
        "instead of", "option", "choice",
    ]

    def analyze(
        self,
        keyword: str,
        serp_features: list[str] | None = None,
        top_results: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        keyword_lower = keyword.lower()
        scores = {intent: 0.0 for intent in SearchIntent}

        for intent, score in self._keyword_scores(keyword_lower).items():
            scores[intent] += score
        for intent, score in self._serp_scores(serp_features or []).items():
            scores[intent] += score
        for intent, score in self._result_scores(top_results or []).items():
            scores[intent] += score

        total = sum(scores.values())
        confidence = {
            intent.value: round((score / total * 100), 2) if total else 25.0
            for intent, score in scores.items()
        }
        primary = max(scores.items(), key=lambda item: item[1])[0] if total else SearchIntent.INFORMATIONAL
        ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        secondary = None
        if total and len(ordered) > 1:
            if confidence[ordered[0][0].value] - confidence[ordered[1][0].value] < 15:
                secondary = ordered[1][0]

        return {
            "keyword": keyword,
            "primary_intent": primary.value,
            "secondary_intent": secondary.value if secondary else None,
            "confidence": confidence,
            "signals_detected": self._detected_signals(keyword_lower, serp_features or []),
            "recommendations": self._recommendations(primary),
        }

    def _keyword_scores(self, keyword: str) -> dict[SearchIntent, float]:
        scores = {intent: 0.0 for intent in SearchIntent}
        for signal in self.INFORMATIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.INFORMATIONAL] += 2
        for signal in self.NAVIGATIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.NAVIGATIONAL] += 3
        for signal in self.TRANSACTIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.TRANSACTIONAL] += 2
        for signal in self.COMMERCIAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.COMMERCIAL] += 2
        if re.match(r"^(what|why|how|when|where|who|can|should|is|are|does)\b", keyword):
            scores[SearchIntent.INFORMATIONAL] += 3
        if re.search(r"\d+\s+(best|top)", keyword):
            scores[SearchIntent.COMMERCIAL] += 3
        return scores

    def _serp_scores(self, features: list[str]) -> dict[SearchIntent, float]:
        scores = {intent: 0.0 for intent in SearchIntent}
        for feature in features:
            value = feature.lower()
            if "snippet" in value or "people" in value or "knowledge" in value:
                scores[SearchIntent.INFORMATIONAL] += 2
            if "shopping" in value or "product" in value or "ad" in value:
                scores[SearchIntent.TRANSACTIONAL] += 2
            if "carousel" in value:
                scores[SearchIntent.COMMERCIAL] += 1
        return scores

    def _result_scores(self, results: list[dict[str, str]]) -> dict[SearchIntent, float]:
        scores = {intent: 0.0 for intent in SearchIntent}
        for result in results[:10]:
            combined = f"{result.get('title', '')} {result.get('description', '')}".lower()
            url = result.get("url", "").lower()
            if any(term in combined for term in ["guide", "how to", "what is", "tutorial"]):
                scores[SearchIntent.INFORMATIONAL] += 0.5
            if any(term in combined for term in ["best", "top", "review", "vs", "compare"]):
                scores[SearchIntent.COMMERCIAL] += 0.5
            if any(term in combined for term in ["buy", "price", "shop", "order", "get"]):
                scores[SearchIntent.TRANSACTIONAL] += 0.5
            if any(term in url for term in ["/product/", "/pricing", "/buy", "/shop", "/checkout"]):
                scores[SearchIntent.TRANSACTIONAL] += 0.5
        return scores

    def _detected_signals(self, keyword: str, serp_features: list[str]) -> dict[str, list[str]]:
        return {
            "keyword": [signal for signal in (
                self.INFORMATIONAL_SIGNALS + self.NAVIGATIONAL_SIGNALS + self.TRANSACTIONAL_SIGNALS + self.COMMERCIAL_SIGNALS
            ) if signal in keyword],
            "serp_features": serp_features,
        }

    def _recommendations(self, intent: SearchIntent) -> list[str]:
        if intent == SearchIntent.INFORMATIONAL:
            return ["Lead with a direct answer, then expand into steps, examples and FAQs."]
        if intent == SearchIntent.COMMERCIAL:
            return ["Use comparison tables, alternatives, decision criteria and clear evaluation language."]
        if intent == SearchIntent.TRANSACTIONAL:
            return ["Make pricing, trust signals, proof and conversion path obvious above the fold."]
        return ["Make brand/entity navigation unambiguous and link to the canonical destination early."]
