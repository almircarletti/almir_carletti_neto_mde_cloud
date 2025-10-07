"""
Componente de visão geral do dashboard.
"""

import streamlit as st
import plotly.express as px
from src.data.data_loader import DataLoader
from src.utils.helpers import create_metric_card, format_number


def render_overview(data_loader: DataLoader):
    """Renderiza a seção de visão geral."""
    st.markdown(
        '<div class="section-header">📊 Visão Geral dos Indicadores Educacionais</div>',
        unsafe_allow_html=True,
    )

    # Carrega estatísticas resumidas
    stats = data_loader.get_summary_stats()

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total de Municípios",
            stats["total_municipios"],
            help="Municípios do Espírito Santo analisados",
        )

    with col2:
        st.metric(
            "Total de Matrículas",
            f"{stats['total_matriculas']:,.0f}".replace(",", "."),
            help="Matrículas nos anos finais do ensino fundamental",
        )

    with col3:
        st.metric(
            "Municípios Acima da Meta",
            stats["municipios_acima_meta"],
            f"{(stats['municipios_acima_meta']/stats['total_registros_ideb']*100):.1f}%",
            help="Municípios que atingiram a meta IDEB 2023",
        )

    with col4:
        st.metric(
            "Taxa Média de Aprovação",
            f"{stats['taxa_aprovacao_media']:.1%}",
            help="Taxa média de aprovação nos anos finais",
        )

    # Gráficos de resumo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Distribuição IDEB por Rede")
        ideb_data = data_loader.load_ideb_data()
        ideb_summary = (
            ideb_data.groupby("REDE")
            .agg({"VL_OBSERVADO_2023": "mean", "acima_meta": "sum"})
            .round(2)
        )

        fig = px.bar(
            x=ideb_summary.index,
            y=ideb_summary["VL_OBSERVADO_2023"],
            title="IDEB Médio por Rede",
            template="plotly_white",
            color=ideb_summary["VL_OBSERVADO_2023"],
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📈 Matrículas por Rede")
        matriculas_data = data_loader.load_microdados()
        matriculas_rede = matriculas_data.groupby("REDE")["QT_MATRICULAS"].sum()

        fig = px.pie(
            values=matriculas_rede.values,
            names=matriculas_rede.index,
            title="Distribuição de Matrículas",
            template="plotly_white",
            hole=0.3,
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Informações adicionais
    st.markdown("### 📋 Resumo dos Dados Disponíveis")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown(
            """
        **Bases de Dados Utilizadas:**
        - 📊 **IDEB Final**: Índices e metas por município/rede
        - 👥 **Microdados**: Matrículas por série escolar  
        - 📈 **Dados por Série**: Taxas de rendimento escolar
        - 🗺️ **Cidades**: Mapeamento de municípios e SREs
        """
        )

    with info_col2:
        st.markdown(
            f"""
        **Redes de Ensino Analisadas:**
        {', '.join([f"• {rede}" for rede in stats['redes_analisadas']])}
        
        **Período de Referência:**
        • IDEB: 2023 (ano de observação)
        • Matrículas: Anos finais do Ensino Fundamental
        • Rendimento: Taxas de aprovação, reprovação e evasão
        """
        )

    # Destaque regional
    st.markdown("### 🌍 Contexto Regional")
    st.info(
        """
    **Espírito Santo - Indicadores Educacionais**
    
    Este dashboard apresenta uma análise dos indicadores educacionais dos municípios capixabas, 
    com foco no desempenho do IDEB e no rendimento escolar nos anos finais do ensino fundamental. 
    
    Os dados permitem comparar o desempenho entre redes municipal e estadual, identificar 
    municípios que atingiram suas metas e analisar padrões de evasão e aprovação escolar.
    """
    )
