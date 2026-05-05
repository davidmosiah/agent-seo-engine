from __future__ import annotations


def prioritize_opportunity(
    impressions: int = 0,
    clicks: int = 0,
    position: float = 100.0,
    conversions: float = 0.0,
    commercial_intent: float = 0.5,
) -> dict:
    volume_score = min(100.0, max(0.0, impressions / 50))
    position_score = _position_score(position)
    ctr = clicks / impressions if impressions else 0.0
    expected_ctr = _expected_ctr(position)
    ctr_gap_score = min(100.0, max(0.0, (expected_ctr - ctr) / max(expected_ctr, 0.01) * 100))
    conversion_score = min(100.0, conversions * 25)
    intent_score = min(100.0, max(0.0, commercial_intent * 100))

    final = round(
        volume_score * 0.25
        + position_score * 0.25
        + ctr_gap_score * 0.20
        + intent_score * 0.20
        + conversion_score * 0.10,
        2,
    )
    return {
        "final_score": final,
        "priority": "high" if final >= 75 else "medium" if final >= 50 else "low",
        "score_breakdown": {
            "volume": round(volume_score, 1),
            "position": round(position_score, 1),
            "ctr_gap": round(ctr_gap_score, 1),
            "commercial_intent": round(intent_score, 1),
            "conversions": round(conversion_score, 1),
        },
        "recommended_action": _action(position, ctr_gap_score),
    }


def _position_score(position: float) -> float:
    if position <= 3:
        return 70
    if position <= 10:
        return 85
    if position <= 20:
        return 100
    if position <= 50:
        return 60
    return 25


def _expected_ctr(position: float) -> float:
    if position <= 1:
        return 0.31
    if position <= 3:
        return 0.12
    if position <= 10:
        return 0.04
    if position <= 20:
        return 0.012
    return 0.004


def _action(position: float, ctr_gap_score: float) -> str:
    if 8 < position <= 20:
        return "Refresh content and internal links to push the URL onto page one."
    if position <= 10 and ctr_gap_score > 40:
        return "Rewrite title and meta description to improve CTR."
    if position > 20:
        return "Build a stronger article or hub page before expecting ranking movement."
    return "Monitor and improve topical depth selectively."
