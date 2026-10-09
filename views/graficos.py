import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.sidebar.markdown("# Gráficos 📊")

st.title("# OS GRÁFICOS")

df_geral = pd.read_csv("data/ProuniRelatorioDadosAbertos2020.csv", sep=';', encoding="latin1")
df_pe = df_geral[df_geral["UF_BENEFICIARIO"] == 'PE']

#display(df_pe.shape)
#display(df_pe.info())
#display(df_pe.isna().sum())

colunas = [#"NOME_IES_BOLSA",
           "TIPO_BOLSA",
           "MODALIDADE_ENSINO_BOLSA",
           #"NOME_CURSO_BOLSA",
           "NOME_TURNO_CURSO_BOLSA",
           #"CPF_BENEFICIARIO",
           "SEXO_BENEFICIARIO",
           "RACA_BENEFICIARIO",
           "DATA_NASCIMENTO",
           "BENEFICIARIO_DEFICIENTE_FISICO",
           "MUNICIPIO_BENEFICIARIO"]

df_pe = df_pe.dropna(subset=colunas)

df_pe_analisado = df_pe[colunas]
df_pe_analisado["DATA_NASCIMENTO"] = pd.to_datetime(df_pe_analisado["DATA_NASCIMENTO"], format="%d/%m/%Y")
df_pe_analisado = df_pe_analisado.sort_values(by = "DATA_NASCIMENTO")
df_pe_analisado = df_pe_analisado.reset_index(drop=True)

series_pe_municipios = df_pe_analisado["MUNICIPIO_BENEFICIARIO"].value_counts()
df_pe_municipios = series_pe_municipios.reset_index()
df_pe_municipios.columns = ["MUNICIPIOS", "TOTAL"]

st.subheader("DISTRIBUIÇÃO DE BOLSAS NACIONAL E ESTADUAL:")
st.write("""
Os gráficos de pizza revelam a distribuição de bolsas nos âmbitos **nacional** e **estadual**.
É possível perceber uma paridade entre ambos,
evidenciando que a distribuição de bolsas no estado reflete o cenário do Brasil.
""")

#distribuição de bolsas no Brasil e no estado de Pernambuco
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

df_geral["TIPO_BOLSA"].value_counts().plot.pie(
    autopct="%1.1f%%",
    ax = ax1
)
ax1.set_title("DISTRIBUIÇÃO NACIONAL DE BOLSAS", fontsize=13)

df_pe_analisado["TIPO_BOLSA"].value_counts().plot.pie(
    autopct="%1.1f%%",
    ax = ax2
)
ax2.set_title("DISTRIBUIÇÃO DE BOLSAS NO ESTADO DE PERNAMBUCO", fontsize=13)

st.pyplot(fig)

st.subheader("DISTRIBUIÇÃO POR PERFIL ÉTNICO-RACIAL EM PERNAMBUCO:")
st.write("""
A análise revela uma predominância de beneficiários que se autodeclaram **pardos**, seguidos por **brancos** e **pretos**. 
Em todos os grupos, observa-se que as **bolsas integrais** representam a grande maioria das concessões em Pernambuco.
Esse cenário demonstra uma paridade com os indicadores nacionais, mantendo a consistência do perfil demográfico atendido pelo programa.
""")

#distribuição de bolsas por perfil étnico-racial em Pernambuco
fig, ax = plt.subplots(figsize=(12, 5))

df_pe_analisado["RACA_BENEFICIARIO"] = df_pe_analisado["RACA_BENEFICIARIO"].replace('Ind¡gena', 'Indígena')
ordem_perfis = ["Parda", "Branca", "Preta", "Amarela", "Indígena"]

sns.countplot(
    data=df_pe_analisado,
    x="RACA_BENEFICIARIO",
    hue="TIPO_BOLSA",
    order=ordem_perfis,
    ax=ax
)
ax.set_title("DISTRIBUIÇÃO POR PERFIL ÉTNICO-RACIAL")
ax.set_xlabel("PERFIL ÉTNICO-RACIAL DO BENEFICIÁRIO")
ax.set_ylabel("QUANTIDADE DE BOLSAS")
ax.legend(title="TIPO DE BOLSA")

st.pyplot(fig)

st.subheader("DISTRIBUIÇÃO DE BOLSAS POR SEXO EM PERNAMBUCO:")
st.write("""
A análise demográfica revela que as **mulheres** detêm a maior parcela dos benefícios concedidos no estado. 
Nota-se que a modalidade **integral** é a grande protagonista em ambos os grupos, indicando que a maioria dos estudantes atendidos em Pernambuco conta com a isenção total das mensalidades, independentemente do gênero.
""")

#distribuição de bolsas por sexo do beneficiário em Pernambuco
fig, ax = plt.subplots(figsize=(12, 5))

