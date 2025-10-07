import pandas as pd
import numpy as np

# ------------------------------
# 1. Caminho dos arquivos
# ------------------------------
file_ideb = "raw_data\divulgacao_anos_finais_municipios_2023\divulgacao_anos_finais_municipios_2023.xlsx"
file_microdados = (
    "raw_data/microdados_censo_escolar_2023/dados/microdados_ed_basica_2023.csv"
)
file_rendimento = "raw_data/tx_rend_municipios_2023/tx_rend_municipios_2023.xlsx"

# ------------------------------
# 2. Leitura dos dataframes
# ------------------------------
print("**********")
print("Lendo os DataFrames")

print("    DataFrame IDEB")
df_ideb = pd.read_excel(
    file_ideb,
    dtype=object,
    skiprows=9,
    sheet_name="IDEB_AF_MUNICÍPIOS",
    usecols=[
        "SG_UF",
        "CO_MUNICIPIO",
        "NO_MUNICIPIO",
        "VL_OBSERVADO_2023",
        "VL_PROJECAO_2021",
        "REDE",
    ],
)

print("    DataFrame Microdados")
df_microdados = pd.read_csv(
    file_microdados,
    dtype=object,
    encoding="latin1",
    sep=";",
    usecols=[
        "NU_ANO_CENSO",
        "SG_UF",
        "CO_MUNICIPIO",
        "NO_MUNICIPIO",
        "QT_MAT_FUND_AF_6",
        "QT_MAT_FUND_AF_7",
        "QT_MAT_FUND_AF_8",
        "QT_MAT_FUND_AF_9",
        "TP_DEPENDENCIA",
    ],
)

print("    DataFrame Rendimento")
df_rendimento = pd.read_excel(
    file_rendimento,
    dtype=object,
    skiprows=8,
    sheet_name="MUNICIPIOS ",
    usecols=[
        "NU_ANO_CENSO",
        "SG_UF",
        "CO_MUNICIPIO",
        "NO_MUNICIPIO",
        "NO_DEPENDENCIA",
        "NO_CATEGORIA",
        "1_CAT_FUN_06",
        "1_CAT_FUN_07",
        "1_CAT_FUN_08",
        "1_CAT_FUN_09",
        "2_CAT_FUN_06",
        "2_CAT_FUN_07",
        "2_CAT_FUN_08",
        "2_CAT_FUN_09",
        "3_CAT_FUN_06",
        "3_CAT_FUN_07",
        "3_CAT_FUN_08",
        "3_CAT_FUN_09",
    ],
)

# ------------------------------
# 3. Conversão de tipos
# ------------------------------
print("\n**********")
print("Convertendo Tipos")

# Matrículas
for c in [
    "QT_MAT_FUND_AF_6",
    "QT_MAT_FUND_AF_7",
    "QT_MAT_FUND_AF_8",
    "QT_MAT_FUND_AF_9",
]:
    df_microdados[c] = (
        pd.to_numeric(df_microdados[c], errors="coerce").fillna(0).astype(int)
    )

# IDEB
for c in ["VL_OBSERVADO_2023", "VL_PROJECAO_2021"]:
    df_ideb[c] = pd.to_numeric(df_ideb[c].replace("-", np.nan), errors="coerce")

# Taxas (transforma em decimal: 98.4 -> 0.984)
taxa_cols = [
    "1_CAT_FUN_06",
    "1_CAT_FUN_07",
    "1_CAT_FUN_08",
    "1_CAT_FUN_09",
    "2_CAT_FUN_06",
    "2_CAT_FUN_07",
    "2_CAT_FUN_08",
    "2_CAT_FUN_09",
    "3_CAT_FUN_06",
    "3_CAT_FUN_07",
    "3_CAT_FUN_08",
    "3_CAT_FUN_09",
]
for c in taxa_cols:
    df_rendimento[c] = pd.to_numeric(df_rendimento[c], errors="coerce") / 100.0

# ------------------------------
# 4. Filtrar apenas ES e redes válidas
# ------------------------------
print("\n**********")
print("Filtrando Dados")

# IDEB
df_ideb_es = df_ideb[df_ideb["SG_UF"] == "ES"].copy()
df_ideb_es = df_ideb_es[df_ideb_es["REDE"] != "Pública"]

df_ideb_es["acima_meta"] = (
    df_ideb_es["VL_OBSERVADO_2023"] >= df_ideb_es["VL_PROJECAO_2021"]
).astype(bool)

