"""
Componente da Página Inicial do Dashboard Educacional
Desenvolvido por: Almir Carletti Neto

Página inicial explicativa sobre o projeto, seguindo a estrutura:
Contexto - Ação - Resultado
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def render_homepage(data_loader, rede_selecionada):
    """
    Renderiza a página inicial do dashboard com informações sobre o projeto.

    Args:
        data_loader: Instância do DataLoader para acessar os dados
        rede_selecionada: Rede de ensino selecionada para filtrar os dados
    """

    # Seção Contexto
    st.markdown("---")
    st.markdown("## 🎯 Contexto")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        ### O Desafio da Visualização Educacional
        
        A análise de indicadores educacionais requer ferramentas que permitam:
        
        - **Acessibilidade**: Interface intuitiva para gestores e pesquisadores
        - **Interatividade**: Exploração dinâmica dos dados
        - **Reprodutibilidade**: Solução que possa ser facilmente replicada
        - **Baixo Custo**: Tecnologias acessíveis e de código aberto
      
        """
        )

    # Seção Ação
    st.markdown("---")
    st.markdown("## ⚡ Uma breve comparação entre as tecnologias utilizadas")

    st.markdown(
        """
    ### Por que não usar Power BI, por exemplo?
    
    Bom, aqui vão alguns motivos que tornam o streamlit uma melhor opção:
    """
    )

    # Comparação Power BI vs Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        #### 🔄 **Power BI**
        
        - ✅ Interface visual intuitiva
        - ✅ Integração com Power Query
        - ❌ Licenciamento pago
        - ❌ Dependência de plataforma Microsoft
        - ❌ Limitações de customização
        - ❌ Dificuldade para deploy público
        """
        )

    with col2:
        st.markdown(
            """
        #### 🚀 **Streamlit (Atual)**
        
        - ✅ **Código aberto e gratuito**
        - ✅ **Deploy fácil e gratuito** (Streamlit Cloud)
        - ✅ **Customização total** da interface
        - ✅ **Integração nativa** com Python
        - ✅ **Reprodutibilidade** completa
        - ✅ **Escalabilidade** para novos recursos
        """
        )

    # Seção Resultado
    st.markdown("---")
    st.markdown("## 🎉 Resultado")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
        ### 🏆 Benefícios Alcançados
        
        #### **Acessibilidade**
        - Interface web responsiva
        - Acesso público gratuito
        - Navegação intuitiva
        
        #### **Interatividade**
        - Mapas clicáveis
        - Filtros dinâmicos
        - Visualizações interativas
        
        #### **Reprodutibilidade**
        - Código fonte disponível
        - Documentação completa
        - Pipeline automatizado
        """
        )

    with col2:
        st.markdown(
            """
        ### 📊 Indicadores Disponíveis
        
        #### **IDEB 2023**
        - Comparação com metas
        - Análise por município
        - Evolução temporal
        
        #### **Matrículas**
        - Distribuição por rede
        - Concentração geográfica
        - Tendências demográficas
        
        #### **Rendimento Escolar**
        - Taxas de aprovação
        - Índices de reprovação
        - Análise de evasão
        """
        )

    # Call to action
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px; margin: 2rem 0;">
        <h3 style="color: #1f77b4; margin-bottom: 1rem;">
            🚀 Explore o Dashboard
        </h3>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
            Navegue pelas diferentes análises disponíveis usando o menu lateral
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <strong>🎯 IDEB</strong><br>
                <small>Qualidade educacional</small>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <strong>👥 Matrículas</strong><br>
                <small>Distribuição demográfica</small>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <strong>📈 Rendimento</strong><br>
                <small>Taxas escolares</small>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Informações técnicas
    st.markdown("---")
    st.markdown("### 🛠️ Informações Técnicas")

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.markdown(
            """
        **📊 Dados**
        - Censo Escolar 2023
        - Anos Finais (6º-9º)
        - 78 municípios ES
        - 4 datasets integrados
        """
        )

    with tech_col2:
        st.markdown(
            """
        **💻 Tecnologias**
        - Python 3.8+
        - Streamlit
        - Plotly
        - Pandas
        """
        )

    with tech_col3:
        st.markdown(
            """
        **🌐 Deploy**
        - Streamlit Cloud
        - Acesso público
        - Atualização automática
        - Código fonte disponível
        """
        )

    # Rodapé da página inicial
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p><strong>Desenvolvido por:</strong> Almir Carletti Neto</p>
        <p><strong>Período:</strong> 2025 - Pós-graduação em Mineração de Dados</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
