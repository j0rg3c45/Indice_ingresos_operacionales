# -*- coding: utf-8 -*-
"""
=============================================================================
ANALISIS EXPLORATORIO - Registro Mercantil 2025
=============================================================================
Objetivo: Identificar datos relevantes, generar graficos basicos y reportar
valores unicos y repetidos de cada columna.

Columnas esperadas (segun diccionario):
  1. CIIU
  2. Tamano
  3. Empleo
  4. Direccion
  5. Estado (activa)
  6. Nueva/Renovada
  7. Comuna
  8. Barrio
  9. Fecha inscripcion
  10. Ingresos operacionales

Ejecucion:
  uv run notebooks_py/01_analisis_exploratorio.py

=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para generar graficos sin bloquear
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("Set2")


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def formato_abreviado(x, pos):
    """Formatea numeros grandes en ejes: 1M, 500K, etc."""
    if abs(x) >= 1_000_000_000:
        return f"{x / 1_000_000_000:.1f}B"
    elif abs(x) >= 1_000_000:
        return f"{x / 1_000_000:.1f}M"
    elif abs(x) >= 1_000:
        return f"{x / 1_000:.0f}K"
    else:
        return f"{x:.0f}"


def aplicar_formato_eje(ax, eje="y"):
    """Aplica formato abreviado a un eje."""
    formatter = mticker.FuncFormatter(formato_abreviado)
    if eje == "y":
        ax.yaxis.set_major_formatter(formatter)
    elif eje == "x":
        ax.xaxis.set_major_formatter(formatter)
    elif eje == "ambos":
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_formatter(formatter)


def formato_valor_etiqueta(v):
    """Formatea un valor numerico para etiquetas en barras."""
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    elif abs(v) >= 1_000:
        return f"{v / 1_000:.0f}K"
    else:
        return f"{v:,.0f}"


# =============================================================================
# 1. CONFIGURACION DE RUTAS
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ARCHIVO_EXCEL = DATA_DIR / "Registro mercantil 2025_.xlsx"
ARCHIVO_REPORTE = OUTPUT_DIR / "reporte_analisis_exploratorio.txt"

# =============================================================================
# 2. CARGA DE DATOS
# =============================================================================
print("=" * 70)
print("CARGA DE DATOS")
print("=" * 70)

df = pd.read_excel(ARCHIVO_EXCEL, engine="openpyxl")

# Normalizar nombres de columnas (minusculas, sin espacios extra)
df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

print(f"\n[OK] Archivo cargado: {ARCHIVO_EXCEL.name}")
print(f"  Filas: {df.shape[0]:,}")
print(f"  Columnas: {df.shape[1]}")
print(f"\n  Nombres de columnas:")
for i, col in enumerate(df.columns, 1):
    print(f"    {i:2d}. {col}")

# =============================================================================
# 3. INFORMACION GENERAL DEL DATASET
# =============================================================================
print("\n" + "=" * 70)
print("INFORMACION GENERAL")
print("=" * 70)

print("\n--- Tipos de datos ---")
print(df.dtypes.to_string())

print("\n--- Primeras 5 filas ---")
print(df.head().to_string())

print("\n--- Estadisticas descriptivas (numericas) ---")
print(df.describe().to_string())

print("\n--- Estadisticas descriptivas (categoricas) ---")
categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()
if categoricas:
    print(df[categoricas].describe().to_string())

# =============================================================================
# 4. REPORTE DE VALORES NULOS
# =============================================================================
print("\n" + "=" * 70)
print("REPORTE DE VALORES NULOS")
print("=" * 70)

nulos = df.isnull().sum()
pct_nulos = (df.isnull().sum() / len(df) * 100).round(2)
reporte_nulos = pd.DataFrame({"nulos": nulos, "porcentaje_%": pct_nulos})
reporte_nulos = reporte_nulos[reporte_nulos["nulos"] > 0].sort_values("nulos", ascending=False)

if reporte_nulos.empty:
    print("\n[OK] No hay valores nulos en el dataset.")
else:
    print(f"\n[!] Columnas con valores nulos ({len(reporte_nulos)}):")
    print(reporte_nulos.to_string())

# =============================================================================
# 5. REPORTE DE VALORES UNICOS Y REPETIDOS
# =============================================================================
print("\n" + "=" * 70)
print("REPORTE DE VALORES UNICOS Y REPETIDOS")
print("=" * 70)

reporte_unicos = []

for col in df.columns:
    total = df[col].count()
    unicos = df[col].nunique()
    repetidos = total - unicos
    valor_mas_frecuente = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
    frecuencia_max = df[col].value_counts().iloc[0] if total > 0 else 0

    reporte_unicos.append({
        "columna": col,
        "total_no_nulos": total,
        "valores_unicos": unicos,
        "valores_repetidos": repetidos,
        "pct_unicos": round(unicos / total * 100, 2) if total > 0 else 0,
        "valor_mas_frecuente": valor_mas_frecuente,
        "frecuencia_max": frecuencia_max,
    })

df_unicos = pd.DataFrame(reporte_unicos)
print("\n")
print(df_unicos.to_string(index=False))

# Detalle de valores unicos por columna categorica
print("\n\n--- Detalle: Top 15 valores por columna categorica ---")
for col in categoricas:
    print(f"\n  [{col.upper()}] ({df[col].nunique()} valores unicos)")
    top = df[col].value_counts().head(15)
    for valor, cuenta in top.items():
        print(f"    {valor}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)")

# =============================================================================
# 6. REPORTE DE DUPLICADOS
# =============================================================================
print("\n" + "=" * 70)
print("REPORTE DE FILAS DUPLICADAS")
print("=" * 70)

duplicados = df.duplicated().sum()
print(f"\n  Filas duplicadas exactas: {duplicados:,} ({duplicados/len(df)*100:.2f}%)")

# =============================================================================
# 7. GRAFICOS BASICOS (con formato abreviado en ejes)
# =============================================================================
print("\n" + "=" * 70)
print("GENERANDO GRAFICOS...")
print("=" * 70)


def guardar_grafico(fig, nombre):
    """Guarda el grafico como PNG en outputs/."""
    ruta = OUTPUT_DIR / f"{nombre}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [OK] Guardado: {ruta.name}")


# --- 7.1 Distribucion de Ingresos Operacionales ---
col_ingresos = [c for c in df.columns if "ingreso" in c]
if col_ingresos:
    col_ing = col_ingresos[0]
    datos_ing = pd.to_numeric(df[col_ing], errors="coerce").dropna()

    if len(datos_ing) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("Distribucion de Ingresos Operacionales", fontsize=14, fontweight="bold")

        # Histograma
        axes[0].hist(datos_ing, bins=50, edgecolor="white", alpha=0.8)
        axes[0].set_xlabel("Ingresos Operacionales")
        axes[0].set_ylabel("Frecuencia")
        axes[0].set_title("Histograma")
        aplicar_formato_eje(axes[0], "x")
        aplicar_formato_eje(axes[0], "y")

        # Boxplot
        axes[1].boxplot(datos_ing, vert=True)
        axes[1].set_ylabel("Ingresos Operacionales")
        axes[1].set_title("Boxplot")
        aplicar_formato_eje(axes[1], "y")

        plt.tight_layout()
        guardar_grafico(fig, "01_distribucion_ingresos")

        # Log-scale para mejor visualizacion
        datos_positivos = datos_ing[datos_ing > 0]
        if len(datos_positivos) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(np.log10(datos_positivos), bins=50, edgecolor="white", alpha=0.8, color="teal")
            ax.set_xlabel("Log10(Ingresos Operacionales)")
            ax.set_ylabel("Frecuencia")
            ax.set_title("Distribucion de Ingresos (escala logaritmica)")
            aplicar_formato_eje(ax, "y")
            plt.tight_layout()
            guardar_grafico(fig, "02_distribucion_ingresos_log")

# --- 7.2 Distribucion por Tamano de empresa ---
col_tamano = [c for c in df.columns if "tama" in c]
if col_tamano:
    col_tam = col_tamano[0]
    conteo_tam = df[col_tam].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    conteo_tam.plot(kind="bar", ax=ax, edgecolor="white")
    ax.set_title("Distribucion por Tamano de Empresa", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tamano")
    ax.set_ylabel("Cantidad de empresas")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    aplicar_formato_eje(ax, "y")
    for i, v in enumerate(conteo_tam.values):
        ax.text(i, v + len(df) * 0.005, formato_valor_etiqueta(v), ha="center", fontsize=9)
    plt.tight_layout()
    guardar_grafico(fig, "03_distribucion_tamano")

# --- 7.3 Distribucion por Estado ---
col_estado = [c for c in df.columns if "estado" in c]
if col_estado:
    col_est = col_estado[0]
    conteo_est = df[col_est].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(conteo_est, labels=conteo_est.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribucion por Estado", fontsize=13, fontweight="bold")
    plt.tight_layout()
    guardar_grafico(fig, "04_distribucion_estado")

# --- 7.4 Tipo de Registro (Mercantil vs ESAL) ---
col_tipo_reg = [c for c in df.columns if "tipo_registro" in c]
if col_tipo_reg:
    col_tr = col_tipo_reg[0]
    conteo_tr = df[col_tr].value_counts()

    fig, ax = plt.subplots(figsize=(7, 6))
    colores = ["#3498db", "#e74c3c"]
    wedges, texts, autotexts = ax.pie(
        conteo_tr,
        labels=conteo_tr.index,
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*len(df)):,})",
        startangle=90,
        colors=colores,
        textprops={"fontsize": 11},
    )
    ax.set_title("Tipo de Registro", fontsize=13, fontweight="bold")
    plt.tight_layout()
    guardar_grafico(fig, "05_tipo_registro")

# --- 7.5 Categoria (Persona Natural / Juridica) ---
col_categoria = [c for c in df.columns if "categoria" in c]
if col_categoria:
    col_cat = col_categoria[0]
    conteo_cat = df[col_cat].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.barh(conteo_cat.index, conteo_cat.values, color=["#2ecc71", "#9b59b6", "#f39c12"], edgecolor="white")
    ax.set_title("Distribucion por Categoria", fontsize=13, fontweight="bold")
    ax.set_xlabel("Cantidad de empresas")
    aplicar_formato_eje(ax, "x")
    for i, v in enumerate(conteo_cat.values):
        ax.text(v + len(df) * 0.005, i, f"{formato_valor_etiqueta(v)} ({v/len(df)*100:.1f}%)", va="center", fontsize=10)
    plt.tight_layout()
    guardar_grafico(fig, "06_categoria")

# --- 7.5 Top 15 Comunas ---
col_comuna = [c for c in df.columns if "comuna" in c]
if col_comuna:
    col_com = col_comuna[0]
    top_comunas = df[col_com].value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    top_comunas.plot(kind="barh", ax=ax, edgecolor="white")
    ax.set_title("Top 15 Comunas con mas empresas", fontsize=13, fontweight="bold")
    ax.set_xlabel("Cantidad de empresas")
    ax.set_ylabel("Comuna")
    aplicar_formato_eje(ax, "x")
    ax.invert_yaxis()
    plt.tight_layout()
    guardar_grafico(fig, "06_top_comunas")

# --- 7.6 Top 15 CIIU ---
col_ciiu = [c for c in df.columns if "ciiu" in c]
if col_ciiu:
    col_ci = col_ciiu[0]
    top_ciiu = df[col_ci].value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    top_ciiu.plot(kind="barh", ax=ax, edgecolor="white", color="coral")
    ax.set_title("Top 15 Actividades Economicas (CIIU)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Cantidad de empresas")
    ax.set_ylabel("Codigo CIIU")
    aplicar_formato_eje(ax, "x")
    ax.invert_yaxis()
    plt.tight_layout()
    guardar_grafico(fig, "07_top_ciiu")

# --- 7.7 Empleo ---
col_empleo = [c for c in df.columns if "empleo" in c]
if col_empleo:
    col_emp = col_empleo[0]
    datos_emp = pd.to_numeric(df[col_emp], errors="coerce").dropna()

    if len(datos_emp) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("Distribucion de Empleo", fontsize=14, fontweight="bold")

        axes[0].hist(datos_emp, bins=50, edgecolor="white", alpha=0.8, color="mediumpurple")
        axes[0].set_xlabel("Numero de empleados")
        axes[0].set_ylabel("Frecuencia")
        axes[0].set_title("Histograma")
        aplicar_formato_eje(axes[0], "x")
        aplicar_formato_eje(axes[0], "y")

        axes[1].boxplot(datos_emp, vert=True)
        axes[1].set_ylabel("Numero de empleados")
        axes[1].set_title("Boxplot")
        aplicar_formato_eje(axes[1], "y")

        plt.tight_layout()
        guardar_grafico(fig, "08_distribucion_empleo")

# --- 7.8 Ingresos por Tamano (boxplot comparativo) ---
if col_ingresos and col_tamano:
    df_temp = df[[col_ing, col_tam]].copy()
    df_temp[col_ing] = pd.to_numeric(df_temp[col_ing], errors="coerce")
    df_temp = df_temp.dropna()

    if len(df_temp) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        df_temp.boxplot(column=col_ing, by=col_tam, ax=ax)
        ax.set_title("Ingresos Operacionales por Tamano de Empresa", fontsize=13, fontweight="bold")
        ax.set_xlabel("Tamano")
        ax.set_ylabel("Ingresos Operacionales")
        aplicar_formato_eje(ax, "y")
        plt.suptitle("")
        plt.tight_layout()
        guardar_grafico(fig, "09_ingresos_por_tamano")

# --- 7.9 Mapa de correlacion (variables numericas) ---
numericas = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numericas) >= 2:
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[numericas].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, ax=ax, fmt=".2f")
    ax.set_title("Matriz de Correlacion", fontsize=13, fontweight="bold")
    plt.tight_layout()
    guardar_grafico(fig, "10_correlacion")

# --- 7.10 Valores nulos por columna (grafico) ---
if not reporte_nulos.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    reporte_nulos["porcentaje_%"].plot(kind="barh", ax=ax, color="salmon", edgecolor="white")
    ax.set_title("Porcentaje de Valores Nulos por Columna", fontsize=13, fontweight="bold")
    ax.set_xlabel("% Nulos")
    ax.invert_yaxis()
    plt.tight_layout()
    guardar_grafico(fig, "11_valores_nulos")

# =============================================================================
# 8. GENERAR REPORTE .TXT EN OUTPUTS
# =============================================================================
print("\n" + "=" * 70)
print("GENERANDO REPORTE .TXT...")
print("=" * 70)

with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("REPORTE DE ANALISIS EXPLORATORIO - Registro Mercantil 2025\n")
    f.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 70 + "\n\n")

    # Info general
    f.write("-" * 70 + "\n")
    f.write("1. INFORMACION GENERAL\n")
    f.write("-" * 70 + "\n")
    f.write(f"  Archivo fuente: {ARCHIVO_EXCEL.name}\n")
    f.write(f"  Total de filas: {len(df):,}\n")
    f.write(f"  Total de columnas: {len(df.columns)}\n")
    f.write(f"  Columnas numericas: {len(numericas)}\n")
    f.write(f"  Columnas categoricas: {len(categoricas)}\n")
    f.write(f"  Filas duplicadas: {duplicados:,}\n\n")

    f.write("  Columnas:\n")
    for i, col in enumerate(df.columns, 1):
        f.write(f"    {i:2d}. {col} ({df[col].dtype})\n")
    f.write("\n")

    # Estadisticas descriptivas
    f.write("-" * 70 + "\n")
    f.write("2. ESTADISTICAS DESCRIPTIVAS (NUMERICAS)\n")
    f.write("-" * 70 + "\n")
    f.write(df.describe().to_string() + "\n\n")

    if categoricas:
        f.write("-" * 70 + "\n")
        f.write("3. ESTADISTICAS DESCRIPTIVAS (CATEGORICAS)\n")
        f.write("-" * 70 + "\n")
        f.write(df[categoricas].describe().to_string() + "\n\n")

    # Valores nulos
    f.write("-" * 70 + "\n")
    f.write("4. VALORES NULOS\n")
    f.write("-" * 70 + "\n")
    if reporte_nulos.empty:
        f.write("  No hay valores nulos en el dataset.\n\n")
    else:
        f.write(reporte_nulos.to_string() + "\n\n")

    # Valores unicos y repetidos
    f.write("-" * 70 + "\n")
    f.write("5. VALORES UNICOS Y REPETIDOS POR COLUMNA\n")
    f.write("-" * 70 + "\n")
    f.write(df_unicos.to_string(index=False) + "\n\n")

    # Detalle categoricas
    f.write("-" * 70 + "\n")
    f.write("6. TOP 15 VALORES POR COLUMNA CATEGORICA\n")
    f.write("-" * 70 + "\n")
    for col in categoricas:
        f.write(f"\n  [{col.upper()}] ({df[col].nunique()} valores unicos)\n")
        top = df[col].value_counts().head(15)
        for valor, cuenta in top.items():
            f.write(f"    {valor}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
    f.write("\n")

    # Duplicados
    f.write("-" * 70 + "\n")
    f.write("7. FILAS DUPLICADAS\n")
    f.write("-" * 70 + "\n")
    f.write(f"  Filas duplicadas exactas: {duplicados:,} ({duplicados/len(df)*100:.2f}%)\n\n")

    # Resumen
    f.write("=" * 70 + "\n")
    f.write("RESUMEN\n")
    f.write("=" * 70 + "\n")
    f.write(f"  Total de registros:    {len(df):,}\n")
    f.write(f"  Total de columnas:     {len(df.columns)}\n")
    f.write(f"  Columnas numericas:    {len(numericas)}\n")
    f.write(f"  Columnas categoricas:  {len(categoricas)}\n")
    f.write(f"  Filas duplicadas:      {duplicados:,}\n")
    f.write(f"  Columnas con nulos:    {len(reporte_nulos)}\n")
    f.write("=" * 70 + "\n")

print(f"  [OK] Reporte guardado: {ARCHIVO_REPORTE.name}")

# =============================================================================
# 8B. GENERAR REPORTE CONSOLIDADO EN OUTPUTS
# =============================================================================
print("\n" + "=" * 70)
print("GENERANDO REPORTE CONSOLIDADO...")
print("=" * 70)

ARCHIVO_CONSOLIDADO = OUTPUT_DIR / "consolidado.txt"

# Identificar columnas clave
col_comuna = [c for c in df.columns if "comuna" in c]
col_ingresos = [c for c in df.columns if "ingreso" in c]
col_empleo = [c for c in df.columns if "personal" in c]
col_tamano = [c for c in df.columns if "tama" in c]
col_ciiu_cod = [c for c in df.columns if "codigo" in c and "ciiu" in c]
col_ciiu_desc = [c for c in df.columns if "desc" in c and "ciiu" in c]
col_sector = [c for c in df.columns if "sector" in c]
col_categoria = [c for c in df.columns if "categoria" in c]
col_tipo_reg = [c for c in df.columns if "tipo_registro" in c]

with open(ARCHIVO_CONSOLIDADO, "w", encoding="utf-8") as f:
    f.write("=" * 100 + "\n")
    f.write("REPORTE CONSOLIDADO - INDICE DE INGRESOS OPERACIONALES\n")
    f.write("Registro Mercantil 2025 - Santiago de Cali\n")
    f.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 100 + "\n\n")

    # 1. Info general
    f.write("-" * 100 + "\n")
    f.write("1. INFORMACION GENERAL DEL DATASET\n")
    f.write("-" * 100 + "\n")
    f.write(f"  Archivo fuente: {ARCHIVO_EXCEL.name}\n")
    f.write(f"  Total registros: {len(df):,}\n")
    f.write(f"  Total columnas: {len(df.columns)}\n")
    f.write(f"  Columnas numericas: {len(numericas)}\n")
    f.write(f"  Columnas categoricas: {len(categoricas)}\n")
    f.write(f"  Filas duplicadas: {duplicados:,}\n")
    if col_comuna:
        df_con_comuna = df[df[col_comuna[0]].notna()]
        f.write(f"  Registros con comuna: {len(df_con_comuna):,}\n")
        f.write(f"  Comunas distintas: {df[col_comuna[0]].nunique()}\n")
    f.write("\n")

    # 2. Indicadores por comuna
    if col_comuna and col_ingresos and col_empleo:
        c_com = col_comuna[0]
        c_ing = col_ingresos[0]
        c_emp = col_empleo[0]
        c_tam = col_tamano[0] if col_tamano else None
        c_ciiu = col_ciiu_cod[0] if col_ciiu_cod else None

        df[c_ing] = pd.to_numeric(df[c_ing], errors="coerce")
        df[c_emp] = pd.to_numeric(df[c_emp], errors="coerce")
        df_cc = df[df[c_com].notna()].copy()

        indicadores = df_cc.groupby(c_com).agg(
            total_empresas=(c_com, "size"),
            ingresos_promedio=(c_ing, "mean"),
            ingresos_total=(c_ing, "sum"),
            empleo_total=(c_emp, "sum"),
            empleo_promedio=(c_emp, "mean"),
        ).reset_index()

        if c_tam:
            micro = df_cc[df_cc[c_tam].str.contains("MICRO", case=False, na=False)]
            tasa_micro = micro.groupby(c_com).size().reset_index(name="n_micro")
            indicadores = indicadores.merge(tasa_micro, on=c_com, how="left")
            indicadores["pct_micro"] = (indicadores["n_micro"] / indicadores["total_empresas"] * 100).round(1)

        if c_ciiu:
            diversidad = df_cc.groupby(c_com)[c_ciiu].nunique().reset_index(name="n_ciiu")
            indicadores = indicadores.merge(diversidad, on=c_com, how="left")

        indicadores = indicadores.sort_values("total_empresas", ascending=False)

        f.write("-" * 100 + "\n")
        f.write("2. INDICADORES ECONOMICOS POR COMUNA\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Comuna':<12} {'Empresas':>9} {'Ing.Promedio':>14} {'Ing.Total':>14} {'Empleo':>8} {'Emp/Emp':>8}")
        if c_tam:
            f.write(f" {'% Micro':>8}")
        if c_ciiu:
            f.write(f" {'CIIU':>5}")
        f.write("\n")
        f.write("-" * 100 + "\n")

        for _, row in indicadores.iterrows():
            ing_p = f"${row['ingresos_promedio']/1e6:.1f}M" if pd.notna(row['ingresos_promedio']) and row['ingresos_promedio'] >= 1e6 else (f"${row['ingresos_promedio']/1e3:.0f}K" if pd.notna(row['ingresos_promedio']) and row['ingresos_promedio'] > 0 else "$0")
            ing_t = f"${row['ingresos_total']/1e9:.2f}B" if pd.notna(row['ingresos_total']) and abs(row['ingresos_total']) >= 1e9 else (f"${row['ingresos_total']/1e6:.0f}M" if pd.notna(row['ingresos_total']) else "N/A")
            emp_p = f"{row['empleo_promedio']:.1f}" if pd.notna(row['empleo_promedio']) else "N/A"
            line = f"{row[c_com]:<12} {int(row['total_empresas']):>9,} {ing_p:>14} {ing_t:>14} {int(row['empleo_total']):>8,} {emp_p:>8}"
            if c_tam:
                pct = f"{row['pct_micro']:.1f}%" if pd.notna(row.get('pct_micro')) else "N/A"
                line += f" {pct:>8}"
            if c_ciiu:
                ciiu_v = f"{int(row['n_ciiu'])}" if pd.notna(row.get('n_ciiu')) else "N/A"
                line += f" {ciiu_v:>5}"
            f.write(line + "\n")

        f.write("-" * 100 + "\n")
        f.write(f"TOTAL: {indicadores['total_empresas'].sum():,.0f} empresas | {indicadores['empleo_total'].sum():,.0f} empleos\n\n")

    # 3. Top sectores
    if col_sector:
        f.write("-" * 100 + "\n")
        f.write("3. TOP 10 SECTORES ECONOMICOS\n")
        f.write("-" * 100 + "\n")
        top_sect = df[col_sector[0]].value_counts().head(10)
        for sector, cuenta in top_sect.items():
            f.write(f"  {sector}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
        f.write("\n")

    # 4. Top CIIU
    if col_ciiu_desc:
        f.write("-" * 100 + "\n")
        f.write("4. TOP 15 ACTIVIDADES ECONOMICAS (CIIU)\n")
        f.write("-" * 100 + "\n")
        top_ciiu = df[col_ciiu_desc[0]].value_counts().head(15)
        for act, cuenta in top_ciiu.items():
            f.write(f"  {str(act)[:70]}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
        f.write("\n")

    # 5. Distribucion por tamano
    if col_tamano:
        f.write("-" * 100 + "\n")
        f.write("5. DISTRIBUCION POR TAMANO DE EMPRESA\n")
        f.write("-" * 100 + "\n")
        dist_tam = df[col_tamano[0]].value_counts()
        for tam, cuenta in dist_tam.items():
            f.write(f"  {tam}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
        f.write("\n")

    # 6. Distribucion por categoria
    if col_categoria:
        f.write("-" * 100 + "\n")
        f.write("6. DISTRIBUCION POR CATEGORIA\n")
        f.write("-" * 100 + "\n")
        dist_cat = df[col_categoria[0]].value_counts()
        for cat, cuenta in dist_cat.items():
            f.write(f"  {cat}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
        f.write("\n")

    # 7. Tipo de registro
    if col_tipo_reg:
        f.write("-" * 100 + "\n")
        f.write("7. TIPO DE REGISTRO\n")
        f.write("-" * 100 + "\n")
        dist_reg = df[col_tipo_reg[0]].value_counts()
        for reg, cuenta in dist_reg.items():
            f.write(f"  {reg}: {cuenta:,} ({cuenta/len(df)*100:.1f}%)\n")
        f.write("\n")

    # 8. Estadisticas de ingresos
    if col_ingresos:
        f.write("-" * 100 + "\n")
        f.write("8. RESUMEN ESTADISTICO DE INGRESOS OPERACIONALES\n")
        f.write("-" * 100 + "\n")
        ing_data = pd.to_numeric(df[col_ingresos[0]], errors="coerce").dropna()
        f.write(f"  Registros con dato: {len(ing_data):,} ({len(ing_data)/len(df)*100:.1f}%)\n")
        f.write(f"  Media:    ${ing_data.mean()/1e6:.1f}M\n")
        f.write(f"  Mediana:  ${ing_data.median()/1e6:.1f}M\n")
        f.write(f"  P25:      ${ing_data.quantile(0.25)/1e6:.1f}M\n")
        f.write(f"  P75:      ${ing_data.quantile(0.75)/1e6:.1f}M\n")
        f.write(f"  Maximo:   ${ing_data.max()/1e9:.2f}B\n")
        f.write(f"  Con ingresos > 0: {(ing_data > 0).sum():,}\n")
        f.write(f"  Con ingresos = 0: {(ing_data == 0).sum():,}\n\n")

    # 9. Estadisticas de empleo
    if col_empleo:
        f.write("-" * 100 + "\n")
        f.write("9. RESUMEN ESTADISTICO DE EMPLEO\n")
        f.write("-" * 100 + "\n")
        emp_data = pd.to_numeric(df[col_empleo[0]], errors="coerce").dropna()
        f.write(f"  Registros con dato: {len(emp_data):,}\n")
        f.write(f"  Media:    {emp_data.mean():.1f} empleados\n")
        f.write(f"  Mediana:  {emp_data.median():.0f} empleados\n")
        f.write(f"  Maximo:   {emp_data.max():,.0f} empleados\n")
        f.write(f"  Total:    {emp_data.sum():,.0f} empleados\n\n")

    # 10. Valores nulos
    f.write("-" * 100 + "\n")
    f.write("10. VALORES NULOS\n")
    f.write("-" * 100 + "\n")
    if reporte_nulos.empty:
        f.write("  No hay valores nulos.\n\n")
    else:
        f.write(reporte_nulos.to_string() + "\n\n")

    # Cierre
    f.write("=" * 100 + "\n")
    f.write("FIN DEL REPORTE CONSOLIDADO\n")
    f.write("=" * 100 + "\n")

print(f"  [OK] Consolidado guardado: {ARCHIVO_CONSOLIDADO.name}")

# =============================================================================
# 8C. GRAFICOS DE RESUMEN CONSOLIDADO
# =============================================================================
print("\n" + "=" * 70)
print("GENERANDO GRAFICOS DE RESUMEN...")
print("=" * 70)

if col_comuna and col_ingresos and col_empleo:
    # Grafico resumen: Top 15 comunas por empresas
    top15 = indicadores.head(15)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Resumen Consolidado - Indicadores por Comuna (Top 15)", fontsize=15, fontweight="bold")

    # 1. Total empresas
    axes[0, 0].barh(top15[c_com], top15["total_empresas"], color="#3498db", edgecolor="white")
    axes[0, 0].set_title("Total de Empresas")
    axes[0, 0].invert_yaxis()
    aplicar_formato_eje(axes[0, 0], "x")

    # 2. Ingresos promedio
    axes[0, 1].barh(top15[c_com], top15["ingresos_promedio"].fillna(0), color="#2ecc71", edgecolor="white")
    axes[0, 1].set_title("Ingresos Promedio")
    axes[0, 1].invert_yaxis()
    aplicar_formato_eje(axes[0, 1], "x")

    # 3. Empleo total
    axes[1, 0].barh(top15[c_com], top15["empleo_total"].fillna(0), color="#9b59b6", edgecolor="white")
    axes[1, 0].set_title("Empleo Total")
    axes[1, 0].invert_yaxis()
    aplicar_formato_eje(axes[1, 0], "x")

    # 4. Diversidad CIIU
    if c_ciiu and "n_ciiu" in top15.columns:
        axes[1, 1].barh(top15[c_com], top15["n_ciiu"].fillna(0), color="#e74c3c", edgecolor="white")
        axes[1, 1].set_title("Diversidad Economica (CIIU distintos)")
        axes[1, 1].invert_yaxis()
    else:
        axes[1, 1].text(0.5, 0.5, "Sin datos CIIU", ha="center", va="center", fontsize=12)
        axes[1, 1].set_axis_off()

    plt.tight_layout()
    guardar_grafico(fig, "12_resumen_consolidado_comunas")

    # Grafico de composicion: tamano de empresa
    if col_tamano:
        dist_tam = df[col_tamano[0]].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        colores = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#9b59b6"]
        wedges, texts, autotexts = ax.pie(
            dist_tam.values,
            labels=dist_tam.index,
            autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*len(df)):,})",
            colors=colores[:len(dist_tam)],
            textprops={"fontsize": 10},
        )
        ax.set_title("Composicion por Tamano de Empresa", fontsize=13, fontweight="bold")
        plt.tight_layout()
        guardar_grafico(fig, "13_composicion_tamano")

    # Grafico: Top 10 sectores
    if col_sector:
        top_sect = df[col_sector[0]].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(12, 6))
        labels_short = [s[:45] + "..." if len(s) > 45 else s for s in top_sect.index]
        ax.barh(labels_short, top_sect.values, color="#1abc9c", edgecolor="white")
        ax.set_title("Top 10 Sectores Economicos", fontsize=13, fontweight="bold")
        ax.set_xlabel("Cantidad de empresas")
        aplicar_formato_eje(ax, "x")
        ax.invert_yaxis()
        plt.tight_layout()
        guardar_grafico(fig, "14_top_sectores")

# =============================================================================
# 9. RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 70)
print("RESUMEN DEL ANALISIS")
print("=" * 70)
print(f"""
  Total de registros:        {len(df):,}
  Total de columnas:         {len(df.columns)}
  Columnas numericas:        {len(numericas)}
  Columnas categoricas:      {len(categoricas)}
  Filas duplicadas:          {duplicados:,}
  Columnas con nulos:        {len(reporte_nulos)}
  Reporte EDA:               {ARCHIVO_REPORTE.name}
  Reporte consolidado:       consolidado.txt
  Graficos PNG:              outputs/
""")

print("[OK] Analisis exploratorio completado exitosamente.")
