"""Mapa: distribuição de bolsas por município, com indicador selecionável e ranking."""

import streamlit as st

from src.prouni.constants import RMR_LABEL
from src.prouni.data import load_data, split_br_pe
from src.prouni.formatting import fmt_int, fmt_pct
from src.prouni.geo import load_geometries, map_frame, municipal_summary
from src.prouni.svgmap import choropleth_html
from src.prouni.ui import callout, embed_html, footer, page_header

_, pe = split_br_pe(load_data())
resumo, nao_casados = municipal_summary(pe)
geo = load_geometries()

page_header(
    "Geografia",
    "Mapa de bolsas por município",
    "Município de residência dos beneficiários, agrupado em classes de mesmo tamanho (quantis). "
    "Passe o mouse sobre um município para ver os valores.",
)

if nao_casados:
    st.warning("Municípios sem correspondência na malha (não aparecem no mapa): " + ", ".join(nao_casados))


ctrl1, ctrl2 = st.columns([2, 3], gap="large")
with ctrl1:
    indicador = st.segmented_control(
        "Indicador",
        options=["Total de bolsas", "% de bolsas integrais"],
        default="Total de bolsas",
        key="indicador_mapa",
    ) or "Total de bolsas"
metric = "total" if indicador == "Total de bolsas" else "pct_integral"
min_bolsas = 10
with ctrl2:
    if metric == "pct_integral":
        min_bolsas = st.slider(
            "Mínimo de bolsas por município",
            min_value=1,
            max_value=50,
            value=10,
            help="Proporções calculadas sobre poucas bolsas variam demais; municípios abaixo do mínimo ficam em cinza.",
            key="min_bolsas_mapa",
        )

# --------------------------------------------------------------------------- #
# Indicadores-resumo
# --------------------------------------------------------------------------- #
total = resumo["bolsas"].sum()
com_bolsa = int((resumo["bolsas"] > 0).sum())
rmr = resumo.loc[resumo["grupo"] == RMR_LABEL, "bolsas"].sum() / total * 100
top10 = resumo.head(10)["bolsas"].sum() / total * 100

k1, k2, k3 = st.columns(3)
k1.metric("Municípios com bolsas", f"{com_bolsa} de {len(resumo)}", border=True)
k2.metric("Região Metropolitana do Recife", fmt_pct(rmr), help="Parcela das bolsas do estado.", border=True)
k3.metric("Dez maiores municípios", fmt_pct(top10), help="Parcela das bolsas do estado.", border=True)


frame, ordem, cores, legenda = map_frame(resumo, metric, min_bolsas)

mapa_html, razao = choropleth_html(frame, geo, ordem, cores, legenda)
# Altura = faixa do tooltip + SVG na largura útil da página (~980 px) + legenda.
embed_html(mapa_html, height=int(46 + 980 * razao + 80))

col_tabela, col_info = st.columns([3, 2], gap="large")
with col_tabela:
    st.markdown("**Ranking de municípios**")
    tabela = frame[frame["bolsas"] > 0][["nome", "grupo", "bolsas", "pct_integral"]].rename(
        columns={"nome": "Município", "grupo": "Grupo", "bolsas": "Bolsas", "pct_integral": "% integrais"}
    )
    tabela["Grupo"] = tabela["Grupo"].map({RMR_LABEL: "RMR"}).fillna("Fora da RMR")
    st.dataframe(
        tabela,
        hide_index=True,
        width="stretch",
        height=420,
        column_config={
            "Bolsas": st.column_config.ProgressColumn(
                "Bolsas", format="%d", min_value=0, max_value=int(resumo["bolsas"].max())
            ),
            "% integrais": st.column_config.NumberColumn(format="%.1f%%"),
        },
    )
with col_info:
    st.markdown("**Como ler o mapa**")
    callout(
        "As cores seguem <b>quantis</b>: cada faixa reúne aproximadamente o mesmo número de municípios, "
        "o que evita que Recife esconda a variação do resto do estado. "
        "Os intervalos da legenda mudam conforme o indicador escolhido."
    )
    st.write("")
    sem = frame.loc[frame["bolsas"] == 0, "nome"].sort_values().tolist()
    if sem:
        with st.expander(f"{len(sem)} municípios sem bolsas"):
            st.write(", ".join(sem))
    st.caption(f"{fmt_int(total)} bolsas em {com_bolsa} municípios.")

footer()
