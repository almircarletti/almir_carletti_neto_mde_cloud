# Dashboard de Indicadores Educacionais do Espírito Santo

## Desenvolvido por: Almir Carletti Neto

### Descrição do Projeto

Este é um dashboard interativo desenvolvido em Streamlit para análise dos indicadores educacionais dos municípios do Espírito Santo, focando em dados do IDEB, matrículas, taxas de aprovação, reprovação e evasão escolar.

### Como Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Estrutura do Projeto

```
├── app.py                 # Aplicação principal
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_loader.py # Carregamento e processamento dos dados
│   ├── components/
│   │   ├── __init__.py
│   │   ├── overview.py    # Visão geral
│   │   ├── ideb.py        # Análise do IDEB
│   │   ├── matriculas.py  # Análise de matrículas
│   │   └── rendimento.py  # Taxas de rendimento
│   └── utils/
│       ├── __init__.py
│       └── helpers.py     # Funções auxiliares
├── database/              # Dados CSV
├── requirements.txt
└── README.md
```

### Dados Utilizados

- **ideb_final.csv**: Índices IDEB 2023 por município e rede
- **microdados_final.csv**: Dados de matrículas por série
- **dados_por_serie.csv**: Taxas de aprovação, reprovação e evasão
- **cities.csv**: Mapeamento de municípios e SREs

### Funcionalidades Atuais

1. **Visão Geral**: Dashboard principal com métricas resumidas
2. **Análise IDEB**: Comparação entre metas e resultados
3. **Análise de Matrículas**: Distribuição por município e rede
4. **Rendimento Escolar**: Taxas de aprovação, reprovação e evasão

### Planos de Expansão Futura

- Mapas interativos com visualizações geoespaciais
- Análises preditivas com machine learning
- Comparações temporais (séries históricas)
- Relatórios automatizados em PDF
- Sistema de alertas para indicadores críticos
- Dashboard mobile responsivo
- Sistema de exportação de dados em múltiplos formatos
