import streamlit as st

st.set_page_config(layout="wide")

home_page = st.Page("views/home.py", title="Home", icon="🏠")
graphs_page = st.Page("views/graficos.py", title="Gráficos", icon="📊")
map_page = st.Page("views/mapa.py", title="Mapa", icon="🧭")

pg = st.navigation([home_page, graphs_page, map_page])

pg.run()
