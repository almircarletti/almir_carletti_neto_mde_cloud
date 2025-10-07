"""
Dashboard de Indicadores Educacionais do Espírito Santo
Desenvolvido por: Almir Carletti Neto

Dashboard interativo para análise dos indicadores educacionais
dos municípios capixabas, incluindo IDEB, matrículas e rendimento escolar.
"""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório src ao path para importações
sys.path.append(str(Path(__file__).parent / "src"))

from src.data.data_loader import DataLoader
from src.components.overview import render_overview
from src.components.ideb import render_ideb_analysis
from src.components.matriculas import render_matriculas_analysis
from src.components.rendimento import render_rendimento_analysis
from src.utils.helpers import apply_custom_css, show_expansion_plans


def main():
    """Função principal da aplicação."""
    # Configuração da página
    st.set_page_config(
        page_title="Dashboard Educacional - Espírito Santo",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Aplica CSS customizado
    apply_custom_css()

    # Cabeçalho principal
    st.markdown(
        """
    <div class="main-header">
        📚 Dashboard de Indicadores Educacionais do Espírito Santo
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <strong>Desenvolvido por:</strong> Almir Carletti Neto | 
        <strong>Fonte:</strong> INEP/MEC - Censo Escolar 2023 | 
        <strong>Tema:</strong> Análise de Indicadores Educacionais
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Inicializa o carregador de dados
    try:
        data_loader = DataLoader()

        # Verifica se os dados estão disponíveis
        stats = data_loader.get_summary_stats()

    except Exception as e:
        st.error(
            f"""
        ❌ **Erro ao carregar os dados:** {str(e)}
        
        Verifique se os arquivos CSV estão na pasta `database/`:
        - ideb_final.csv
        - microdados_final.csv  
        - dados_por_serie.csv
        - cities.csv
        """
        )
        st.stop()

    # Sidebar para navegação
    st.sidebar.markdown("### 🎓 ES Educação")

    st.sidebar.markdown("### 📋 Navegação")

    # Menu de navegação
    opcoes_menu = [
        "🏠 Visão Geral",
        "🎯 Análise IDEB",
        "👥 Análise de Matrículas",
        "📈 Rendimento Escolar",
        "🚀 Planos de Expansão",
    ]

    opcao_selecionada = st.sidebar.radio(
        "Selecione uma seção:",
        opcoes_menu,
        help="Navegue pelas diferentes análises disponíveis",
    )

    # Informações do sidebar
    st.sidebar.markdown("### 📊 Resumo dos Dados")
    st.sidebar.metric("Municípios", stats["total_municipios"])
    st.sidebar.metric(
        "Total Matrículas", f"{stats['total_matriculas']:,.0f}".replace(",", ".")
    )
    st.sidebar.metric(
        "IDEB Médio", f"{data_loader.load_ideb_data()['VL_OBSERVADO_2023'].mean():.2f}"
    )

    st.sidebar.markdown("### 🎓 Sobre o Dashboard")
    st.sidebar.info(
        """
    Este dashboard apresenta análises dos indicadores educacionais dos municípios 
    do Espírito Santo, com foco em:
    
    • **IDEB 2023**: Índice de qualidade educacional
    • **Matrículas**: Distribuição por município e rede
    • **Rendimento**: Taxas de aprovação, reprovação e evasão
    
    **Dados:** Censo Escolar 2023 - Anos Finais do Ensino Fundamental
    """
    )

    # Renderiza a seção selecionada
    if opcao_selecionada == "🏠 Visão Geral":
        render_overview(data_loader)

    elif opcao_selecionada == "🎯 Análise IDEB":
        render_ideb_analysis(data_loader)

    elif opcao_selecionada == "👥 Análise de Matrículas":
        render_matriculas_analysis(data_loader)

    elif opcao_selecionada == "📈 Rendimento Escolar":
        render_rendimento_analysis(data_loader)

    elif opcao_selecionada == "🚀 Planos de Expansão":
        show_expansion_plans()

    # Rodapé
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📊 Metodologia:**")
        st.markdown(
            """
        - Dados do Censo Escolar 2023
        - Foco nos Anos Finais (6º ao 9º ano)
        - Análise por município e rede
        """
        )

    with col2:
        st.markdown("**🛠️ Tecnologias:**")
        st.markdown(
            """
        - Streamlit (Interface)
        - Plotly (Visualizações)
        - Pandas (Processamento)
        """
        )

    with col3:
        st.markdown("**📈 Dados:**")
        st.markdown(
            """
        - 4 datasets CSV integrados
        - 1.400+ registros processados
        - Análise educacional completa
        """
        )


if __name__ == "__main__":
    main()
