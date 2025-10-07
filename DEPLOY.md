# 🚀 Guia de Deploy do Dashboard Educacional

## Deploy no Streamlit Cloud (Recomendado)

### 1. Preparação

1. **Crie uma conta** no [Streamlit Cloud](https://streamlit.io/cloud)
2. **Conecte seu GitHub** à conta do Streamlit Cloud
3. **Crie um repositório** no GitHub com os arquivos do projeto

### 2. Deploy

1. No Streamlit Cloud, clique em **"New app"**
2. Selecione seu repositório GitHub
3. Defina o arquivo principal como: `app.py`
4. Clique em **"Deploy"**

### 3. Configurações Importantes

- **Branch**: main (ou master)
- **File path**: app.py
- **Python version**: 3.8+

## Deploy Local para Desenvolvimento

### 1. Instalação Rápida

```bash
# Clonar ou baixar o projeto
cd "Trabalho 01 - Streamlit"

# Instalar dependências
pip install -r requirements.txt

# Executar
streamlit run app.py
```

### 2. Usando o Script Automático

```bash
python run_app.py
```

## Estrutura Final do Projeto

```
Trabalho 01 - Streamlit/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── README.md             # Documentação
├── DEPLOY.md             # Este arquivo
├── run_app.py            # Script de execução local
├── test_app.py           # Testes
├── .streamlit/
│   └── config.toml       # Configurações do Streamlit
├── src/
│   ├── data/
│   │   └── data_loader.py # Carregamento de dados
│   ├── components/       # Componentes do dashboard
│   │   ├── overview.py
│   │   ├── ideb.py
│   │   ├── matriculas.py
│   │   └── rendimento.py
│   └── utils/
│       └── helpers.py    # Funções auxiliares
└── database/             # Dados CSV
    ├── ideb_final.csv
    ├── microdados_final.csv
    ├── dados_por_serie.csv
    └── cities.csv
```

**Versão:** 1.0
