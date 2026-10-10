"""Mapa coroplético em SVG responsivo, gerado em Python."""

from __future__ import annotations

import math
from html import escape

import geopandas as gpd
import pandas as pd

from .constants import GRID, SURFACE, TEXT, TEXT_MUTED
from .formatting import fmt_int

NORONHA = "FERNANDO DE NORONHA"
K = 160.0
COS_LAT = math.cos(math.radians(8.4))
PAD = 14.0
INSET_W = 96.0
INSET_ZOOM = 4.0


def _proj(lon: float, lat: float) -> tuple[float, float]:
    return lon * COS_LAT * K, -lat * K


def _path(geom, dx: float, dy: float, zoom: float = 1.0, center: tuple[float, float] | None = None) -> str:
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    partes = []
    for poly in polys:
        for anel in [poly.exterior, *poly.interiors]:
            pts = []
            for lon, lat in anel.coords:
                x, y = _proj(lon, lat)
                if center is not None:
                    x, y = center[0] + (x - center[0]) * zoom, center[1] + (y - center[1]) * zoom
                pts.append(f"{x + dx:.1f} {y + dy:.1f}")
            partes.append("M" + "L".join(pts) + "Z")
    return "".join(partes)


def choropleth_html(
    frame: pd.DataFrame,
    geo: gpd.GeoDataFrame,
    ordem: list[str],
    cores: dict[str, str],
    legenda: str,
) -> tuple[str, float]:
    dados = geo[["cd_mun", "municipio_norm", "geometry"]].merge(
        frame[["cd_mun", "nome", "bolsas", "pct_txt", "grupo", "classe"]], on="cd_mun"
    )
    continente = dados[dados["municipio_norm"] != NORONHA]
    ilha = dados[dados["municipio_norm"] == NORONHA]

    minx, miny, maxx, maxy = continente.total_bounds
    x0, y1 = _proj(minx, miny)
    x1, y0 = _proj(maxx, maxy)
    dx, dy = PAD - x0, PAD - y0
    largura_mapa = x1 - x0
    largura = largura_mapa + 2 * PAD + INSET_W
    altura = (y1 - y0) + 2 * PAD

    grupos, tips, regras = [], [], []

    def adicionar(linha, d: str) -> None:
        cod = linha["cd_mun"]
        cor = cores[linha["classe"]]
        grupos.append(f'<g class="pe-mun pe-m{cod}"><path d="{d}" fill="{cor}" fill-rule="evenodd"/></g>')
        tips.append(
            f'<div class="pe-tip pe-t{cod}"><b>{escape(linha["nome"])}</b>'
            f'<span>{fmt_int(linha["bolsas"])} bolsas</span>'
            f'<span>Integrais: {escape(linha["pct_txt"])}</span>'
            f'<span class="pe-dim">{escape(linha["grupo"])}</span></div>'
        )
        regras.append(f".pe-wrap:has(.pe-m{cod}:hover) .pe-t{cod}{{display:flex}}")

    for _, linha in continente.iterrows():
        adicionar(linha, _path(linha.geometry, dx, dy))

    inset_svg = ""
    if not ilha.empty:
        linha = ilha.iloc[0]
        b = linha.geometry.bounds
        cx, cy = _proj((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        alvo_x = largura_mapa + 2 * PAD + INSET_W / 2 - 4
        alvo_y = PAD + 34
        adicionar(linha, _path(linha.geometry, alvo_x - cx, alvo_y - cy, INSET_ZOOM, (cx, cy)))
        inset_svg = (
            f'<rect x="{alvo_x - INSET_W / 2 + 4:.1f}" y="{PAD:.1f}" width="{INSET_W - 12:.1f}" height="92" '
            f'rx="6" fill="none" stroke="{GRID}" stroke-dasharray="3 3"/>'
            f'<text x="{alvo_x:.1f}" y="{PAD + 78:.1f}" text-anchor="middle" class="pe-inset">F. de Noronha</text>'
            f'<text x="{alvo_x:.1f}" y="{PAD + 88:.1f}" text-anchor="middle" class="pe-inset">(ampliada)</text>'
        )

    legenda_html = "".join(
        f'<span class="pe-key"><i style="background:{cores[c]}"></i>{escape(c)}</span>' for c in ordem
    )

    css = f"""
<style>
html, body {{ margin: 0; background: transparent; }}
.pe-wrap {{ width: 100%; font-family: 'Source Sans Pro', -apple-system, 'Segoe UI', Roboto, sans-serif; color: {TEXT}; }}
.pe-tipbar {{ min-height: 46px; display: flex; align-items: center; margin-bottom: .25rem; }}
.pe-hint {{ color: {TEXT_MUTED}; font-size: .93rem; }}
.pe-wrap:has(.pe-mun:hover) .pe-hint {{ display: none; }}
.pe-tip {{ display: none; gap: .3rem 1rem; align-items: baseline; flex-wrap: wrap; font-size: .98rem; }}
.pe-tip b {{ font-size: 1.05rem; }}
.pe-tip .pe-dim {{ color: {TEXT_MUTED}; }}
.pe-svg {{ width: 100%; height: auto; display: block; }}
.pe-mun path {{ stroke: {SURFACE}; stroke-width: .7; stroke-linejoin: round; cursor: pointer; }}
.pe-mun:hover path {{ stroke: #fff; stroke-width: 1.7; filter: brightness(1.18); }}
.pe-inset {{ fill: {TEXT_MUTED}; font-size: 10px; }}
.pe-legend {{ display: flex; flex-wrap: wrap; align-items: center; gap: .35rem 1.1rem; margin-top: .6rem; font-size: .88rem; }}
.pe-legend-title {{ color: {TEXT_MUTED}; font-weight: 600; margin-right: .2rem; }}
.pe-key {{ display: inline-flex; align-items: center; gap: .4rem; }}
.pe-key i {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
{"".join(regras)}
</style>
"""
    html = (
        css
        + '<div class="pe-wrap">'
        + '<div class="pe-tipbar"><div class="pe-hint">Passe o mouse sobre um município para ver os valores.</div>'
        + "".join(tips)
        + "</div>"
        + f'<svg class="pe-svg" viewBox="0 0 {largura:.0f} {altura:.0f}" role="img" '
        + 'aria-label="Mapa de Pernambuco com as bolsas do ProUni por município">'
        + "".join(grupos)
        + inset_svg
        + "</svg>"
        + f'<div class="pe-legend"><span class="pe-legend-title">{escape(legenda)}</span>{legenda_html}</div>'
        + "</div>"
    )
    return html, altura / largura
