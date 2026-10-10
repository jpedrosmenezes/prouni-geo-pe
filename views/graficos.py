"""Gráficos: comparação Brasil × PE, perfil dos beneficiários e ranking de municípios."""

import pandas as pd
import streamlit as st

from src.prouni.constants import (
    COLOR_MODALIDADE,
    COLOR_TIPO,
    ORDEM_FAIXA_ETARIA,
    ORDEM_RACA,
    RMR_LABEL,
)
from src.prouni.data import load_data, split_br_pe
from src.prouni.formatting import fmt_int, fmt_pct, fmt_pp
from src.prouni.geo import municipal_summary
from src.prouni.plots import CHART_CONFIG, share_comparison, stacked_by_tipo, top_municipios
from src.prouni.ui import callout, footer, page_header, section

br, pe_all = split_br_pe(load_data())


def mostrar(fig):
    st.plotly_chart(fig, width="stretch", theme=None, config=CHART_CONFIG)


def pct(serie, valor):
    s = serie.dropna()
    return (s == valor).mean() * 100 if len(s) else 0.0


page_header(
    "Análise",
    "Gráficos",
    "Como as bolsas se distribuem por tipo, modalidade, perfil dos beneficiários e município.",
)


with st.sidebar:
    st.markdown("#### Filtros · Pernambuco")
    st.caption("Aplicam-se às abas **Perfil** e **Municípios**. A comparação Brasil × PE usa todos os dados.")
    f_modalidade = st.pills(
        "Modalidade",
        options=list(COLOR_MODALIDADE),
        selection_mode="multi",
        default=list(COLOR_MODALIDADE),
        key="f_modalidade",
    )
    f_tipo = st.pills(
        "Tipo de bolsa",
        options=list(COLOR_TIPO),
        selection_mode="multi",
        default=list(COLOR_TIPO),
        key="f_tipo",
    )

pe = pe_all[
    pe_all["modalidade"].isin(f_modalidade or list(COLOR_MODALIDADE))
    & pe_all["tipo"].isin(f_tipo or list(COLOR_TIPO))
]

tab_comp, tab_perfil, tab_mun = st.tabs(["Brasil × Pernambuco", "Perfil dos beneficiários", "Municípios"])


with tab_comp:
    integral_pe, integral_br = pct(pe_all["tipo"], "Integral"), pct(br["tipo"], "Integral")
    ead_pe, ead_br = pct(pe_all["modalidade"], "EAD"), pct(br["modalidade"], "EAD")

    esq, dir_ = st.columns(2, gap="large")
    with esq:
        section(
            "Tipo de bolsa",
            f"Em Pernambuco, {fmt_pct(integral_pe)} das bolsas são integrais "
            f"({fmt_pp(integral_pe - integral_br)} em relação ao Brasil).",
        )
        mostrar(share_comparison({"Brasil": br["tipo"], "Pernambuco": pe_all["tipo"]}, COLOR_TIPO))
    with dir_:
        section(
            "Modalidade de ensino",
            f"Cursos a distância somam {fmt_pct(ead_pe)} das bolsas em PE "
            f"({fmt_pp(ead_pe - ead_br)} em relação ao Brasil).",
        )
        mostrar(share_comparison({"Brasil": br["modalidade"], "Pernambuco": pe_all["modalidade"]}, COLOR_MODALIDADE))

    section("Turno do curso em Pernambuco", "Nº de bolsas por turno, separado por tipo de bolsa.")
    mostrar(stacked_by_tipo(pe_all, "turno", height=300))