sns.countplot (
    data = df_pe_analisado,
    x = "SEXO_BENEFICIARIO",
    hue = "TIPO_BOLSA",
    ax = ax
)
ax.set_title("DISTRIBUIÇÃO DE BOLSAS POR SEXO")
ax.set_xlabel("SEXO DO BENEFICIÁRIO")
ax.set_ylabel("QUANTIDADE DE BOLSAS")
ax.legend(title="TIPO DE BOLSA")

st.pyplot(fig)

st.subheader("DISTRIBUIÇÃO DE BOLSAS PARA DEFICIÊNTES FÍSICOS:")
st.write("""
Este recorte quantifica a presença de beneficiários com deficiência física no programa. 
Embora o volume total de bolsas concentre-se em pessoas sem deficiência, o monitoramento desses dados é essencial para medir o alcance das políticas de **inclusão educacional**.
Observa-se que, mesmo no grupo PCD, a oferta de **bolsas integrais** permanece como o principal modelo de auxílio oferecido no estado.
""")

#distribuição de bolsas para deficiêntes físicos em Pernambuco
fig, ax = plt.subplots(figsize=(12, 5))

sns.countplot(
    data = df_pe_analisado,
    x = "BENEFICIARIO_DEFICIENTE_FISICO",
    hue = "TIPO_BOLSA",
    ax=ax
)
ax.set_title("DISTRIBUIÇÃO DE BOLSAS ENTRE PESSOAS COM E SEM DEFICIÊNCIA FÍSICA")
ax.set_xlabel("BENEFICIÁRIO DEFICIÊNTE FÍSICO")
ax.set_ylabel("QUANTIDADE DE BOLSAS")
ax.legend(title="TIPO DE BOLSA")

st.pyplot(fig)

st.subheader("DISTRIBUIÇÃO DE BOLSAS NACIONAL E ESTADUAL:")
st.write("""
A análise regional destaca uma forte **centralização na Região Metropolitana do Recife**, que abriga a maioria das cidades com maior volume de beneficiários. 
Entre as exceções fora do eixo metropolitano, destacam-se polos regionais como **Caruaru, Petrolina e Bonito**, que exercem papel fundamental na interiorização do acesso ao ensino superior.
Esse cenário evidencia como as bolsas estão distribuídas entre os principais centros urbanos e de desenvolvimento do estado.
""")

#distribuição de bolsas entre os top 10 municípios de Pernambuco
df_pe_top_municipios = df_pe_municipios.head(10)

regiao_metropolitana = ["RECIFE",
                        "JABOATAO DOS GUARARAPES",
                        "OLINDA",
                        "PAULISTA",
                        "CABO DE SANTO AGOSTINHO",
                        "CAMARAGIBE",
                        "IGARASSU",
                        "SAO LOURENCO DA MATA",
                        "ABREU E LIMA",
                        "IPOJUCA",
                        "MORENO",
                        "ITAPISSUMA",
                        "ARAÇOIABA",
                        "ILHA DE ITAMARACA"]

df_pe_top_municipios["REGIÃO METROPOLITANA"] = np.where(df_pe_top_municipios["MUNICIPIOS"].isin(regiao_metropolitana), "SIM", "NÃO")

fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(
    data = df_pe_top_municipios,
    x = "MUNICIPIOS",
    y = "TOTAL",
    hue = "REGIÃO METROPOLITANA",
    ax = ax
)
ax.set_title("TOP 10 MUNICÍPIOS COM MAIS BENEFICIÁRIOS")
ax.set_xlabel("MUNICÍPIOS DE BENEFICIÁRIOS")
ax.tick_params(axis='x', rotation=90)
ax.set_ylabel("QUANTIDADE DE BOLSAS")

st.pyplot(fig)

st.write("""
---
""")
st.subheader("(TESTE) HEATMAP DA DISTRIBUIÇÃO DE BOLSAS POR PERFIL ÉTNICO-RACIAL")
st.write("""
Este mapa de calor cruza o perfil étnico-racial com a modalidade da bolsa, permitindo visualizar a **densidade de beneficiários** em cada categoria. 
A intensidade do vermelho confirma que a maior concentração de estudantes em Pernambuco está no grupo de **bolsistas integrais que se autodeclaram pardos**.
""")

#(teste) heatmap da distribuição de bolsas por perfil étnico-racial em Pernambuco
tabela = pd.crosstab(
    df_pe_analisado["RACA_BENEFICIARIO"],
    df_pe_analisado["TIPO_BOLSA"]
)

tabela = tabela.reindex(ordem_perfis)

fig, ax = plt.subplots(figsize=(12, 5))

sns.heatmap(
    tabela,
    annot=True,
    fmt="d",
    cmap="Reds",
    ax=ax
)
ax.set_title("DISTRIBUIÇÃO DE BOLSAS POR RAÇA")
ax.set_xlabel("TIPO DE BOLSA")
ax.set_ylabel("QUANTIDADE DE BOLSAS POR RAÇA")
ax.tick_params(axis='y', rotation=0)

st.pyplot(fig)
