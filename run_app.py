"""
Script para executar o dashboard localmente.
"""

import subprocess
import sys
from pathlib import Path


def install_requirements():
    """Instala as dependências necessárias."""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def run_streamlit():
    """Executa o dashboard Streamlit."""
    print("🚀 Iniciando o dashboard...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o Streamlit: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Dashboard encerrado pelo usuário.")


def main():
    """Função principal."""
    print("=" * 60)
    print("📚 Dashboard de Indicadores Educacionais do Espírito Santo")
    print("=" * 60)

    # Verifica se os arquivos de dados existem
    data_files = [
        "database/ideb_final.csv",
        "database/microdados_final.csv",
        "database/dados_por_serie.csv",
        "database/cities.csv",
    ]

    missing_files = []
    for file_path in data_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Arquivos de dados não encontrados:")
        for file in missing_files:
            print(f"   • {file}")
        print("\n💡 Certifique-se de que os arquivos CSV estão na pasta 'database/'")
        return

    print("✅ Todos os arquivos de dados encontrados!")

    # Instala dependências e executa o app
    if install_requirements():
        print("\n" + "=" * 60)
        print("🌐 O dashboard será aberto em: http://localhost:8501")
        print("🛑 Para encerrar, pressione Ctrl+C")
        print("=" * 60)
        run_streamlit()


if __name__ == "__main__":
    main()
