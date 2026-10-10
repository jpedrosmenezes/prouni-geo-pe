"""Visão geral: indicadores principais, achados calculados e guia de navegação."""

import streamlit as st

from src.prouni.constants import ANO, IBGE_URL, MEC_URL, RMR_LABEL
from src.prouni.data import load_data, split_br_pe
from src.prouni.formatting import fmt_int, fmt_pct, fmt_pp
from src.prouni.geo import municipal_summary
from src.prouni.ui import card, footer, hero, section

br, pe = split_br_pe(load_data())
resumo, nao_casados = municipal_summary(pe)


def pct(serie, valor):
    s = serie.dropna()
    return (s == valor).mean() * 100


integral_pe, integral_br = pct(pe["tipo"], "Integral"), pct(br["tipo"], "Integral")
mulheres_pe, mulheres_br = pct(pe["sexo"], "Feminino"), pct(br["sexo"], "Feminino")
ead_pe, ead_br = pct(pe["modalidade"], "EAD"), pct(br["modalidade"], "EAD")
com_bolsa = int((resumo["bolsas"] > 0).sum())

hero(
    f"Dados abertos do MEC · {ANO}",
    "Bolsas do ProUni em Pernambuco",
    "Quem recebeu, onde mora e como as bolsas se distribuem pelo estado. "
    "Uma análise exploratória dos dados abertos do programa, com comparação nacional e mapa por município.",
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(
    "Bolsas em PE",
    fmt_int(len(pe)),
    delta=f"{fmt_pct(len(pe) / len(br) * 100)} do Brasil",
    delta_color="off",
    delta_arrow="off",
    border=True,
)
c2.metric(
    "Bolsas integrais",
    fmt_pct(integral_pe),
    delta=f"{fmt_pp(integral_pe - integral_br)} vs. Brasil",
    delta_color="off",
    delta_arrow="off",
    border=True,
)
c3.metric(
    "Beneficiárias mulheres",
    fmt_pct(mulheres_pe),
    delta=f"{fmt_pp(mulheres_pe - mulheres_br)} vs. Brasil",
    delta_color="off",
    delta_arrow="off",
    border=True,
)
c4.metric(
    "Cursos a distância",
    fmt_pct(ead_pe),
    delta=f"{fmt_pp(ead_pe - ead_br)} vs. Brasil",
    delta_color="off",
    delta_arrow="off",
    border=True,
)
c5.metric(
    "Municípios com bolsas",
    str(com_bolsa),
    delta=f"de {len(resumo)} no estado",
    delta_color="off",
    delta_arrow="off",
    border=True,
)


raca = pe["raca"].dropna().value_counts(normalize=True).mul(100)
top_raca = [f"<b>{fmt_pct(v)}</b> {nome.lower()}s" for nome, v in raca.head(3).items()]
idade_mediana = pe["idade"].median()
ate_24 = (pe["idade"].dropna() <= 24).mean() * 100

rmr = resumo[resumo["grupo"] == RMR_LABEL]
recife = resumo.iloc[0]
fora = resumo[resumo["grupo"] != RMR_LABEL].head(2)

section("O que os dados mostram")
a, b, c = st.columns(3)
with a:
    card(
        "Perfil dos beneficiários",
        f"Entre os beneficiários, {', '.join(top_raca[:-1])} e {top_raca[-1]}. "
        f"A idade mediana é de <b>{idade_mediana:.0f} anos</b> e <b>{fmt_pct(ate_24, 0)}</b> têm até 24 anos.",
    )
with b:
    card(
        "Tipo e modalidade",
        f"<b>{fmt_pct(integral_pe)}</b> das bolsas são integrais, contra {fmt_pct(integral_br)} no Brasil. "
        f"Os cursos a distância respondem por <b>{fmt_pct(ead_pe)}</b> das bolsas no estado "
        f"({fmt_pct(ead_br)} no país).",
    )
with c:
    card(
        "Geografia",
        f"A Região Metropolitana do Recife reúne <b>{fmt_pct(rmr['bolsas'].sum() / len(pe) * 100)}</b> das bolsas "
        f"e só {recife['nome']} tem <b>{fmt_pct(recife['bolsas'] / len(pe) * 100)}</b>. "
        f"Fora da RMR, lideram {fora.iloc[0]['nome']} e {fora.iloc[1]['nome']}.",
    )


section("Explore a análise")
n1, n2 = st.columns(2)
with n1:
    with st.container(border=True):
        st.markdown("**:material/bar_chart: Gráficos**")
        st.caption(
            "Comparação Brasil × Pernambuco, perfil por raça/cor, sexo, faixa etária e deficiência, "
            "e ranking de municípios. Com filtros por modalidade e tipo de bolsa."
        )
        st.page_link("views/graficos.py", label="Abrir gráficos", icon=":material/arrow_forward:")
with n2:
    with st.container(border=True):
        st.markdown("**:material/map: Mapa**")
        st.caption(
            "Mapa interativo dos 185 municípios, por número de bolsas ou por proporção de bolsas "
            "integrais, com ranking pesquisável ao lado."
        )
        st.page_link("views/mapa.py", label="Abrir mapa", icon=":material/arrow_forward:")


section("Dados e método")
with st.expander("Fontes, tratamento e limitações"):
    st.markdown(
        f"""
**Fontes**

- Bolsas concedidas pelo ProUni em {ANO}: [dados abertos do MEC]({MEC_URL}).
- Malha municipal de Pernambuco (2025): [IBGE]({IBGE_URL}).

**Tratamento**

- Os microdados cobrem {fmt_int(len(br))} bolsas no país; {fmt_int(len(pe))} são de beneficiários residentes em Pernambuco.
- O CPF (mascarado na fonte) não é carregado.
- O arquivo mistura codificações de texto; os rótulos foram corrigidos (por exemplo, "Indígena").
- Nomes de municípios são normalizados (sem acento, caixa alta) e quatro grafias divergentes entre MEC e IBGE
  são reconciliadas (Iguaraci → Iguaracy, Itamaracá → Ilha de Itamaracá, Belém de São Francisco → Belém do São Francisco,
  Lagoa do Itaenga → Lagoa de Itaenga).
  {"Todas as bolsas foram associadas a um município da malha." if not nao_casados else "Sem correspondência na malha: " + ", ".join(nao_casados) + "."}
- A idade é aproximada (ano de {ANO} menos ano de nascimento); datas implausíveis são descartadas.

**Limitações**

- Os dados trazem apenas **bolsas concedidas**, sem candidatos ou elegíveis. Não permitem concluir sobre acesso ou equidade do programa.
- O município é o de **residência do beneficiário**, não o da instituição de ensino.
- Contagens são absolutas e refletem, em parte, o tamanho da população de cada município.
- A variável de deficiência refere-se apenas a **deficiência física**.
"""
    )

footer()
