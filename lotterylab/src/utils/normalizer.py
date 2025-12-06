from __future__ import annotations

def normalize_game_type(raw: str, provider: str | None = None) -> str:
    v = (raw or "").strip().lower()
    p = (provider or "").strip().lower()
    # Polish Totalizator equivalent mappings
    if v in {"lotto plus", "plus", "lotto_plus"}:
        return "lotto_plus"
    if v in {"lotto"}:
        return "lotto"
    if v in {"mini lotto", "minilotto", "mini_lotto"}:
        return "mini_lotto"
    # fallback to safe slug
    return v.replace(" ", "_")
