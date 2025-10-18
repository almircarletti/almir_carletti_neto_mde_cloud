"""
Componente de análise de matrículas.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from src.data.data_loader import DataLoader


def render_matriculas_analysis(data_loader: DataLoader):
    """Renderiza a seção de análise de matrículas."""
    st.markdown(
        '<div class="section-header">👥 Análise de Matrículas Escolares</div>',
        unsafe_allow_html=True,
    )

    # Carrega dados
    microdados_df = data_loader.load_microdados()

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        rede_filter = st.selectbox(
            "Rede de Ensino:",
            ["Todas"] + list(microdados_df["REDE"].unique()),
            key="matriculas_rede",
        )

    with col2:
        anos_disponiveis = sorted(microdados_df["ANO_ESCOLAR"].unique())
        ano_filter = st.selectbox(
            "Ano Escolar:",
            ["Todos"] + [f"{ano}º ano" for ano in anos_disponiveis],
            key="matriculas_ano",
        )

    with col3:
        municipios = data_loader.get_municipios_list()
        municipio_filter = st.selectbox(
            "Município:", ["Todos"] + municipios, key="matriculas_municipio"
        )

    # Aplica filtros
    filtered_df = microdados_df.copy()

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

    # Métricas de matrículas
    total_matriculas = filtered_df["QT_MATRICULAS"].sum()
    total_municipios = filtered_df["NO_MUNICIPIO"].nunique()
    media_por_municipio = (
        total_matriculas / total_municipios if total_municipios > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total de Matrículas",
            f"{total_matriculas:,.0f}".replace(",", "."),
            help="Total de matrículas nos filtros selecionados",
        )

    with col2:
        st.metric("Municípios", total_municipios, help="Número de municípios com dados")

    with col3:
        st.metric(
            "Média por Município",
            f"{media_por_municipio:.0f}",
            help="Média de matrículas por município",
        )

    with col4:
        if len(filtered_df) > 0:
            maior_municipio = (
                filtered_df.groupby("NO_MUNICIPIO")["QT_MATRICULAS"].sum().idxmax()
            )
            st.metric(
                "Maior Município", maior_municipio, help="Município com mais matrículas"
            )
        else:
            st.metric("Maior Município", "N/A")

    if len(filtered_df) > 0:
        # Gráficos de análise
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Matrículas por Ano Escolar")

            matriculas_ano = (
                filtered_df.groupby("ANO_ESCOLAR")["QT_MATRICULAS"].sum().reset_index()
            )
            matriculas_ano["ANO_ESCOLAR"] = (
                matriculas_ano["ANO_ESCOLAR"].astype(str) + "º ano"
            )

            fig = px.bar(
                matriculas_ano,
                x="ANO_ESCOLAR",
                y="QT_MATRICULAS",
                title="Distribuição por Série",
                template="plotly_white",
                color="QT_MATRICULAS",
                color_continuous_scale="Blues",
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🏫 Matrículas por Rede")

            matriculas_rede = filtered_df.groupby("REDE")["QT_MATRICULAS"].sum()

            fig = px.pie(
                values=matriculas_rede.values,
                names=matriculas_rede.index,
                title="Distribuição por Rede",
                template="plotly_white",
                hole=0.3,
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Ranking de municípios
        st.markdown("### 🏆 Ranking de Municípios por Matrículas")

        ranking_municipios = (
            filtered_df.groupby(["NO_MUNICIPIO", "REDE"])["QT_MATRICULAS"]
            .sum()
            .reset_index()
        )
        ranking_municipios = ranking_municipios.sort_values(
            "QT_MATRICULAS", ascending=False
        ).head(15)

        fig = px.bar(
            ranking_municipios,
            x="QT_MATRICULAS",
            y="NO_MUNICIPIO",
            color="REDE",
            orientation="h",
            title="Top 15 Municípios",
            template="plotly_white",
            height=600,
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

        # Tabela detalhada
        st.markdown("### 📋 Dados Detalhados")

        tabela_detalhada = (
            filtered_df.groupby(["NO_MUNICIPIO", "REDE", "ANO_ESCOLAR"])[
                "QT_MATRICULAS"
            ]
            .sum()
            .reset_index()
        )
        tabela_detalhada = tabela_detalhada.sort_values(
            ["NO_MUNICIPIO", "REDE", "ANO_ESCOLAR"]
        )
        tabela_detalhada["ANO_ESCOLAR"] = (
            tabela_detalhada["ANO_ESCOLAR"].astype(str) + "º ano"
        )
        tabela_detalhada.columns = ["Município", "Rede", "Ano Escolar", "Matrículas"]

        st.dataframe(
            tabela_detalhada, use_container_width=True, hide_index=True, height=400
        )

        # Análise por SRE
        if municipio_filter == "Todos":
            st.markdown(
                "### 🌍 Análise por SRE (Superintendência Regional de Educação)"
            )

            cities_df = data_loader.load_cities()
            df_with_sre = filtered_df.merge(
                cities_df[["ibge_code", "sre"]],
                left_on="CO_MUNICIPIO",
                right_on="ibge_code",
                how="left",
            )

            sre_analysis = (
                df_with_sre.groupby("sre")["QT_MATRICULAS"]
                .sum()
                .sort_values(ascending=False)
            )

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.bar(
                    x=sre_analysis.values,
                    y=sre_analysis.index,
                    orientation="h",
                    title="Matrículas por SRE",
                    template="plotly_white",
                )
                fig.update_layout(
                    height=400, yaxis={"categoryorder": "total ascending"}
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("**Resumo por SRE:**")
                for sre, matriculas in sre_analysis.head(5).items():
                    st.write(f"• **{sre}**: {matriculas:,.0f}".replace(",", "."))

    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")

    # Informações sobre os dados
    with st.expander("ℹ️ Sobre os Dados de Matrículas"):
        st.markdown(
            """
        **Fonte dos Dados:**
        - Censo Escolar 2023 (INEP/MEC)
        - Anos Finais do Ensino Fundamental (6º ao 9º ano)
        
        **Cobertura:**
        - Rede Estadual e Municipal
        - Todos os municípios do Espírito Santo
        
        **Observações:**
        - Dados referem-se ao ano letivo de 2023
        - Inclui apenas escolas públicas
        - Valores zerados podem indicar ausência de oferta da série no município/rede
        """
        )
