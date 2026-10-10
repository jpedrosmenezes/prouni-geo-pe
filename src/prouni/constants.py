"""Caminhos, paleta, ordens de categorias e listas de referência."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "raw" / "ProuniRelatorioDadosAbertos2020.csv"
SHP_PATH = ROOT / "data" / "raw" / "mapa" / "PE_Municipios_2025.shp"

ANO = 2020
UF = "PE"

APP_TITLE = "ProUni em Pernambuco · 2020"
REPO_URL = "https://github.com/jpedrosmenezes/prouni-geo-pe"
PROFILE_URL = "https://github.com/jpedrosmenezes"
AUTHOR = "João Pedro S. Menezes"
MEC_URL = "https://dadosabertos.mec.gov.br/prouni"
IBGE_URL = "https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais"

SURFACE = "#0f1419"     # fundo da página
PANEL = "#171e26"       # cartões e tooltips
GRID = "#26303b"        # grades e eixos (recessivos)
TEXT = "#e8ecf1"        # texto primário
TEXT_MUTED = "#9aa7b5"  # texto secundário
INK = "#0b0f14"         # texto sobre marcas coloridas
ACCENT = "#3987e5"

COLOR_TIPO = {"Integral": "#3987e5", "Parcial": "#d95926"}
COLOR_MODALIDADE = {"Presencial": "#9085e9", "EAD": "#199e70"}
RMR_LABEL = "Região Metropolitana do Recife"
OUTRAS_LABEL = "Demais municípios"
COLOR_GRUPO = {RMR_LABEL: "#d55181", OUTRAS_LABEL: "#8b95a5"}

RAMP = ["#104281", "#1c5cab", "#3987e5", "#86b6ef", "#cde2fb"]
COLOR_SEM_DADO = "#262f3a"

ORDEM_RACA = ["Parda", "Branca", "Preta", "Amarela", "Indígena", "Não informada"]
ORDEM_FAIXA_ETARIA = ["Até 19", "20–24", "25–29", "30–39", "40+"]
FAIXA_ETARIA_BINS = [0, 19, 24, 29, 39, 200]

ALIASES_MUNICIPIOS = {
    "BELEM DE SAO FRANCISCO": "BELEM DO SAO FRANCISCO",
    "IGUARACI": "IGUARACY",
    "ITAMARACA": "ILHA DE ITAMARACA",
    "LAGOA DO ITAENGA": "LAGOA DE ITAENGA",
}

REGIAO_METROPOLITANA = frozenset(
    {
        "RECIFE",
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
        "ARACOIABA",
        "ILHA DE ITAMARACA",
        "GOIANA",
    }
)
