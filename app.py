"""
Dashboard de Indicadores Educacionais do Espírito Santo
Desenvolvido por: Almir Carletti Neto

Dashboard interativo para análise dos indicadores educacionais
dos municípios capixabas, incluindo IDEB, matrículas e rendimento escolar.
"""

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Dashboard Educacional ES - Almir Carletti Neto",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c5aa0;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6, #ffffff, #f0f2f6);
        border-radius: 10px;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c5aa0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-left: 4px solid #2c5aa0;
        background-color: #f8f9fa;
    }
    
    .info-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .placeholder-box {
        background-color: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        color: #6c757d;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background-color: #f8f9fa;
        border-top: 1px solid #e1e5e9;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    # Header principal
    st.markdown(
        '<h1 class="main-header">🎓 Indicadores Educacionais do Espírito Santo</h1>',
        unsafe_allow_html=True,
    )

    # Informações do desenvolvedor
    st.markdown(
        '<h2 class="section-header">👨‍💻 Desenvolvedor</h2>', unsafe_allow_html=True
    )

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Nome:** Almir Carletti Neto")
        with col2:
            st.info("**Disciplina:** Cloud Computing para produtos de dados")
        with col3:
            st.info("**Instituição:** IFES - Campus Serra")

    # Tema do projeto
    st.markdown(
        '<h2 class="section-header">🎯 Tema do Projeto</h2>', unsafe_allow_html=True
    )
    st.markdown(
        """
    <div class="info-card">
        <p>Este projeto visa criar um <strong>dashboard interativo</strong> para análise e visualização de indicadores educacionais do Espírito Santo, 
        permitindo aos gestores educacionais e pesquisadores explorar dados de forma intuitiva e eficiente.</p>
        <p>O foco está na <strong>transformação de dados brutos</strong> em insights acionáveis através de visualizações 
        interativas e análises comparativas entre municípios, redes de ensino e séries escolares.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Seções do Dashboard usando Layouts e Containers
    st.markdown(
        '<h2 class="section-header">📊 Seções do Dashboard</h2>', unsafe_allow_html=True
    )

    # Seção 1: Visão Geral
    with st.container():
        st.subheader("📈 Visão Geral")
        st.markdown(
            "Dashboard principal com métricas consolidadas e indicadores-chave de performance educacional"
        )

        # Layout em colunas para métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                '<div class="placeholder-box">📊 Área para card - Total de Municípios</div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                '<div class="placeholder-box">📊 Área para card - Rede Pública</div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                '<div class="placeholder-box">📊 Área para card - Rede Privada</div>',
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                '<div class="placeholder-box">📊 Área para card - Meta IDEB</div>',
                unsafe_allow_html=True,
            )

        # Placeholder para gráfico futuro
        with st.container():
            st.markdown(
                '<div class="placeholder-box">📊 Área para gráfico de evolução temporal dos indicadores</div>',
                unsafe_allow_html=True,
            )

    # Seção 2: Análise IDEB
    with st.container():
        st.subheader("🎯 Análise IDEB")
        st.markdown(
            "Comparação de metas vs. observado, ranking de municípios e evolução temporal"
        )

        # Layout em colunas para análise IDEB
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                '<div class="placeholder-box">📈 Área para gráfico de comparação metas vs. resultados IDEB</div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                '<div class="placeholder-box">🏆 Área para ranking dos municípios</div>',
                unsafe_allow_html=True,
            )

    # Seção 3: Análise de Matrículas
    with st.container():
        st.subheader("👥 Análise de Matrículas")
        st.markdown(
            "Distribuição por série, rede de ensino e evolução das matrículas ao longo do tempo"
        )

        # Layout em colunas para análise de matrículas
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                '<div class="placeholder-box">🍕 Área para gráfico de pizza - distribuição por rede</div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                '<div class="placeholder-box">📊 Área para gráfico de barras - matrículas por série</div>',
                unsafe_allow_html=True,
            )

    # Seção 4: Análise de Rendimento
    with st.container():
        st.subheader("📚 Análise de Rendimento")
        st.markdown(
            "Taxas de aprovação, reprovação e abandono por série e rede de ensino"
        )

        # Layout em colunas para análise de rendimento
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                '<div class="placeholder-box">✅ Área para taxas de aprovação</div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                '<div class="placeholder-box">❌ Área para taxas de reprovação</div>',
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                '<div class="placeholder-box">🚪 Área para taxas de abandono</div>',
                unsafe_allow_html=True,
            )

    # Bases de dados
    st.markdown(
        '<h2 class="section-header">🗄️ Bases de Dados Planejadas</h2>',
        unsafe_allow_html=True,
    )

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            <div class="info-card">
                <h4>📊 Dados IDEB</h4>
                <p><strong>Fonte:</strong> INEP - Instituto Nacional de Estudos e Pesquisas Educacionais</p>
                <p><strong>Conteúdo:</strong> Índice de Desenvolvimento da Educação Básica por município e série</p>
                <p><strong>Frequência:</strong> Anual</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <div class="info-card">
                <h4>👥 Microdados de Matrículas</h4>
                <p><strong>Fonte:</strong> Censo Escolar INEP</p>
                <p><strong>Conteúdo:</strong> Dados detalhados de matrículas por escola, série e rede</p>
                <p><strong>Frequência:</strong> Anual</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class="info-card">
                <h4>📚 Dados de Rendimento</h4>
                <p><strong>Fonte:</strong> Censo Escolar INEP</p>
                <p><strong>Conteúdo:</strong> Taxas de aprovação, reprovação e abandono escolar</p>
                <p><strong>Frequência:</strong> Anual</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <div class="info-card">
                <h4>🏛️ Dados Geográficos</h4>
                <p><strong>Fonte:</strong> IBGE - Instituto Brasileiro de Geografia e Estatística</p>
                <p><strong>Conteúdo:</strong> Informações demográficas e geográficas dos municípios</p>
                <p><strong>Frequência:</strong> Decenal (Censo) / Anual (Estimativas)</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Footer
    st.markdown(
        """
    <div class="footer">
        <p><strong>Desenvolvido por:</strong> Almir Carletti Neto | <strong>IFES</strong> | <strong>2025</strong></p>
        <p>Dashboard Educacional do Espírito Santo - Projeto Acadêmico</p>
        <p><em>Versão de baixa estética e usabilidade - Estrutura das seções implementada com Layouts e Containers do Streamlit</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
