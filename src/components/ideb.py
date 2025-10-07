"""
Componente de análise do IDEB.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data.data_loader import DataLoader


def render_ideb_analysis(data_loader: DataLoader):
    """Renderiza a seção de análise do IDEB."""
    st.markdown(
        '<div class="section-header">🎯 Análise do IDEB - Índice de Desenvolvimento da Educação Básica</div>',
        unsafe_allow_html=True,
    )

    # Carrega dados do IDEB
    ideb_df = data_loader.load_ideb_data()

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        rede_filter = st.selectbox(
            "Selecione a Rede:",
            ["Todas"] + list(ideb_df["REDE"].unique()),
            help="Filtrar análise por rede de ensino",
        )

    with col2:
        municipios = data_loader.get_municipios_list()
        municipio_filter = st.selectbox(
            "Selecione o Município:",
            ["Todos"] + municipios,
            help="Filtrar análise por município específico",
        )

    # Aplica filtros
    filtered_df = ideb_df.copy()
    if rede_filter != "Todas":
        filtered_df = filtered_df[filtered_df["REDE"] == rede_filter]

    if municipio_filter != "Todos":
        cities_df = data_loader.load_cities()
        municipio_code = cities_df[cities_df["municipio"] == municipio_filter][
            "ibge_code"
        ].iloc[0]
        filtered_df = filtered_df[filtered_df["CO_MUNICIPIO"] == municipio_code]

    # Métricas IDEB
    col1, col2, col3, col4 = st.columns(4)

    # Remove valores nulos para cálculos
    valid_data = filtered_df.dropna(subset=["VL_OBSERVADO_2023"])

    with col1:
        ideb_medio = valid_data["VL_OBSERVADO_2023"].mean()
        st.metric(
            "IDEB Médio 2023",
            f"{ideb_medio:.2f}" if not pd.isna(ideb_medio) else "N/A",
            help="Valor médio do IDEB observado em 2023",
        )

    with col2:
        meta_media = valid_data["VL_PROJECAO_2021"].mean()
        st.metric(
            "Meta Média",
            f"{meta_media:.2f}" if not pd.isna(meta_media) else "N/A",
            help="Valor médio das metas projetadas",
        )

    with col3:
        acima_meta = len(valid_data[valid_data["acima_meta"] == True])
        total_valid = len(valid_data)
        perc_acima = (acima_meta / total_valid * 100) if total_valid > 0 else 0
        st.metric(
            "Acima da Meta",
            f"{acima_meta}/{total_valid}",
            f"{perc_acima:.1f}%",
            help="Número e percentual de registros acima da meta",
        )

    with col4:
        if len(valid_data) > 0:
            diferenca_media = (
                valid_data["VL_OBSERVADO_2023"] - valid_data["VL_PROJECAO_2021"]
            ).mean()
            delta_symbol = "+" if diferenca_media > 0 else ""
            st.metric(
                "Diferença Média",
                f"{delta_symbol}{diferenca_media:.2f}",
                help="Diferença média entre IDEB observado e meta",
            )
        else:
            st.metric("Diferença Média", "N/A")

    # Gráficos de análise
    if len(valid_data) > 0:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 IDEB vs Meta por Município")

            # Prepara dados para o gráfico
            chart_data = valid_data.copy()
            chart_data["Status"] = chart_data["acima_meta"].map(
                {True: "Acima da Meta", False: "Abaixo da Meta"}
            )

            fig = px.scatter(
                chart_data,
                x="VL_PROJECAO_2021",
                y="VL_OBSERVADO_2023",
                color="Status",
                hover_data=["NO_MUNICIPIO", "REDE"],
                title="IDEB Observado vs Meta",
                template="plotly_white",
                color_discrete_map={
                    "Acima da Meta": "#2E8B57",
                    "Abaixo da Meta": "#DC143C",
                },
            )

            # Linha de igualdade (y = x)
            min_val = min(
                chart_data["VL_PROJECAO_2021"].min(),
                chart_data["VL_OBSERVADO_2023"].min(),
            )
            max_val = max(
                chart_data["VL_PROJECAO_2021"].max(),
                chart_data["VL_OBSERVADO_2023"].max(),
            )
            fig.add_trace(
                go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode='lines',
                    line=dict(dash="dash", color="gray"),
                    name="Meta = Observado",
                    showlegend=True
                )
            )

            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🏆 Ranking dos Municípios")

            # Top 10 municípios por IDEB
            ranking = valid_data.nlargest(10, "VL_OBSERVADO_2023")[
                [
                    "NO_MUNICIPIO",
                    "REDE",
                    "VL_OBSERVADO_2023",
                    "VL_PROJECAO_2021",
                    "acima_meta",
                ]
            ].round(2)

            ranking["Status"] = ranking["acima_meta"].map({True: "✅", False: "❌"})
            ranking_display = ranking[
                ["NO_MUNICIPIO", "REDE", "VL_OBSERVADO_2023", "Status"]
            ]
            ranking_display.columns = ["Município", "Rede", "IDEB 2023", "Meta"]

            st.dataframe(ranking_display, use_container_width=True, hide_index=True)

        # Análise por rede
        st.markdown("### 🔍 Comparativo por Rede de Ensino")

        rede_analysis = (
            valid_data.groupby("REDE")
            .agg(
                {
                    "VL_OBSERVADO_2023": ["mean", "count"],
                    "VL_PROJECAO_2021": "mean",
                    "acima_meta": "sum",
                }
            )
            .round(3)
        )

        rede_analysis.columns = [
            "IDEB_Médio",
            "Qtd_Registros",
            "Meta_Média",
            "Acima_Meta",
        ]
        rede_analysis["Perc_Acima_Meta"] = (
            rede_analysis["Acima_Meta"] / rede_analysis["Qtd_Registros"] * 100
        ).round(1)
        rede_analysis["Diferença"] = (
            rede_analysis["IDEB_Médio"] - rede_analysis["Meta_Média"]
        ).round(3)

        st.dataframe(
            rede_analysis[
                [
                    "IDEB_Médio",
                    "Meta_Média",
                    "Diferença",
                    "Acima_Meta",
                    "Perc_Acima_Meta",
                ]
            ],
            use_container_width=True,
        )

    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")

    # Informações sobre o IDEB
    with st.expander("ℹ️ Sobre o IDEB"):
        st.markdown(
            """
        **O que é o IDEB?**
        
        O Índice de Desenvolvimento da Educação Básica (IDEB) é um indicador de qualidade educacional 
        que combina informações de desempenho em exames padronizados com informações sobre rendimento escolar.
        
        **Como é calculado:**
        - **Desempenho**: Resultados da Prova Brasil/SAEB
        - **Rendimento**: Taxa de aprovação escolar
        - **Fórmula**: IDEB = Desempenho × Taxa de Aprovação
        
        **Interpretação:**
        - **Escala**: 0 a 10 pontos
        - **Meta**: Definida para cada município/escola
        - **Objetivo**: Atingir média 6,0 até 2022 (padrão OCDE)
        """
        )
