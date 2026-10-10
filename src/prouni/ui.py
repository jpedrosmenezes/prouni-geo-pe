"""Componentes de interface compartilhados: CSS, cabeçalhos, destaques e rodapé."""

from __future__ import annotations

import streamlit as st

from .constants import (
    ACCENT,
    AUTHOR,
    GRID,
    PANEL,
    PROFILE_URL,
    REPO_URL,
    TEXT,
    TEXT_MUTED,
)

_CSS = f"""
<style>
.block-container {{ padding-top: 2.4rem; padding-bottom: 3rem; max-width: 1180px; }}
header[data-testid="stHeader"] {{ background: transparent; }}
footer {{ visibility: hidden; }}

.eyebrow {{
    color: {ACCENT}; font-size: .78rem; font-weight: 600;
    letter-spacing: .12em; text-transform: uppercase; margin: 0 0 .35rem 0;
}}
.hero-title {{
    font-size: 2.7rem; font-weight: 700; line-height: 1.08;
    letter-spacing: -0.02em; margin: 0 0 .7rem 0; color: {TEXT};
}}
.hero-sub {{
    color: {TEXT_MUTED}; font-size: 1.1rem; line-height: 1.55;
    max-width: 44rem; margin: 0 0 1.6rem 0;
}}
.page-title {{
    font-size: 2rem; font-weight: 700; letter-spacing: -0.015em;
    margin: 0 0 .4rem 0; color: {TEXT};
}}
.page-sub {{ color: {TEXT_MUTED}; font-size: 1.02rem; max-width: 46rem; margin: 0 0 1.2rem 0; }}

.section-title {{
    font-size: 1.15rem; font-weight: 600; margin: 1.4rem 0 .15rem 0; color: {TEXT};
}}
.section-caption {{ color: {TEXT_MUTED}; font-size: .93rem; margin: 0 0 .5rem 0; }}

.callout {{
    border-left: 3px solid {ACCENT}; background: {PANEL}; color: {TEXT};
    padding: .75rem 1rem; border-radius: 0 10px 10px 0; font-size: .96rem; line-height: 1.5;
}}
.callout b {{ color: #fff; }}

.card-title {{ font-weight: 600; font-size: 1rem; margin-bottom: .3rem; color: {TEXT}; }}
.card-body {{ color: {TEXT_MUTED}; font-size: .93rem; line-height: 1.5; }}
.card-body b {{ color: {TEXT}; font-weight: 600; }}

.site-footer {{
    margin-top: 3rem; padding-top: 1rem; border-top: 1px solid {GRID};
    color: {TEXT_MUTED}; font-size: .85rem;
}}
.site-footer a {{ color: {TEXT_MUTED}; text-decoration: underline; }}

[data-testid="stMetricValue"] {{ font-weight: 650; letter-spacing: -0.01em; }}
[data-testid="stTabs"] button[role="tab"] {{ font-size: .98rem; }}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<p class="eyebrow">{eyebrow}</p>'
        f'<h1 class="hero-title">{title}</h1>'
        f'<p class="hero-sub">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<p class="eyebrow">{eyebrow}</p>'
        f'<h1 class="page-title">{title}</h1>'
        f'<p class="page-sub">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def section(title: str, caption: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)


def callout(html: str) -> None:
    st.markdown(f'<div class="callout">{html}</div>', unsafe_allow_html=True)


def card(title: str, body_html: str) -> None:
    with st.container(border=True, height=150):
        st.markdown(
            f'<div class="card-title">{title}</div><div class="card-body">{body_html}</div>',
            unsafe_allow_html=True,
        )


def footer() -> None:
    st.markdown(
        f'<div class="site-footer">Análise exploratória de dados abertos do MEC e da malha municipal do IBGE. '
        f'Desenvolvido por <a href="{PROFILE_URL}" target="_blank">{AUTHOR}</a> · '
        f'<a href="{REPO_URL}" target="_blank">Código no GitHub</a></div>',
        unsafe_allow_html=True,
    )


def sidebar_footer() -> None:
    with st.sidebar:
        st.caption(f"[Código no GitHub]({REPO_URL})  \nDados: MEC (ProUni 2020) e IBGE")


def embed_html(html: str, height: int) -> None:
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        import streamlit.components.v1 as components

        components.html(html, height=height, scrolling=False)
