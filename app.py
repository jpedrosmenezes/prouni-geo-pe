"""Ponto de entrada do app: configuração da página, tema e navegação."""

import streamlit as st

from src.prouni.constants import APP_TITLE
from src.prouni.ui import inject_css, sidebar_footer

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

pages = [
    st.Page("views/home.py", title="Visão geral", icon=":material/home:", default=True),
    st.Page("views/graficos.py", title="Gráficos", icon=":material/bar_chart:"),
    st.Page("views/mapa.py", title="Mapa", icon=":material/map:"),
]

pg = st.navigation(pages)
pg.run()
sidebar_footer()
