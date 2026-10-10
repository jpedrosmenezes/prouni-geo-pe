import pytest

from src.prouni.data import canonical_municipio, load_data, normalize_name, split_br_pe
from src.prouni.geo import municipal_summary, quantile_classes


def test_normalize_name_remove_acentos_e_espacos():
    assert normalize_name(" Ilha de  Itamaracá ") == "ILHA DE ITAMARACA"


@pytest.mark.parametrize(
    "mec, ibge",
    [
        ("IGUARACI", "IGUARACY"),
        ("ITAMARACA", "ILHA DE ITAMARACA"),
        ("LAGOA DO ITAENGA", "LAGOA DE ITAENGA"),
        ("BELEM DE SAO FRANCISCO", "BELEM DO SAO FRANCISCO"),
    ],
)
def test_aliases_de_municipios(mec, ibge):
    assert canonical_municipio(mec) == ibge


@pytest.fixture(scope="module")
def pe():
    return split_br_pe(load_data())[1]


def test_rotulos_corrigidos(pe):
    assert "Indígena" in set(pe["raca"].dropna())
    assert not any("¡" in str(x) for x in pe["raca"].dropna().unique())


def test_cpf_nao_e_carregado():
    assert "CPF_BENEFICIARIO" not in load_data().columns


def test_todas_as_bolsas_casam_com_a_malha(pe):
    resumo, nao_casados = municipal_summary(pe)
    assert nao_casados == []
    assert resumo["bolsas"].sum() == len(pe)
    assert len(resumo) == 185


def test_quantile_classes_cobre_todos_os_valores():
    import pandas as pd

    valores = pd.Series([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
    classes = quantile_classes(valores)
    assert classes.notna().all()
