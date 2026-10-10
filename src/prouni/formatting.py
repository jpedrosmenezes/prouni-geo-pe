"""Formatação de números no padrão brasileiro (1.234,5)."""

from __future__ import annotations


def fmt_int(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".")


def fmt_pct(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}".replace(".", ",") + "%"


def fmt_pp(value: float, decimals: int = 1) -> str:
    sign = "+" if value > 0 else "-" if value < 0 else ""
    return f"{sign}{abs(value):.{decimals}f}".replace(".", ",") + " p.p."
