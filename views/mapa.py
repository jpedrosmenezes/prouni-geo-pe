import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from graphs_page import df_pe_municipios

st.sidebar.markdown("# Mapa 🧭")

st.title("# O MAPA")
st.write("""
Utilizando **GeoPandas**, mapeei a distribuição de bolsas por municípios pernambucanos através de uma classificação por **quantis**. 
O mapa revela uma **acentuada mancha de concentração na Região Metropolitana do Recife (RMR)**, indicando que a oferta de bolsas está fortemente centralizada no litoral e zona da mata. Ao mesmo tempo, é possível identificar polos isolados no interior, fornecendo um panorama sobre o alcance geográfico do programa no estado.
""")

@st.cache_data
def mapa_analise_e_grafico():
    mapa_pe = gpd.read_file("mapa/PE_Municipios_2025.shp")

    mapa_pe["municipio_norm"] = (
        mapa_pe["NM_MUN"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.upper()
        .str.strip()
    )
    df_pe_municipios["municipio_norm"] = (
        df_pe_municipios["MUNICIPIOS"]
        .str.strip()
    )

    mapa_dados = mapa_pe.merge(
        df_pe_municipios,
        how="left",
        on="municipio_norm"
    )
    mapa_dados["TOTAL"] = mapa_dados["TOTAL"].fillna(0)

    fig, ax = plt.subplots(figsize=(12, 8))

    mapa_dados.plot(
        column="TOTAL",
        cmap="Reds",
        edgecolor="black",
        linewidth=0.3,
        ax=ax
    )

    vmin=mapa_dados["TOTAL"].min()
    vmax=mapa_dados["TOTAL"].max()
    norm = plt.Normalize(vmin = vmin, vmax = vmax)

    sm = plt.cm.ScalarMappable(cmap="Reds", norm=norm)

    cbar = fig.colorbar(sm, ax=ax, shrink=0.5)
    cbar.set_label("NÚMERO DE BOLSAS", fontsize=12)

    ax.axis("off")
    ax.set_title("DISTRIBUIÇÃO DE BOLSAS EM PERNAMBUCO", fontsize=15)

    return fig

st.pyplot(mapa_analise_e_grafico())