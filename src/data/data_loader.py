"""
Módulo para carregamento e processamento dos dados educacionais.
"""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Dict, Optional


class DataLoader:
    """Classe responsável pelo carregamento e processamento dos dados."""

    def __init__(self, data_path: str = "database"):
        """
        Inicializa o carregador de dados.

        Args:
            data_path: Caminho para a pasta com os dados CSV
        """
        self.data_path = Path(data_path)
        self._data_cache: Dict[str, pd.DataFrame] = {}

    @st.cache_data
    def load_ideb_data(_self) -> pd.DataFrame:
        """Carrega dados do IDEB."""
        return pd.read_csv(_self.data_path / "ideb_final.csv", sep=";")

    @st.cache_data
    def load_microdados(_self) -> pd.DataFrame:
        """Carrega microdados de matrículas."""
        return pd.read_csv(_self.data_path / "microdados_final.csv", sep=";")

    @st.cache_data
    def load_dados_serie(_self) -> pd.DataFrame:
        """Carrega dados por série com taxas de rendimento."""
        return pd.read_csv(_self.data_path / "dados_por_serie.csv", sep=";")

    @st.cache_data
    def load_cities(_self) -> pd.DataFrame:
        """Carrega dados de cidades e SREs."""
        return pd.read_csv(_self.data_path / "cities.csv")

    def get_summary_stats(self) -> Dict:
        """Retorna estatísticas resumidas dos dados."""
        ideb_df = self.load_ideb_data()
        microdados_df = self.load_microdados()
        dados_serie_df = self.load_dados_serie()
        cities_df = self.load_cities()

        return {
            "total_municipios": len(cities_df),
            "total_registros_ideb": len(ideb_df),
            "municipios_acima_meta": len(ideb_df[ideb_df["acima_meta"] == True]),
            "total_matriculas": microdados_df["QT_MATRICULAS"].sum(),
            "taxa_aprovacao_media": dados_serie_df["TAXA_APROVACAO"].mean(),
            "taxa_evasao_media": dados_serie_df["TAXA_EVASAO"].mean(),
            "redes_analisadas": sorted(ideb_df["REDE"].unique().tolist()),
        }

    def get_municipios_list(self) -> list:
        """Retorna lista de municípios únicos."""
        cities_df = self.load_cities()
        return sorted(cities_df["municipio"].unique().tolist())

    def get_sre_list(self) -> list:
        """Retorna lista de SREs únicas."""
        cities_df = self.load_cities()
        return sorted(cities_df["sre"].unique().tolist())

    def filter_data_by_municipio(self, municipio: str) -> Dict[str, pd.DataFrame]:
        """Filtra todos os dados por município específico."""
        cities_df = self.load_cities()
        municipio_code = cities_df[cities_df["municipio"] == municipio][
            "ibge_code"
        ].iloc[0]

        return {
            "ideb": self.load_ideb_data()[
                self.load_ideb_data()["CO_MUNICIPIO"] == municipio_code
            ],
            "microdados": self.load_microdados()[
                self.load_microdados()["CO_MUNICIPIO"] == municipio_code
            ],
            "dados_serie": self.load_dados_serie()[
                self.load_dados_serie()["CO_MUNICIPIO"] == municipio_code
            ],
        }