# Microdados
df_micro_es = df_microdados[df_microdados["SG_UF"] == "ES"].copy()
df_micro_es = df_micro_es[~df_micro_es["TP_DEPENDENCIA"].isin(["1", "4"])]

# Rendimento
df_rend_es = df_rendimento[df_rendimento["SG_UF"] == "ES"].copy()
df_rend_es = df_rend_es[
    df_rend_es["NO_DEPENDENCIA"].isin(["Estadual", "Municipal"])
    & (df_rend_es["NO_CATEGORIA"] == "Total")
].copy()
df_rend_es = df_rend_es.rename(columns={"NO_DEPENDENCIA": "REDE"})

# ------------------------------
# 5. NOVA ESTRUTURA: Transformar para linha por município+rede+ano
# ------------------------------
print("\n**********")
print("Reestruturando dados por ano escolar")

# 5.1 Criar base dos microdados por ano
print("  Transformando microdados...")
df_micro_melted = []

# Agregar matrículas por município+rede primeiro
agg = (
    df_micro_es.groupby(["CO_MUNICIPIO", "TP_DEPENDENCIA"])
    .agg(
        {
            "QT_MAT_FUND_AF_6": "sum",
            "QT_MAT_FUND_AF_7": "sum",
            "QT_MAT_FUND_AF_8": "sum",
            "QT_MAT_FUND_AF_9": "sum",
        }
    )
    .reset_index()
)

keys = df_micro_es.drop_duplicates(["CO_MUNICIPIO", "TP_DEPENDENCIA"])[
    ["CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF", "TP_DEPENDENCIA"]
]

df_micro_base = keys.merge(agg, on=["CO_MUNICIPIO", "TP_DEPENDENCIA"], how="right")
df_micro_base["REDE"] = np.where(
    df_micro_base["TP_DEPENDENCIA"] == "2", "Estadual", "Municipal"
)

for ano in [6, 7, 8, 9]:
    df_ano = df_micro_base[["CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF", "REDE"]].copy()
    df_ano["ANO_ESCOLAR"] = ano
    df_ano["QT_MATRICULAS"] = df_micro_base[f"QT_MAT_FUND_AF_{ano}"]
    df_micro_melted.append(df_ano)

df_micro_final = pd.concat(df_micro_melted, ignore_index=True)

print("  Processando taxas de rendimento...")
df_rates_melted = []

for ano in [6, 7, 8, 9]:
    df_ano_rates = df_rend_es[["CO_MUNICIPIO", "REDE"]].copy()
    df_ano_rates["ANO_ESCOLAR"] = ano
    df_ano_rates["TAXA_EVASAO"] = df_rend_es[f"3_CAT_FUN_0{ano}"]
    df_ano_rates["TAXA_APROVACAO"] = df_rend_es[f"1_CAT_FUN_0{ano}"]
    df_ano_rates["TAXA_REPROVACAO"] = df_rend_es[f"2_CAT_FUN_0{ano}"]
    df_rates_melted.append(df_ano_rates)

df_rates_final = pd.concat(df_rates_melted, ignore_index=True)

print("  Processando IDEB...")
print(
    "  ATENÇÃO: IDEB original é agregado dos anos finais - repetindo valor para todas as séries"
)
df_ideb_melted = []

for ano in [6, 7, 8, 9]:
    df_ano_ideb = df_ideb_es[["CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF", "REDE"]].copy()
    df_ano_ideb["ANO_ESCOLAR"] = ano

    df_ano_ideb["VL_OBSERVADO_2023"] = df_ideb_es["VL_OBSERVADO_2023"]
    df_ano_ideb["VL_PROJECAO_2021"] = df_ideb_es["VL_PROJECAO_2021"]
    df_ano_ideb["acima_meta"] = df_ideb_es["acima_meta"]

    df_ideb_melted.append(df_ano_ideb)

df_ideb_final = pd.concat(df_ideb_melted, ignore_index=True)

# ------------------------------
# 6. Merge dos dados por município+rede+ano
# ------------------------------
print("\n**********")
print("Fazendo merge dos dados por município+rede+ano")

# Padronizar tipos
df_micro_final["CO_MUNICIPIO"] = df_micro_final["CO_MUNICIPIO"].astype(str)
df_rates_final["CO_MUNICIPIO"] = df_rates_final["CO_MUNICIPIO"].astype(str)
df_ideb_final["CO_MUNICIPIO"] = df_ideb_final["CO_MUNICIPIO"].astype(str)

