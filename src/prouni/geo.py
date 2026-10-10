"""Malha municipal (IBGE), resumo por município e classificação em quantis para o mapa."""

from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd
import streamlit as st

from .constants import (
    COLOR_SEM_DADO,
    OUTRAS_LABEL,
    RAMP,
    REGIAO_METROPOLITANA,
    RMR_LABEL,
    SHP_PATH,
)
from .data import normalize_name

SEM_BOLSAS = "Sem bolsas"


@st.cache_data(show_spinner="Carregando malha municipal…")
def load_geometries() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(SHP_PATH).to_crs(epsg=4326)
    gdf["geometry"] = gdf.geometry.simplify(0.002, preserve_topology=True)
    gdf["cd_mun"] = gdf["CD_MUN"].astype(str)
    gdf["municipio_norm"] = gdf["NM_MUN"].map(normalize_name)
    gdf = gdf.rename(columns={"NM_MUN": "nome", "AREA_KM2": "area_km2", "NM_RGINT": "regiao_intermediaria"})
    return gdf[["cd_mun", "nome", "municipio_norm", "area_km2", "regiao_intermediaria", "geometry"]]


def attributes() -> pd.DataFrame:
    return pd.DataFrame(load_geometries().drop(columns="geometry"))


def municipal_summary(pe: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    attrs = attributes()

    flag = (pe["tipo"] == "Integral").rename("integral")
    agg = (
        flag.groupby(pe["municipio_norm"])
        .agg(bolsas="size", integrais="sum")
        .reset_index()
    )
    nao_casados = sorted(set(agg["municipio_norm"]) - set(attrs["municipio_norm"]))

    out = attrs.merge(agg, on="municipio_norm", how="left")
    out[["bolsas", "integrais"]] = out[["bolsas", "integrais"]].fillna(0).astype(int)
    out["pct_integral"] = (out["integrais"] / out["bolsas"] * 100).where(out["bolsas"] > 0)
    out["grupo"] = np.where(
        out["municipio_norm"].isin(REGIAO_METROPOLITANA), RMR_LABEL, OUTRAS_LABEL
    )
    return out.sort_values("bolsas", ascending=False).reset_index(drop=True), nao_casados


def quantile_classes(values: pd.Series, k: int = 5, integer: bool = True, suffix: str = "") -> pd.Series:
    edges = np.quantile(values, np.linspace(0, 1, k + 1))
    if integer:
        edges = np.ceil(edges)
    else:
        edges = np.round(edges, 0)
        edges[0], edges[-1] = np.floor(values.min()), np.ceil(values.max())
    edges = np.unique(edges)
    if len(edges) < 2:
        edges = np.array([edges[0], edges[0] + 1])

    labels = []
    for i in range(len(edges) - 1):
        lo = edges[i] + 1 if (integer and i > 0) else edges[i]
        hi = edges[i + 1]
        labels.append(f"{lo:.0f}{suffix}" if lo >= hi else f"{lo:.0f}–{hi:.0f}{suffix}")
    return pd.cut(values, bins=edges, labels=labels, include_lowest=True, ordered=True)


def map_frame(
    summary: pd.DataFrame, metric: str, min_bolsas: int = 10
) -> tuple[pd.DataFrame, list[str], dict[str, str], str]:
    df = summary.copy()
    if metric == "total":
        com_dado = df["bolsas"] > 0
        sem_dado_label = SEM_BOLSAS
        classes = quantile_classes(df.loc[com_dado, "bolsas"], integer=True)
        legenda = "Nº de bolsas"
    else:
        com_dado = df["bolsas"] >= min_bolsas
        sem_dado_label = f"Menos de {min_bolsas} bolsas"
        classes = quantile_classes(
            df.loc[com_dado, "pct_integral"], integer=False, suffix="%"
        )
        legenda = "% de bolsas integrais"

    df["classe"] = sem_dado_label
    df.loc[com_dado, "classe"] = classes.astype(str)
    df["classe"] = df["classe"].where(df["classe"].isin(set(map(str, classes.cat.categories))), sem_dado_label)

    ordem_dados = [str(c) for c in classes.cat.categories if (df["classe"] == str(c)).any()]
    idx = np.linspace(0, len(RAMP) - 1, len(ordem_dados)).round().astype(int)
    cores = {rotulo: RAMP[i] for rotulo, i in zip(ordem_dados, idx, strict=True)}
    cores[sem_dado_label] = COLOR_SEM_DADO
    ordem = [sem_dado_label, *ordem_dados]

    df["pct_txt"] = df["pct_integral"].map(
        lambda v: "—" if pd.isna(v) else f"{v:.1f}".replace(".", ",") + "%"
    )
    return df, ordem, cores, legenda
