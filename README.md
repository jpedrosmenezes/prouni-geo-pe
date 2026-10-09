# Análise de Bolsas do ProUni em Pernambuco (2020)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://prouni-pe-analysis.streamlit.app/)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Dashboard interativo que analisa a distribuição de bolsas do **ProUni** em **Pernambuco** em 2020, com recortes de tipo de bolsa, raça/cor, sexo e deficiência física, além de uma visão geoespacial por município.

**Demo:** https://prouni-pe-analysis.streamlit.app/

> Apps no Streamlit Community Cloud hibernam após um tempo sem acessos. Se aparecer a tela de "wake up", basta clicar no botão e aguardar alguns segundos.

<!-- Substitua pelos seus prints/GIF, ex.: docs/img/home.png, docs/img/graficos.png, docs/img/mapa.png -->
<!-- ![Mapa de bolsas por município](docs/img/mapa.png) -->

---

## Pergunta de pesquisa

Como as bolsas do ProUni estão distribuídas em Pernambuco entre perfis de beneficiários e entre municípios, e como esse cenário se compara ao do Brasil?

## Principais achados

- **Tipo de bolsa:** a distribuição entre bolsas integrais e parciais em PE é comparável à nacional (ver gráfico na página *Gráficos*).
- **Raça/cor:** pessoas autodeclaradas pardas formam o maior grupo, seguidas por brancas e pretas.
- **Sexo:** mulheres concentram a maior parcela das bolsas.
- **Geografia:** há forte concentração na Região Metropolitana do Recife, com polos no interior (ex.: Caruaru e Petrolina).

## Funcionalidades

| Página | O que mostra |
|---|---|
| **Home** | Contexto do projeto e resumo da análise |
| **Gráficos** | Distribuição por tipo de bolsa (Brasil × PE), raça/cor, sexo, deficiência física e top 10 municípios |
| **Mapa** | Mapa coroplético de bolsas por município de residência do beneficiário |

## Dados e metodologia

**Fontes**

- **Bolsas ProUni 2020:** dados abertos do MEC (`ProuniRelatorioDadosAbertos2020.csv`). Fonte: `<link da página do conjunto de dados>`. Baixado em `AAAA-MM-DD`.
- **Malha municipal de PE:** IBGE (`PE_Municipios_2025.shp`). Fonte: `<link da página de download>`.

**Tratamento**

1. Leitura do CSV (separador `;`) e filtro por `UF_BENEFICIARIO == "PE"`.
2. Remoção de registros com valores ausentes nas colunas analisadas.
3. Padronização de rótulos (ex.: correção de encoding em "Indígena") e de nomes de municípios (sem acento, maiúsculas) para cruzar com a malha do IBGE.
4. Contagem de bolsas por município e junção (`merge`) com o shapefile.

### Limitações

- Os dados cobrem **apenas bolsas concedidas** em 2020, sem candidatos nem elegíveis. Não permitem concluir sobre acesso ou equidade do programa.
- O município é o de **residência do beneficiário**, não o da instituição de ensino.
- Contagens são absolutas e refletem, em parte, o tamanho da população de cada município. Uma versão *per capita* é um próximo passo.
- A coluna de deficiência refere-se a **deficiência física**, não a todas as pessoas com deficiência.

## Estrutura do projeto

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── app.py                  # ponto de entrada e navegação
├── views/                  # páginas do Streamlit
│   ├── home.py
│   ├── graficos.py
│   └── mapa.py
├── src/
│   └── prouni/
│       ├── __init__.py
│       ├── constants.py    # colunas, ordem de categorias, lista da RMR
│       ├── data.py         # leitura, limpeza e cache dos dados
│       ├── geo.py          # normalização de nomes e merge com a malha
│       └── plots.py        # funções que geram as figuras
├── data/
│   ├── raw/                # CSV original (ver seção Dados)
│   └── processed/          # dados já filtrados para PE
├── mapa/                   # shapefile dos municípios de PE
├── notebooks/
│   └── analise.ipynb       # exploração original
├── tests/
│   ├── test_data.py
│   └── test_geo.py
└── .github/
    └── workflows/
        └── ci.yml          # lint + testes
```

## Como rodar localmente

Requisitos: Python 3.11 ou superior.

```bash
# 1. Clonar
git clone https://github.com/jpedrosmenezes/ProUni-Data.git
cd ProUni-Data

# 2. Ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Executar
streamlit run app.py
```

O app abre em `http://localhost:8501`.

## Testes e qualidade

```bash
pip install ruff pytest
ruff check .
pytest
```

## Tecnologias

- **Python**
- **Pandas** para tratamento de dados
- **GeoPandas** para dados geoespaciais
- **Matplotlib e Seaborn** para visualização
- **Streamlit** para a interface

## Próximos passos

- [ ] Normalizar bolsas por população (bolsas por mil habitantes)
- [ ] Mapa interativo com tooltip (município e total)
- [ ] Filtros por tipo de bolsa, modalidade e turno
- [ ] Incluir outros anos do ProUni e comparar a evolução
- [ ] Testes automatizados do merge de municípios

## Licença e fontes

- **Código:** [MIT](LICENSE) © 2026 João Pedro S. Menezes
- **Dados:** mantêm as licenças e termos de uso das fontes originais citadas acima.

## Autor

**João Pedro S. Menezes**: [GitHub](https://github.com/jpedrosmenezes)