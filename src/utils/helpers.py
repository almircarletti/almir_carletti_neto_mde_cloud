"""
Funções auxiliares para formatação e cálculos.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any


def format_number(value: float, decimals: int = 2) -> str:
    """Formata número com separadores de milhares."""
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}".replace(",", ".")


def create_metric_card(
    title: str, value: Any, delta: str = None, help_text: str = None
):
    """Cria um card de métrica estilizado."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label=title, value=value, delta=delta, help=help_text)


def create_simple_bar_chart(
    data, x_col: str, y_col: str, title: str, color_col: str = None
):
    """Cria gráfico de barras simples."""
    fig = px.bar(
        data, x=x_col, y=y_col, title=title, color=color_col, template="plotly_white"
    )
    fig.update_layout(showlegend=False, height=400, title_x=0.5)
    return fig


def create_donut_chart(labels: list, values: list, title: str):
    """Cria gráfico de rosca."""
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])

    fig.update_layout(title=title, title_x=0.5, height=400, template="plotly_white")
    return fig


def apply_custom_css():
    """Aplica CSS customizado ao Streamlit."""
    st.markdown(
        """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f4e79;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #2c5aa0;
        border-bottom: 2px solid #e1e5f2;
        padding-bottom: 0.5rem;
    }
    
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2c5aa0;
        margin: 1rem 0;
    }
    
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    /* Tornar sidebar fixa e não retrátil */
    .css-1d391kg {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        height: 100vh !important;
        width: 21rem !important;
        z-index: 999 !important;
        overflow-y: auto !important;
    }
    
    /* Esconder botão de retrair sidebar */
    .css-1rs6os {
        display: none !important;
    }
    
    .css-17eq0hr {
        display: none !important;
    }
    
    /* Ajustar conteúdo principal para não sobrepor a sidebar */
    .main .block-container {
        padding-left: 22rem !important;
        padding-top: 1rem !important;
    }
    
    /* Garantir que a sidebar não seja retrátil */
    .css-1d391kg[data-testid="stSidebar"] {
        transform: translateX(0) !important;
        transition: none !important;
    }
    
    /* Responsivo para dispositivos móveis */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
        }
        
        .css-1d391kg {
            width: 18rem !important;
        }
    }
    
    /* Garantir que elementos da sidebar sejam visíveis */
    .css-1d391kg .css-1v0mbdj {
        padding: 1rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def show_expansion_plans():
    """Exibe seção com planos de expansão futura."""
    st.markdown(
        '<div class="section-header">🚀 Planos de Expansão Futura</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Visualizações Avançadas")
        st.markdown(
            """
        - **Mapas Interativos**: Visualização geoespacial dos indicadores
        - **Séries Temporais**: Análise da evolução histórica
        - **Dashboards Comparativos**: Benchmarking entre municípios
        - **Gráficos de Correlação**: Análise de fatores correlacionados
        """
        )

        st.markdown("### 🤖 Analytics Avançado")
        st.markdown(
            """
        - **Machine Learning**: Modelos preditivos para IDEB
        - **Clustering**: Agrupamento de municípios similares
        - **Análise de Tendências**: Previsão de indicadores
        - **Detecção de Anomalias**: Identificação de padrões atípicos
        """
        )

    with col2:
        st.markdown("### 📱 Funcionalidades Técnicas")
        st.markdown(
            """
        - **Relatórios PDF**: Geração automática de relatórios
        - **Sistema de Alertas**: Notificações para metas críticas
        - **Dashboard Mobile**: Interface responsiva
        - **Exportação de Dados**: CSV, Excel, PDF
        """
        )

        st.markdown("### 📈 Análises Especializadas")
        st.markdown(
            """
        - **Análise Socioeconômica**: Correlação com dados do IBGE
        - **Impacto de Políticas**: Avaliação de intervenções
        - **Previsão de Desempenho**: Modelos preditivos para IDEB
        - **Análise de Eficiência**: Benchmarking entre municípios
        """
        )
