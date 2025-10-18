"""
Componente de análise de rendimento escolar.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data.data_loader import DataLoader


def render_rendimento_analysis(data_loader: DataLoader, rede_selecionada):
    """Renderiza a seção de análise de rendimento escolar."""
    st.markdown(
        '<div class="section-header">📈 Análise de Rendimento Escolar</div>',
        unsafe_allow_html=True,
    )

    # Carrega dados
    dados_serie_df = data_loader.load_dados_serie()

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        rede_filter = st.selectbox(
            "Rede de Ensino:",
            ["Todas"] + list(dados_serie_df["REDE"].unique()),
            key="rendimento_rede",
        )

    with col2:
        anos_disponiveis = sorted(dados_serie_df["ANO_ESCOLAR"].unique())
        ano_filter = st.selectbox(
            "Ano Escolar:",
            ["Todos"] + [f"{ano}º ano" for ano in anos_disponiveis],
            key="rendimento_ano",
        )

    with col3:
        municipios = data_loader.get_municipios_list()
        municipio_filter = st.selectbox(
            "Município:", ["Todos"] + municipios, key="rendimento_municipio"
        )

    # Aplica filtros
    filtered_df = dados_serie_df.copy()

    if rede_filter != "Todas":
        filtered_df = filtered_df[filtered_df["REDE"] == rede_filter]

    if ano_filter != "Todos":
        ano_numero = int(ano_filter.split("º")[0])
        filtered_df = filtered_df[filtered_df["ANO_ESCOLAR"] == ano_numero]

    if municipio_filter != "Todos":
        cities_df = data_loader.load_cities()
        municipio_code = cities_df[cities_df["municipio"] == municipio_filter][
            "ibge_code"
        ].iloc[0]
        filtered_df = filtered_df[filtered_df["CO_MUNICIPIO"] == municipio_code]

    if len(filtered_df) > 0:
        # Calcula médias ponderadas pelas matrículas
        total_matriculas = filtered_df["QT_MATRICULAS"].sum()

        if total_matriculas > 0:
            taxa_aprovacao_media = (
                filtered_df["APROVADOS_ABSOLUTOS"].sum() / total_matriculas * 100
            )
            taxa_reprovacao_media = (
                filtered_df["REPROVADOS_ABSOLUTOS"].sum() / total_matriculas * 100
            )
            taxa_evasao_media = (
                filtered_df["EVASAO_ABSOLUTA"].sum() / total_matriculas * 100
            )
        else:
            taxa_aprovacao_media = taxa_reprovacao_media = taxa_evasao_media = 0

        # Métricas de rendimento
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Taxa de Aprovação",
                f"{taxa_aprovacao_media:.1f}%",
                help="Percentual de alunos aprovados",
            )

        with col2:
            st.metric(
                "Taxa de Reprovação",
                f"{taxa_reprovacao_media:.1f}%",
                help="Percentual de alunos reprovados",
            )

        with col3:
            st.metric(
                "Taxa de Evasão",
                f"{taxa_evasao_media:.1f}%",
                help="Percentual de alunos evadidos",
            )

        with col4:
            st.metric(
                "Total de Matrículas",
                f"{total_matriculas:,.0f}".replace(",", "."),
                help="Total de matrículas analisadas",
            )

        # Gráficos de análise
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Composição do Rendimento")

            labels = ["Aprovação", "Reprovação", "Evasão"]
            values = [taxa_aprovacao_media, taxa_reprovacao_media, taxa_evasao_media]
            colors = ["#2E8B57", "#DC143C", "#FF8C00"]

            fig = go.Figure(
                data=[
                    go.Pie(labels=labels, values=values, hole=0.3, marker_colors=colors)
                ]
            )

            fig.update_layout(
                title="Distribuição do Rendimento (%)",
                height=400,
                template="plotly_white",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 📈 Rendimento por Ano Escolar")

            rendimento_ano = (
                filtered_df.groupby("ANO_ESCOLAR")
                .agg(
                    {
                        "QT_MATRICULAS": "sum",
                        "APROVADOS_ABSOLUTOS": "sum",
                        "REPROVADOS_ABSOLUTOS": "sum",
                        "EVASAO_ABSOLUTA": "sum",
                    }
                )
                .reset_index()
            )

            # Calcula percentuais
            rendimento_ano["Taxa_Aprovacao"] = (
                rendimento_ano["APROVADOS_ABSOLUTOS"]
                / rendimento_ano["QT_MATRICULAS"]
                * 100
            )
            rendimento_ano["Taxa_Reprovacao"] = (
                rendimento_ano["REPROVADOS_ABSOLUTOS"]
                / rendimento_ano["QT_MATRICULAS"]
                * 100
            )
            rendimento_ano["Taxa_Evasao"] = (
                rendimento_ano["EVASAO_ABSOLUTA"]
                / rendimento_ano["QT_MATRICULAS"]
                * 100
            )

            rendimento_ano["ANO_ESCOLAR"] = (
                rendimento_ano["ANO_ESCOLAR"].astype(str) + "º ano"
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=rendimento_ano["ANO_ESCOLAR"],
                    y=rendimento_ano["Taxa_Aprovacao"],
                    name="Aprovação",
                    marker_color="#2E8B57",
                )
            )

            fig.add_trace(
                go.Bar(
                    x=rendimento_ano["ANO_ESCOLAR"],
                    y=rendimento_ano["Taxa_Reprovacao"],
                    name="Reprovação",
                    marker_color="#DC143C",
                )
            )

            fig.add_trace(
                go.Bar(
                    x=rendimento_ano["ANO_ESCOLAR"],
                    y=rendimento_ano["Taxa_Evasao"],
                    name="Evasão",
                    marker_color="#FF8C00",
                )
            )

            fig.update_layout(
                title="Taxas por Série (%)",
                barmode="group",
                height=400,
                template="plotly_white",
                yaxis_title="Percentual (%)",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Análise comparativa por rede
        if rede_filter == "Todas":
            st.markdown("### 🔍 Comparativo por Rede de Ensino")

            comp_rede = (
                filtered_df.groupby("REDE")
                .agg(
                    {
                        "QT_MATRICULAS": "sum",
                        "APROVADOS_ABSOLUTOS": "sum",
                        "REPROVADOS_ABSOLUTOS": "sum",
                        "EVASAO_ABSOLUTA": "sum",
                    }
                )
                .reset_index()
            )

            # Calcula percentuais por rede
            comp_rede["Taxa_Aprovacao"] = (
                comp_rede["APROVADOS_ABSOLUTOS"] / comp_rede["QT_MATRICULAS"] * 100
            ).round(1)
            comp_rede["Taxa_Reprovacao"] = (
                comp_rede["REPROVADOS_ABSOLUTOS"] / comp_rede["QT_MATRICULAS"] * 100
            ).round(1)
            comp_rede["Taxa_Evasao"] = (
                comp_rede["EVASAO_ABSOLUTA"] / comp_rede["QT_MATRICULAS"] * 100
            ).round(1)

            col1, col2 = st.columns([2, 1])

            with col1:
                # Gráfico de barras agrupadas
                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=comp_rede["REDE"],
                        y=comp_rede["Taxa_Aprovacao"],
                        name="Aprovação",
                        marker_color="#2E8B57",
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=comp_rede["REDE"],
                        y=comp_rede["Taxa_Reprovacao"],
                        name="Reprovação",
                        marker_color="#DC143C",
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=comp_rede["REDE"],
                        y=comp_rede["Taxa_Evasao"],
                        name="Evasão",
                        marker_color="#FF8C00",
                    )
                )

                fig.update_layout(
                    title="Comparativo de Rendimento por Rede",
                    barmode="group",
                    height=400,
                    template="plotly_white",
                    yaxis_title="Percentual (%)",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("**Resumo por Rede:**")
                for _, row in comp_rede.iterrows():
                    st.markdown(
                        f"""
                    **{row['REDE']}**
                    - Aprovação: {row['Taxa_Aprovacao']:.1f}%
                    - Reprovação: {row['Taxa_Reprovacao']:.1f}%
                    - Evasão: {row['Taxa_Evasao']:.1f}%
                    - Matrículas: {row['QT_MATRICULAS']:,.0f}
                    """.replace(
                            ",", "."
                        )
                    )

        # Ranking de municípios por aprovação
        st.markdown("### 🏆 Ranking de Municípios por Taxa de Aprovação")

        ranking_municipios = (
            filtered_df.groupby(["NO_MUNICIPIO", "REDE"])
            .agg({"QT_MATRICULAS": "sum", "APROVADOS_ABSOLUTOS": "sum"})
            .reset_index()
        )

        ranking_municipios["Taxa_Aprovacao"] = (
            ranking_municipios["APROVADOS_ABSOLUTOS"]
            / ranking_municipios["QT_MATRICULAS"]
            * 100
        ).round(1)
        ranking_municipios = ranking_municipios[
            ranking_municipios["QT_MATRICULAS"] >= 10
        ]  # Filtrar municípios com pelo menos 10 matrículas
        ranking_municipios = ranking_municipios.sort_values(
            "Taxa_Aprovacao", ascending=False
        ).head(15)

        # Exibe tabela do ranking
        ranking_display = ranking_municipios[
            ["NO_MUNICIPIO", "REDE", "Taxa_Aprovacao", "QT_MATRICULAS"]
        ].copy()
        ranking_display.columns = [
            "Município",
            "Rede",
            "Taxa Aprovação (%)",
            "Matrículas",
        ]

        st.dataframe(ranking_display, use_container_width=True, hide_index=True)

        # Tabela detalhada com todos os indicadores
        st.markdown("### 📋 Dados Detalhados por Município")

        tabela_detalhada = (
            filtered_df.groupby(["NO_MUNICIPIO", "REDE"])
            .agg(
                {
                    "QT_MATRICULAS": "sum",
                    "APROVADOS_ABSOLUTOS": "sum",
                    "REPROVADOS_ABSOLUTOS": "sum",
                    "EVASAO_ABSOLUTA": "sum",
                }
            )
            .reset_index()
        )

        tabela_detalhada["Taxa_Aprovacao"] = (
            tabela_detalhada["APROVADOS_ABSOLUTOS"]
            / tabela_detalhada["QT_MATRICULAS"]
            * 100
        ).round(1)
        tabela_detalhada["Taxa_Reprovacao"] = (
            tabela_detalhada["REPROVADOS_ABSOLUTOS"]
            / tabela_detalhada["QT_MATRICULAS"]
            * 100
        ).round(1)
        tabela_detalhada["Taxa_Evasao"] = (
            tabela_detalhada["EVASAO_ABSOLUTA"]
            / tabela_detalhada["QT_MATRICULAS"]
            * 100
        ).round(1)

        tabela_display = tabela_detalhada[
            [
                "NO_MUNICIPIO",
                "REDE",
                "QT_MATRICULAS",
                "Taxa_Aprovacao",
                "Taxa_Reprovacao",
                "Taxa_Evasao",
            ]
        ].sort_values(["NO_MUNICIPIO", "REDE"])

        tabela_display.columns = [
            "Município",
            "Rede",
            "Matrículas",
            "Aprovação (%)",
            "Reprovação (%)",
            "Evasão (%)",
        ]

        st.dataframe(
            tabela_display, use_container_width=True, hide_index=True, height=400
        )

    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")

    # Informações sobre rendimento escolar
    with st.expander("ℹ️ Sobre os Indicadores de Rendimento"):
        st.markdown(
            """
        **Definições:**
        
        - **Taxa de Aprovação**: Percentual de alunos aprovados para a próxima série
        - **Taxa de Reprovação**: Percentual de alunos retidos na mesma série
        - **Taxa de Evasão**: Percentual de alunos que abandonaram a escola
        
        **Importância:**
        - Indicadores essenciais para o cálculo do IDEB
        - Refletem a eficiência do sistema educacional
        - Influenciam diretamente na qualidade da educação
        
        **Meta Nacional:**
        - Reduzir as taxas de reprovação e evasão
        - Aumentar a taxa de aprovação com qualidade
        - Atingir fluxo escolar adequado (aprovação próxima a 100%)
        
        **Fonte:** Censo Escolar 2023 - INEP/MEC
        """
        )
