"""Leitura e limpeza dos microdados do ProUni (dados abertos do MEC)."""

from __future__ import annotations

import unicodedata

import pandas as pd
import streamlit as st

from .constants import (
    ALIASES_MUNICIPIOS,
    ANO,
    CSV_PATH,
    FAIXA_ETARIA_BINS,
    ORDEM_FAIXA_ETARIA,
    UF,
)

COLUNAS = {
    "TIPO_BOLSA": "tipo",
    "MODALIDADE_ENSINO_BOLSA": "modalidade",
    "NOME_TURNO_CURSO_BOLSA": "turno",
    "SEXO_BENEFICIARIO": "sexo",
    "RACA_BENEFICIARIO": "raca",
    "DATA_NASCIMENTO": "nascimento",
    "BENEFICIARIO_DEFICIENTE_FISICO": "pcd",
    "UF_BENEFICIARIO": "uf",
    "MUNICIPIO_BENEFICIARIO": "municipio",
}


def normalize_name(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.upper().split())


def canonical_municipio(value: str) -> str:
    norm = normalize_name(value)
    return ALIASES_MUNICIPIOS.get(norm, norm)


def clean_microdata(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    df["raca"] = df["raca"].replace({"Ind¡gena": "Indígena", "Não Informada": "Não informada"})
    df["tipo"] = df["tipo"].str.strip().str.capitalize()
    df["modalidade"] = df["modalidade"].str.strip().replace({"PRESENCIAL": "Presencial"})
    df["turno"] = df["turno"].str.strip().str.capitalize()
    df["sexo"] = df["sexo"].map({"F": "Feminino", "M": "Masculino"})
    df["pcd"] = df["pcd"].map({"S": "Sim", "N": "Não"})

    nascimento = pd.to_datetime(df["nascimento"], format="%d/%m/%Y", errors="coerce")
    idade = ANO - nascimento.dt.year
    df["idade"] = idade.where(idade.between(14, 90))
    df["faixa_etaria"] = pd.cut(
        df["idade"], bins=FAIXA_ETARIA_BINS, labels=ORDEM_FAIXA_ETARIA, include_lowest=True
    )

    unicos = df["municipio"].dropna().unique()
    chave = {nome: canonical_municipio(nome) for nome in unicos}
    df["municipio_norm"] = df["municipio"].map(chave)

    for col in ("tipo", "modalidade", "turno", "sexo", "raca", "pcd", "uf"):
        df[col] = df[col].astype("category")

    return df.drop(columns=["nascimento"])


@st.cache_data(show_spinner="Carregando microdados do ProUni…")
def load_data() -> pd.DataFrame:
    raw = pd.read_csv(
        CSV_PATH,
        sep=";",
        encoding="latin1",
        usecols=list(COLUNAS),
        dtype=str,
    ).rename(columns=COLUNAS)
    return clean_microdata(raw)


def split_br_pe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return df, df[df["uf"] == UF]