# Merge microdados + taxas de rendimento
df_consolidado = df_micro_final.merge(
    df_rates_final, on=["CO_MUNICIPIO", "REDE", "ANO_ESCOLAR"], how="left"
)

# Merge com IDEB
df_consolidado = df_consolidado.merge(
    df_ideb_final[
        [
            "CO_MUNICIPIO",
            "REDE",
            "ANO_ESCOLAR",
            "VL_OBSERVADO_2023",
            "VL_PROJECAO_2021",
            "acima_meta",
        ]
    ],
    on=["CO_MUNICIPIO", "REDE", "ANO_ESCOLAR"],
    how="left",
)

# ------------------------------
# 7. Calcular KPIs por série
# ------------------------------
print("\n**********")
print("Calculando KPIs por série")

# Só calcular se temos matrícula e taxa
df_consolidado["EVASAO_ABSOLUTA"] = (
    df_consolidado["QT_MATRICULAS"] * df_consolidado["TAXA_EVASAO"]
)
df_consolidado["APROVADOS_ABSOLUTOS"] = (
    df_consolidado["QT_MATRICULAS"] * df_consolidado["TAXA_APROVACAO"]
)
df_consolidado["REPROVADOS_ABSOLUTOS"] = (
    df_consolidado["QT_MATRICULAS"] * df_consolidado["TAXA_REPROVACAO"]
)

# Tratar valores NaN
df_consolidado["EVASAO_ABSOLUTA"] = df_consolidado["EVASAO_ABSOLUTA"].fillna(0)
df_consolidado["APROVADOS_ABSOLUTOS"] = df_consolidado["APROVADOS_ABSOLUTOS"].fillna(0)
df_consolidado["REPROVADOS_ABSOLUTOS"] = df_consolidado["REPROVADOS_ABSOLUTOS"].fillna(
    0
)

# ------------------------------
# 8. Verificação e limpeza
# ------------------------------
print("\n**********")
print("Verificação dos dados")

print(f"Total de registros: {len(df_consolidado)}")
print(f"Municípios únicos: {df_consolidado['NO_MUNICIPIO'].nunique()}")
print(f"Redes: {df_consolidado['REDE'].unique()}")
print(f"Anos escolares: {sorted(df_consolidado['ANO_ESCOLAR'].unique())}")

# Verificar registros sem matrícula
sem_matricula = df_consolidado[df_consolidado["QT_MATRICULAS"] == 0]
print(f"Registros sem matrícula: {len(sem_matricula)}")

# Verificar registros sem taxa de rendimento
sem_taxa = df_consolidado[df_consolidado["TAXA_APROVACAO"].isna()]
print(f"Registros sem taxa de rendimento: {len(sem_taxa)}")

# ------------------------------
# 9. Salvamento final
# ------------------------------
print("\n**********")
print("Salvando arquivos finais")

# Reordenar colunas
colunas_finais = [
    "CO_MUNICIPIO",
    "NO_MUNICIPIO",
    "SG_UF",
    "REDE",
    "ANO_ESCOLAR",
    "QT_MATRICULAS",
    "TAXA_EVASAO",
    "TAXA_APROVACAO",
    "TAXA_REPROVACAO",
    "EVASAO_ABSOLUTA",
    "APROVADOS_ABSOLUTOS",
    "REPROVADOS_ABSOLUTOS",
]

df_final = (
    df_consolidado[colunas_finais]
    .sort_values(["NO_MUNICIPIO", "REDE", "ANO_ESCOLAR"])
    .reset_index(drop=True)
)

# Salvar arquivo principal
df_final.to_csv(
    "power-bi/data/dados_por_serie.csv", index=False, sep=";", encoding="utf-8"
)

# Manter compatibilidade com arquivos antigos (agregados)
df_micro_final.to_csv(
    "power-bi/data/microdados_final.csv", index=False, sep=";", encoding="utf-8"
)
df_ideb_es.to_csv(
    "power-bi/data/ideb_final.csv", index=False, sep=";", encoding="utf-8"
)

# Testes locais
df_final.to_excel("raw_data/tests/dados_por_serie.xlsx", index=False)

print(f"\n✅ Processamento concluído!")
print(f"📊 Novo arquivo criado: dados_por_serie.csv")
print(f"📋 Estrutura: {len(df_final)} linhas (município + rede + ano escolar)")
print(f"🔍 Colunas: {', '.join(colunas_finais)}")
