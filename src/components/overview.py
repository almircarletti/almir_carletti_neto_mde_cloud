"""
Componente de visão geral do dashboard.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from src.data.data_loader import DataLoader
from src.utils.helpers import create_metric_card, format_number


def render_overview(data_loader: DataLoader, rede_selecionada):
    """Renderiza a seção de visão geral."""
    st.markdown(
        '<div class="section-header">📊 Visão Geral dos Indicadores Educacionais</div>',
        unsafe_allow_html=True,
    )

    # Carrega dados filtrados por rede
    ideb_data = data_loader.load_ideb_data()[
        data_loader.load_ideb_data()["REDE"] == rede_selecionada
    ]
    microdados_data = data_loader.load_microdados()[
        data_loader.load_microdados()["REDE"] == rede_selecionada
    ]
    dados_serie_data = data_loader.load_dados_serie()[
        data_loader.load_dados_serie()["REDE"] == rede_selecionada
    ]

    # Calcula estatísticas filtradas
    municipios_filtrados = len(ideb_data["CO_MUNICIPIO"].unique())
    matriculas_filtradas = microdados_data["QT_MATRICULAS"].sum()
    municipios_acima_meta = len(ideb_data[ideb_data["acima_meta"] == True])
    taxa_aprovacao_media = dados_serie_data["TAXA_APROVACAO"].mean()

    # Mostra informação sobre o filtro
    st.info(f"📊 **Dados filtrados para:** {rede_selecionada}")

    # Métricas principais (filtradas)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Municípios",
            municipios_filtrados,
            help=f"Municípios do Espírito Santo - {rede_selecionada}",
        )

    with col2:
        st.metric(
            "Total de Matrículas",
            f"{matriculas_filtradas:,.0f}".replace(",", "."),
            help=f"Matrículas nos anos finais - {rede_selecionada}",
        )

    with col3:
        st.metric(
            "Municípios Acima da Meta",
            municipios_acima_meta,
            (
                f"{(municipios_acima_meta/municipios_filtrados*100):.1f}%"
                if municipios_filtrados > 0
                else "0%"
            ),
            help=f"Municípios que atingiram a meta IDEB 2023 - {rede_selecionada}",
        )

    with col4:
        st.metric(
            "Taxa Média de Aprovação",
            (
                f"{taxa_aprovacao_media:.1%}"
                if not pd.isna(taxa_aprovacao_media)
                else "N/A"
            ),
            help=f"Taxa média de aprovação nos anos finais - {rede_selecionada}",
        )

    # Gráficos de resumo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 IDEB por Município")
        # Remove valores nulos para o gráfico
        ideb_validos = ideb_data.dropna(subset=["VL_OBSERVADO_2023"])

        if len(ideb_validos) > 0:
            fig = px.bar(
                ideb_validos,
                x="NO_MUNICIPIO",
                y="VL_OBSERVADO_2023",
                title=f"IDEB 2023 - {rede_selecionada}",
                template="plotly_white",
                color="VL_OBSERVADO_2023",
                color_continuous_scale=["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_tickangle=-45,
                coloraxis_colorbar=dict(title="IDEB"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de IDEB disponíveis para esta rede.")

    with col2:
        st.markdown("### 📈 Matrículas por Série")
        if len(microdados_data) > 0:
            matriculas_serie = microdados_data.groupby("ANO_ESCOLAR")[
                "QT_MATRICULAS"
            ].sum()

            fig = px.bar(
                x=matriculas_serie.index,
                y=matriculas_serie.values,
                title=f"Matrículas por Série - {rede_selecionada}",
                template="plotly_white",
                color=matriculas_serie.values,
                color_continuous_scale=["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Série",
                yaxis_title="Matrículas",
                coloraxis_colorbar=dict(title="Matrículas"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de matrículas disponíveis para esta rede.")

    # Informações adicionais
    st.markdown("### 📋 Resumo dos Dados Disponíveis")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown(
            f"""
        **Dados Filtrados para {rede_selecionada}:**
        - 📊 **Municípios**: {municipios_filtrados} municípios analisados
        - 👥 **Matrículas**: {matriculas_filtradas:,.0f} alunos matriculados
        - 🎯 **Acima da Meta**: {municipios_acima_meta} municípios
        - 📈 **Taxa Aprovação**: {taxa_aprovacao_media:.1%} média
        """
        )

    with info_col2:
        st.markdown(
            f"""
        **Rede Selecionada:**
        • {rede_selecionada}
        
        **Período de Referência:**
        • IDEB: 2023 (ano de observação)
        • Matrículas: Anos finais do Ensino Fundamental (6º-9º)
        • Rendimento: Taxas de aprovação, reprovação e evasão
        """
        )

    # Destaque regional
    st.markdown("### 🌍 Contexto Regional")
    st.info(
        f"""
    **Espírito Santo - Rede {rede_selecionada}**
    
    Esta análise apresenta os indicadores educacionais dos municípios capixabas da rede {rede_selecionada}, 
    com foco no desempenho do IDEB e no rendimento escolar nos anos finais do ensino fundamental. 
    
    Os dados permitem identificar municípios que atingiram suas metas IDEB, analisar padrões de 
    evasão e aprovação escolar, e comparar o desempenho entre diferentes municípios da mesma rede.
    """
    )