with tab_perfil:
    if pe.empty:
        st.info("Nenhuma bolsa corresponde aos filtros selecionados.")
    else:
        st.caption(f"{fmt_int(len(pe))} de {fmt_int(len(pe_all))} bolsas de Pernambuco nos filtros atuais.")

        esq, dir_ = st.columns([3, 2], gap="large")
        with esq:
            top_raca = pe["raca"].value_counts(normalize=True).mul(100)
            lider = top_raca.index[0]
            section(
                "Raça/cor",
                f"Autodeclaradas {lider.lower()}s são o maior grupo ({fmt_pct(top_raca.iloc[0])}).",
            )
            mostrar(stacked_by_tipo(pe, "raca", order=ORDEM_RACA, height=330))
        with dir_:
            fem = pct(pe["sexo"], "Feminino")
            section("Sexo", f"Mulheres recebem {fmt_pct(fem)} das bolsas.")
            mostrar(stacked_by_tipo(pe, "sexo", height=330))

        esq, dir_ = st.columns([3, 2], gap="large")
        with esq:
            mediana = pe["idade"].median()
            section("Faixa etária", f"Idade mediana de {mediana:.0f} anos no ano da concessão.")
            mostrar(stacked_by_tipo(pe, "faixa_etaria", order=ORDEM_FAIXA_ETARIA, height=330, horizontal=False))
        with dir_:
            com = pe[pe["pcd"] == "Sim"]
            sem = pe[pe["pcd"] == "Não"]
            section("Deficiência física", "Beneficiários que declaram deficiência física.")
            m1, m2 = st.columns(2)
            m1.metric("Com deficiência", fmt_int(len(com)), border=True)
            m2.metric("% do total", fmt_pct(len(com) / len(pe) * 100), border=True)
            if len(com) and len(sem):
                mostrar(
                    share_comparison(
                        {"Sem deficiência": sem["tipo"], "Com deficiência": com["tipo"]},
                        COLOR_TIPO,
                        height=170,
                    )
                )
            st.caption("Recorte pequeno: leia proporções com cautela.")

        with st.expander("Ver dados em tabela"):
            tabela = (
                pd.crosstab(pe["raca"], pe["tipo"], margins=True, margins_name="Total")
                .reindex([*ORDEM_RACA, "Total"])
                .dropna(how="all")
                .fillna(0)
                .astype(int)
            )
            st.dataframe(tabela, width="stretch")


with tab_mun:
    if pe.empty:
        st.info("Nenhuma bolsa corresponde aos filtros selecionados.")
    else:
        resumo, _ = municipal_summary(pe)
        total = resumo["bolsas"].sum()
        rmr = resumo.loc[resumo["grupo"] == RMR_LABEL, "bolsas"].sum() / total * 100
        top10 = resumo.head(10)["bolsas"].sum() / total * 100
        recife = resumo.iloc[0]

        esq, dir_ = st.columns([3, 2], gap="large")
        with esq:
            section("Dez municípios com mais bolsas", "Cor indica se o município pertence à Região Metropolitana do Recife.")
            mostrar(top_municipios(resumo, 10))
        with dir_:
            section("Concentração")
            st.metric("Região Metropolitana do Recife", fmt_pct(rmr), border=True)
            st.metric(f"Só {recife['nome']}", fmt_pct(recife["bolsas"] / total * 100), border=True)
            st.metric("Dez maiores municípios", fmt_pct(top10), border=True)
            callout(
                "Contagens absolutas favorecem municípios populosos. "
                "Para ver a distribuição espacial completa, abra o <b>Mapa</b>."
            )

        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        with st.expander("Ver dados em tabela"):
            st.dataframe(
                resumo[["nome", "grupo", "bolsas", "integrais", "pct_integral"]]
                .rename(
                    columns={
                        "nome": "Município",
                        "grupo": "Grupo",
                        "bolsas": "Bolsas",
                        "integrais": "Integrais",
                        "pct_integral": "% integrais",
                    }
                )
                .head(25),
                hide_index=True,
                width="stretch",
                column_config={"% integrais": st.column_config.NumberColumn(format="%.1f%%")},
            )
            st.caption("25 municípios com mais bolsas. A lista completa está na página Mapa.")

footer()
