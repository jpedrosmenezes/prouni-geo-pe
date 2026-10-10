"""Figuras Plotly: tema escuro, marcas finas, rótulos diretos e tooltips em português."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from .constants import (
    COLOR_GRUPO,
    COLOR_TIPO,
    GRID,
    INK,
    PANEL,
    SURFACE,
    TEXT,
    TEXT_MUTED,
)
from .formatting import fmt_int, fmt_pct

FONT = "Inter, 'Source Sans Pro', -apple-system, 'Segoe UI', sans-serif"
CHART_CONFIG = {"displayModeBar": False, "scrollZoom": False}


def _base(fig: go.Figure, height: int, legend: bool = True) -> go.Figure:
    fig.update_layout(
        height=height,
        margin={"l": 0, "r": 8, "t": 8, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": FONT, "size": 13, "color": TEXT_MUTED},
        separators=",.",
        showlegend=legend,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "title_text": "",
            "font": {"color": TEXT, "size": 13},
            "traceorder": "normal",
        },
        hoverlabel={"bgcolor": PANEL, "bordercolor": GRID, "font": {"color": TEXT, "family": FONT}},
        bargap=0.38,
    )
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID, zeroline=False, tickfont={"color": TEXT_MUTED})
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, zeroline=False, tickfont={"color": TEXT}, automargin=True)
    return fig


def _mark(color: str) -> dict:
    return {"color": color, "line": {"color": SURFACE, "width": 2}}


def share_comparison(groups: dict[str, pd.Series], colors: dict[str, str], height: int = 190) -> go.Figure:
    rows = []
    for grupo, serie in groups.items():
        contagem = serie.dropna().value_counts()
        total = contagem.sum()
        for cat in colors:
            n = int(contagem.get(cat, 0))
            rows.append((grupo, cat, n / total * 100 if total else 0.0, n))
    dados = pd.DataFrame(rows, columns=["grupo", "cat", "pct", "n"])

    fig = go.Figure()
    for cat, cor in colors.items():
        sub = dados[dados["cat"] == cat]
        fig.add_bar(
            y=sub["grupo"],
            x=sub["pct"],
            name=cat,
            orientation="h",
            marker=_mark(cor),
            text=[fmt_pct(v) if v >= 8 else "" for v in sub["pct"]],  # segmentos finos ficam só no tooltip
            textposition="inside",
            insidetextanchor="middle",
            textfont={"color": INK, "size": 13, "family": FONT},
            customdata=sub["n"],
            hovertemplate=f"<b>%{{y}}</b><br>{cat}: %{{x:.1f}}% (%{{customdata:,.0f}} bolsas)<extra></extra>",
        )
    _base(fig, height)
    fig.update_layout(barmode="stack")
    fig.update_xaxes(range=[0, 100], ticksuffix="%", showgrid=False, showticklabels=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig


def stacked_by_tipo(
    df: pd.DataFrame,
    col: str,
    order: list[str] | None = None,
    height: int = 320,
    horizontal: bool = True,
) -> go.Figure:
    ct = pd.crosstab(df[col], df["tipo"]).reindex(columns=list(COLOR_TIPO), fill_value=0)
    if order is not None:
        ct = ct.reindex(order, fill_value=0)
    ct = ct[ct.sum(axis=1) > 0]
    if order is None:
        ct = ct.loc[ct.sum(axis=1).sort_values(ascending=False).index]

    cats = [str(c) for c in ct.index]
    totais = ct.sum(axis=1)
    grande_total = totais.sum()
    rotulos = [f"{fmt_int(n)} · {fmt_pct(n / grande_total * 100)}" for n in totais]

    fig = go.Figure()
    for tipo, cor in COLOR_TIPO.items():
        parte = ct[tipo] / totais * 100
        comuns = {
            "name": tipo,
            "marker": _mark(cor),
            "customdata": parte,
            "hovertemplate": (
                f"<b>%{{{'y' if horizontal else 'x'}}}</b><br>{tipo}: "
                f"%{{{'x' if horizontal else 'y'}:,.0f}} bolsas "
                "(%{customdata:.1f}% do grupo)<extra></extra>"
            ),
        }
        if horizontal:
            fig.add_bar(y=cats, x=ct[tipo], orientation="h", **comuns)
        else:
            fig.add_bar(x=cats, y=ct[tipo], **comuns)

    rotulo_comum = {
        "mode": "text",
        "text": rotulos,
        "textfont": {"color": TEXT, "size": 12, "family": FONT},
        "showlegend": False,
        "hoverinfo": "skip",
        "cliponaxis": False,
    }
    _base(fig, height)
    fig.update_layout(barmode="stack")
    if horizontal:
        fig.add_scatter(x=totais, y=cats, textposition="middle right", **rotulo_comum)
        fig.update_xaxes(range=[0, totais.max() * 1.38], showgrid=True, tickformat=",.0f")
        fig.update_yaxes(
            type="category", categoryorder="array", categoryarray=cats, autorange="reversed", showgrid=False
        )
    else:
        fig.add_scatter(x=cats, y=totais, textposition="top center", **rotulo_comum)
        fig.update_yaxes(range=[0, totais.max() * 1.22], showgrid=True, tickformat=",.0f")
        fig.update_xaxes(type="category", categoryorder="array", categoryarray=cats, showgrid=False)
    return fig


def top_municipios(summary: pd.DataFrame, n: int = 10, height: int = 420) -> go.Figure:
    top = summary.nlargest(n, "bolsas")
    nomes = top["nome"].tolist()

    fig = go.Figure()
    for grupo, cor in COLOR_GRUPO.items():
        sub = top[top["grupo"] == grupo]
        if sub.empty:
            continue
        fig.add_bar(
            y=sub["nome"],
            x=sub["bolsas"],
            name=grupo,
            orientation="h",
            marker=_mark(cor),
            text=[fmt_int(v) for v in sub["bolsas"]],
            textposition="outside",
            textfont={"color": TEXT, "size": 12, "family": FONT},
            cliponaxis=False,
            customdata=sub["pct_integral"].fillna(0),
            hovertemplate=(
                "<b>%{y}</b><br>%{x:,.0f} bolsas<br>"
                f"{grupo}<br>%{{customdata:.1f}}% integrais<extra></extra>"
            ),
        )
    _base(fig, height)
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(showgrid=True, tickformat=",.0f", range=[0, top["bolsas"].max() * 1.15])
    fig.update_yaxes(
        type="category", categoryorder="array", categoryarray=nomes, autorange="reversed", showgrid=False
    )
    return fig
