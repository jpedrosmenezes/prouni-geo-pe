"""Teste de fumaça: cada página executa sem exceções, inclusive com interações."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app():
    return AppTest.from_file(APP, default_timeout=120).run()


def test_paginas_sem_excecoes():
    at = _app()
    assert not at.exception
    for pagina in ("views/graficos.py", "views/mapa.py", "views/home.py"):
        at.switch_page(pagina).run()
        assert not at.exception, pagina


def test_mapa_indicador_alternativo():
    at = _app().switch_page("views/mapa.py").run()
    at.session_state["indicador_mapa"] = "% de bolsas integrais"
    at.run()
    assert not at.exception


def test_graficos_com_filtros_extremos():
    at = _app().switch_page("views/graficos.py").run()
    at.session_state["f_modalidade"] = ["EAD"]
    at.session_state["f_tipo"] = ["Parcial"]
    at.run()
    assert not at.exception
