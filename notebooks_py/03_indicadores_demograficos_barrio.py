# -*- coding: utf-8 -*-
"""
=============================================================================
INDICADORES DEMOGRAFICOS + ECONOMICOS POR BARRIO - Cali 2025
=============================================================================
Cruza el Registro Mercantil 2025 con el shapefile de Personas por Hogar
(Censo 2016) para generar indicadores territoriales relevantes.

Ejecucion:
  C:\\Users\\Jorge\\.venv\\Scripts\\python.exe notebooks_py/03_indicadores_demograficos_barrio.py

=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import geopandas as gpd
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")
plt.style.use("seaborn-v0_8-whitegrid")


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def formato_abreviado(x, pos):
    """
    Formatea numeros grandes para ejes de graficos.
    Convierte: 1000 -> 1K, 1000000 -> 1M, 1000000000 -> 1B
    Esto hace que los graficos sean mas faciles de leer cuando
    los valores son muy grandes.
    """
    if abs(x) >= 1_000_000_000:
        return f"{x / 1_000_000_000:.1f}B"
    elif abs(x) >= 1_000_000:
        return f"{x / 1_000_000:.1f}M"
    elif abs(x) >= 1_000:
        return f"{x / 1_000:.0f}K"
    else:
        return f"{x:.0f}"


def aplicar_formato_eje(ax, eje="y"):
    """Aplica formato abreviado a un eje del grafico."""
    formatter = mticker.FuncFormatter(formato_abreviado)
    if eje == "y":
        ax.yaxis.set_major_formatter(formatter)
    elif eje == "x":
        ax.xaxis.set_major_formatter(formatter)


# =============================================================================
# 1. CONFIGURACION DE RUTAS
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GEO_DIR = DATA_DIR / "info_geo"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ARCHIVO_EXCEL = DATA_DIR / "Registro mercantil 2025_.xlsx"

# =============================================================================
# 2. CARGA DE DATOS
# =============================================================================
print("=" * 70)
print("CARGA DE DATOS")
print("=" * 70)

# 2.1 Registro Mercantil
print("\n[1/2] Cargando Registro Mercantil...")
df = pd.read_excel(ARCHIVO_EXCEL, engine="openpyxl")
df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
print(f"  Registros: {len(df):,}")

# 2.2 Shapefile de Personas por Hogar
print("[2/2] Cargando shapefile Personas por Hogar...")
zip_files = [f for f in GEO_DIR.glob("*.zip") if "Personas" in f.name]

if not zip_files:
    print("  [!] No se encontro el ZIP de Personas por hogar")
    exit()

with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(zip_files[0], "r") as z:
        z.extractall(tmp)
    shp_files = list(Path(tmp).glob("**/*.shp"))
    gdf_barrios = gpd.read_file(shp_files[0])

# Normalizar CRS a WGS84
if gdf_barrios.crs and gdf_barrios.crs.to_epsg() != 4326:
    gdf_barrios = gdf_barrios.to_crs("EPSG:4326")

print(f"  Barrios: {len(gdf_barrios)}")
print(f"  CRS: {gdf_barrios.crs}")
print(f"  Columnas: {list(gdf_barrios.columns)}")

# =============================================================================
# 3. PREPARACION Y CRUCE DE DATOS
# =============================================================================
print("\n" + "=" * 70)
print("PREPARACION Y CRUCE DE DATOS")
print("=" * 70)

# Identificar columnas
col_barrio_rm = [c for c in df.columns if "barrio" in c][0]
col_comuna_rm = [c for c in df.columns if "comuna" in c][0]
col_ingresos = [c for c in df.columns if "ingreso" in c][0]
col_empleo = [c for c in df.columns if "personal" in c][0]
col_tamano = [c for c in df.columns if "tama" in c][0]

# Convertir a numerico
df[col_ingresos] = pd.to_numeric(df[col_ingresos], errors="coerce")
df[col_empleo] = pd.to_numeric(df[col_empleo], errors="coerce")

# Indicadores del Registro Mercantil por barrio
df_barrio = df[df[col_barrio_rm].notna()].copy()
print(f"\nRegistros con barrio: {len(df_barrio):,}")

ind_barrio = df_barrio.groupby(col_barrio_rm).agg(
    total_empresas=(col_barrio_rm, "size"),
    ingresos_promedio=(col_ingresos, "mean"),
    ingresos_total=(col_ingresos, "sum"),
    empleo_total=(col_empleo, "sum"),
).reset_index()

# Normalizar nombres para el cruce
# El shapefile tiene nombres como "Ciudadela Floralia", el RM como "Ciudadela Floralia"
ind_barrio["barrio_key"] = ind_barrio[col_barrio_rm].str.strip().str.title()
gdf_barrios["barrio_key"] = gdf_barrios["barrio"].str.strip().str.title()

# Merge
gdf_merged = gdf_barrios.merge(ind_barrio, on="barrio_key", how="left")
n_match = gdf_merged["total_empresas"].notna().sum()
print(f"Barrios cruzados: {n_match} de {len(gdf_merged)}")

# =============================================================================
# 4. CALCULO DE INDICADORES RELEVANTES
# =============================================================================
print("\n" + "=" * 70)
print("CALCULO DE INDICADORES")
print("=" * 70)

# --- INDICADOR 1: Empresas por cada 1000 habitantes ---
# Formula: (total_empresas / poblacion_total) * 1000
# Interpretacion: Mide la densidad empresarial relativa a la poblacion.
# Un valor alto indica un barrio con mucha actividad economica per capita.
# Un valor bajo puede indicar un barrio "dormitorio" con poca actividad comercial.
gdf_merged["empresas_por_1000hab"] = (
    gdf_merged["total_empresas"] / gdf_merged["poblacio_3"] * 1000
).round(1)

# --- INDICADOR 2: Empleo por cada 1000 habitantes ---
# Formula: (empleo_total / poblacion_total) * 1000
# Interpretacion: Mide la capacidad de generacion de empleo del barrio.
# Un valor alto indica que el barrio es un polo de empleo (atrae trabajadores).
# Un valor bajo indica que los residentes probablemente trabajan en otros barrios.
gdf_merged["empleo_por_1000hab"] = (
    gdf_merged["empleo_total"] / gdf_merged["poblacio_3"] * 1000
).round(1)

# --- INDICADOR 3: Ingresos per capita ---
# Formula: ingresos_total / poblacion_total
# Interpretacion: Mide el volumen economico generado por habitante del barrio.
# Permite comparar la productividad economica territorial independiente del tamano.
# Valores muy altos indican zonas industriales/comerciales con poca residencia.
gdf_merged["ingresos_per_capita"] = (
    gdf_merged["ingresos_total"] / gdf_merged["poblacio_3"]
).round(0)

# --- INDICADOR 4: Personas por empresa ---
# Formula: poblacion_total / total_empresas
# Interpretacion: Cuantos habitantes hay por cada empresa en el barrio.
# Un valor bajo (ej: 5-10) indica alta densidad comercial.
# Un valor alto (ej: 100+) indica barrios residenciales con poca oferta comercial.
gdf_merged["personas_por_empresa"] = (
    gdf_merged["poblacio_3"] / gdf_merged["total_empresas"]
).round(1)

# --- INDICADOR 5: Ratio empleo/hogares ---
# Formula: empleo_total / hogares
# Interpretacion: Cuantos empleos genera el barrio por cada hogar que tiene.
# Si es > 1, el barrio genera mas empleos de los que necesitan sus hogares.
# Si es < 1, los hogares dependen de empleo externo.
# Util para medir autosuficiencia economica del territorio.
gdf_merged["empleo_por_hogar"] = (
    gdf_merged["empleo_total"] / gdf_merged["hogares"]
).round(2)

# --- INDICADOR 6: Densidad empresarial por vivienda ---
# Formula: total_empresas / viviendas
# Interpretacion: Relacion entre actividad economica y uso residencial.
# Valores altos indican zonas mixtas (comercio + vivienda).
# Valores bajos indican zonas puramente residenciales.
gdf_merged["empresas_por_vivienda"] = (
    gdf_merged["total_empresas"] / gdf_merged["viviendas"]
).round(3)

# Filtrar barrios con datos completos para analisis
gdf_analisis = gdf_merged[
    gdf_merged["total_empresas"].notna() & 
    gdf_merged["poblacio_3"].notna() &
    (gdf_merged["poblacio_3"] > 0)
].copy()

print(f"\nBarrios con datos completos para analisis: {len(gdf_analisis)}")
print("\nINDICADORES CALCULADOS:")
print("-" * 70)
print(f"  1. Empresas por 1000 hab  -> Densidad empresarial relativa")
print(f"  2. Empleo por 1000 hab    -> Capacidad de generacion de empleo")
print(f"  3. Ingresos per capita    -> Productividad economica territorial")
print(f"  4. Personas por empresa   -> Cobertura comercial del barrio")
print(f"  5. Empleo por hogar       -> Autosuficiencia economica")
print(f"  6. Empresas por vivienda  -> Mixtura de uso (comercial/residencial)")

# Estadisticas de los indicadores
print("\n\nESTADISTICAS DE INDICADORES:")
print("-" * 70)
cols_ind = ["empresas_por_1000hab", "empleo_por_1000hab", "ingresos_per_capita",
            "personas_por_empresa", "empleo_por_hogar", "empresas_por_vivienda"]
print(gdf_analisis[cols_ind].describe().round(2).to_string())

# =============================================================================
# 5. GRAFICOS
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


# --- 5.1 Top 20 barrios por empresas/1000 hab ---
top20_emp1000 = gdf_analisis.nlargest(20, "empresas_por_1000hab")

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top20_emp1000["barrio_key"], top20_emp1000["empresas_por_1000hab"], color="#3498db", edgecolor="white")
ax.set_title("Top 20 Barrios - Empresas por cada 1000 habitantes\n(Mayor densidad empresarial relativa)", fontsize=13, fontweight="bold")
ax.set_xlabel("Empresas por 1000 hab")
ax.invert_yaxis()
# Agregar etiquetas de valor
for i, v in enumerate(top20_emp1000["empresas_por_1000hab"]):
    ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=8)
plt.tight_layout()
guardar_grafico(fig, "15_top20_empresas_por_1000hab")

# --- 5.2 Top 20 barrios por empleo/1000 hab ---
top20_empleo = gdf_analisis.nlargest(20, "empleo_por_1000hab")

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top20_empleo["barrio_key"], top20_empleo["empleo_por_1000hab"], color="#2ecc71", edgecolor="white")
ax.set_title("Top 20 Barrios - Empleo por cada 1000 habitantes\n(Mayores polos de empleo)", fontsize=13, fontweight="bold")
ax.set_xlabel("Empleos por 1000 hab")
ax.invert_yaxis()
for i, v in enumerate(top20_empleo["empleo_por_1000hab"]):
    ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=8)
plt.tight_layout()
guardar_grafico(fig, "16_top20_empleo_por_1000hab")

# --- 5.3 Scatter: Empresas vs Poblacion por barrio ---
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(
    gdf_analisis["poblacio_3"],
    gdf_analisis["total_empresas"],
    c=gdf_analisis["comuna"],
    cmap="tab20",
    alpha=0.6,
    s=40,
    edgecolors="white",
    linewidth=0.5
)
ax.set_xlabel("Poblacion del barrio")
ax.set_ylabel("Total de empresas")
ax.set_title("Relacion Poblacion vs Empresas por Barrio\n(Cada punto es un barrio, color = comuna)", fontsize=13, fontweight="bold")
aplicar_formato_eje(ax, "x")
aplicar_formato_eje(ax, "y")
# Linea de referencia: promedio nacional
ratio_promedio = gdf_analisis["total_empresas"].sum() / gdf_analisis["poblacio_3"].sum()
x_line = np.linspace(0, gdf_analisis["poblacio_3"].max(), 100)
ax.plot(x_line, x_line * ratio_promedio, "--", color="red", alpha=0.7, label=f"Promedio: {ratio_promedio*1000:.0f} emp/1000hab")
ax.legend(fontsize=10)
plt.tight_layout()
guardar_grafico(fig, "17_scatter_poblacion_vs_empresas")

# --- 5.4 Distribucion de empresas por 1000 hab (histograma) ---
fig, ax = plt.subplots(figsize=(10, 5))
datos = gdf_analisis["empresas_por_1000hab"].dropna()
ax.hist(datos[datos < datos.quantile(0.95)], bins=30, edgecolor="white", alpha=0.8, color="#9b59b6")
ax.axvline(datos.median(), color="red", linestyle="--", linewidth=2, label=f"Mediana: {datos.median():.0f}")
ax.axvline(datos.mean(), color="orange", linestyle="-", linewidth=2, label=f"Media: {datos.mean():.0f}")
ax.set_xlabel("Empresas por 1000 habitantes")
ax.set_ylabel("Cantidad de barrios")
ax.set_title("Distribucion de Densidad Empresarial por Barrio\n(Empresas por cada 1000 habitantes)", fontsize=13, fontweight="bold")
ax.legend(fontsize=11)
plt.tight_layout()
guardar_grafico(fig, "18_distribucion_empresas_1000hab")

# --- 5.5 Comparativo por comuna: indicadores promedio ---
ind_comuna = gdf_analisis.groupby("comuna").agg(
    empresas_1000hab=("empresas_por_1000hab", "mean"),
    empleo_1000hab=("empleo_por_1000hab", "mean"),
    personas_empresa=("personas_por_empresa", "mean"),
    empleo_hogar=("empleo_por_hogar", "mean"),
).reset_index().sort_values("empresas_1000hab", ascending=False)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Indicadores Promedio por Comuna", fontsize=14, fontweight="bold")

# 1. Empresas/1000hab por comuna
axes[0, 0].barh(ind_comuna["comuna"].astype(str), ind_comuna["empresas_1000hab"], color="#3498db")
axes[0, 0].set_title("Empresas por 1000 hab")
axes[0, 0].set_xlabel("Promedio")
axes[0, 0].invert_yaxis()

# 2. Empleo/1000hab por comuna
ind_comuna_sorted = ind_comuna.sort_values("empleo_1000hab", ascending=False)
axes[0, 1].barh(ind_comuna_sorted["comuna"].astype(str), ind_comuna_sorted["empleo_1000hab"], color="#2ecc71")
axes[0, 1].set_title("Empleo por 1000 hab")
axes[0, 1].set_xlabel("Promedio")
axes[0, 1].invert_yaxis()

# 3. Personas por empresa
ind_comuna_sorted2 = ind_comuna.sort_values("personas_empresa", ascending=True)
axes[1, 0].barh(ind_comuna_sorted2["comuna"].astype(str), ind_comuna_sorted2["personas_empresa"], color="#e74c3c")
axes[1, 0].set_title("Personas por empresa (menor = mas comercial)")
axes[1, 0].set_xlabel("Promedio")
axes[1, 0].invert_yaxis()

# 4. Empleo por hogar
ind_comuna_sorted3 = ind_comuna.sort_values("empleo_hogar", ascending=False)
axes[1, 1].barh(ind_comuna_sorted3["comuna"].astype(str), ind_comuna_sorted3["empleo_hogar"], color="#f39c12")
axes[1, 1].set_title("Empleo por hogar (>1 = genera mas del que necesita)")
axes[1, 1].set_xlabel("Promedio")
axes[1, 1].invert_yaxis()

plt.tight_layout()
guardar_grafico(fig, "19_indicadores_promedio_comuna")

# --- 5.6 Mapa coropletico: Empresas por 1000 hab ---
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
gdf_analisis.plot(
    column="empresas_por_1000hab",
    cmap="YlOrRd",
    linewidth=0.5,
    edgecolor="0.3",
    legend=True,
    legend_kwds={"label": "Empresas por 1000 hab", "shrink": 0.7},
    ax=ax,
    missing_kwds={"color": "lightgrey"}
)
ax.set_title("Mapa: Empresas por cada 1000 habitantes por Barrio\n(Densidad empresarial relativa a la poblacion)", fontsize=13, fontweight="bold")
ax.set_axis_off()
plt.tight_layout()
guardar_grafico(fig, "20_mapa_empresas_1000hab_barrio")

# =============================================================================
# 6. REPORTE DE INDICADORES
# =============================================================================
print("\n" + "=" * 70)
print("GENERANDO REPORTE...")
print("=" * 70)

REPORTE_PATH = OUTPUT_DIR / "indicadores_demograficos_barrio.txt"

with open(REPORTE_PATH, "w", encoding="utf-8") as f:
    f.write("=" * 100 + "\n")
    f.write("INDICADORES DEMOGRAFICOS + ECONOMICOS POR BARRIO - Cali\n")
    f.write("Cruce: Registro Mercantil 2025 + Personas por Hogar (Censo 2016)\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 100 + "\n\n")

    f.write("-" * 100 + "\n")
    f.write("INDICADORES CALCULADOS Y SU RELEVANCIA\n")
    f.write("-" * 100 + "\n\n")

    f.write("1. EMPRESAS POR 1000 HABITANTES\n")
    f.write("   Formula: (total_empresas / poblacion) * 1000\n")
    f.write("   Relevancia: Mide la densidad empresarial relativa a la poblacion.\n")
    f.write("   Uso: Identificar barrios con alta/baja actividad economica per capita.\n")
    f.write("   Seguimiento: Comparar entre periodos para medir dinamismo empresarial.\n\n")

    f.write("2. EMPLEO POR 1000 HABITANTES\n")
    f.write("   Formula: (empleo_total / poblacion) * 1000\n")
    f.write("   Relevancia: Identifica polos de empleo vs barrios dormitorio.\n")
    f.write("   Uso: Planificacion de transporte y movilidad laboral.\n")
    f.write("   Seguimiento: Medir si las intervenciones generan empleo local.\n\n")

    f.write("3. INGRESOS PER CAPITA\n")
    f.write("   Formula: ingresos_total / poblacion\n")
    f.write("   Relevancia: Productividad economica del territorio por habitante.\n")
    f.write("   Uso: Comparar nivel economico entre barrios independiente del tamano.\n")
    f.write("   Seguimiento: Medir crecimiento economico territorial.\n\n")

    f.write("4. PERSONAS POR EMPRESA\n")
    f.write("   Formula: poblacion / total_empresas\n")
    f.write("   Relevancia: Cobertura comercial. Menos personas/empresa = mas oferta.\n")
    f.write("   Uso: Identificar desiertos comerciales (barrios sin oferta).\n")
    f.write("   Seguimiento: Medir si se cierra la brecha de acceso a servicios.\n\n")

    f.write("5. EMPLEO POR HOGAR\n")
    f.write("   Formula: empleo_total / hogares\n")
    f.write("   Relevancia: Autosuficiencia economica del barrio.\n")
    f.write("   Uso: Si > 1, el barrio exporta empleo. Si < 1, depende de otros.\n")
    f.write("   Seguimiento: Medir si las zonas se vuelven autosuficientes.\n\n")

    f.write("6. EMPRESAS POR VIVIENDA\n")
    f.write("   Formula: total_empresas / viviendas\n")
    f.write("   Relevancia: Mixtura de uso del suelo (comercial vs residencial).\n")
    f.write("   Uso: Planificacion urbana y zonificacion.\n")
    f.write("   Seguimiento: Medir transformacion del uso del suelo.\n\n")

    # Top 20 barrios
    f.write("-" * 100 + "\n")
    f.write("TOP 20 BARRIOS - EMPRESAS POR 1000 HABITANTES\n")
    f.write("-" * 100 + "\n")
    f.write(f"{'Barrio':<30} {'Comuna':>6} {'Poblacion':>10} {'Empresas':>9} {'Emp/1000hab':>12}\n")
    f.write("-" * 100 + "\n")
    for _, row in top20_emp1000.iterrows():
        f.write(f"{str(row['barrio_key'])[:30]:<30} {int(row['comuna']):>6} {int(row['poblacio_3']):>10,} {int(row['total_empresas']):>9,} {row['empresas_por_1000hab']:>12.1f}\n")
    f.write("\n")

    # Top 20 empleo
    f.write("-" * 100 + "\n")
    f.write("TOP 20 BARRIOS - EMPLEO POR 1000 HABITANTES\n")
    f.write("-" * 100 + "\n")
    f.write(f"{'Barrio':<30} {'Comuna':>6} {'Poblacion':>10} {'Empleo':>8} {'Emp/1000hab':>12}\n")
    f.write("-" * 100 + "\n")
    for _, row in top20_empleo.iterrows():
        f.write(f"{str(row['barrio_key'])[:30]:<30} {int(row['comuna']):>6} {int(row['poblacio_3']):>10,} {int(row['empleo_total']):>8,} {row['empleo_por_1000hab']:>12.1f}\n")
    f.write("\n")

    # Resumen por comuna
    f.write("-" * 100 + "\n")
    f.write("PROMEDIO DE INDICADORES POR COMUNA\n")
    f.write("-" * 100 + "\n")
    f.write(f"{'Comuna':>6} {'Emp/1000hab':>12} {'Empleo/1000hab':>15} {'Pers/Empresa':>13} {'Empleo/Hogar':>13}\n")
    f.write("-" * 100 + "\n")
    for _, row in ind_comuna.iterrows():
        f.write(f"{int(row['comuna']):>6} {row['empresas_1000hab']:>12.1f} {row['empleo_1000hab']:>15.1f} {row['personas_empresa']:>13.1f} {row['empleo_hogar']:>13.2f}\n")

    f.write("\n" + "=" * 100 + "\n")
    f.write("FIN DEL REPORTE\n")
    f.write("=" * 100 + "\n")

print(f"  [OK] Reporte guardado: {REPORTE_PATH.name}")

# =============================================================================
# 7. RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)
print(f"""
  Barrios analizados:        {len(gdf_analisis)}
  Indicadores calculados:    6
  Graficos generados:        6
  Reporte:                   {REPORTE_PATH.name}

  INDICADORES MAS RELEVANTES (por orden de importancia):

  1. Empresas/1000hab  - El mas importante porque normaliza por poblacion
                         y permite comparar barrios de cualquier tamano.
                         Mediana: {gdf_analisis['empresas_por_1000hab'].median():.0f} | Media: {gdf_analisis['empresas_por_1000hab'].mean():.0f}

  2. Empleo/1000hab    - Identifica donde se genera el empleo vs donde
                         vive la gente. Clave para movilidad y transporte.
                         Mediana: {gdf_analisis['empleo_por_1000hab'].median():.0f} | Media: {gdf_analisis['empleo_por_1000hab'].mean():.0f}

  3. Personas/empresa  - Facil de comunicar: "en este barrio hay 1 empresa
                         por cada X personas". Detecta desiertos comerciales.
                         Mediana: {gdf_analisis['personas_por_empresa'].median():.0f} | Media: {gdf_analisis['personas_por_empresa'].mean():.0f}

  4. Empleo/hogar      - Mide autosuficiencia. Si > 1, el barrio es polo
                         de empleo. Si < 1, es barrio dormitorio.
                         Mediana: {gdf_analisis['empleo_por_hogar'].median():.2f} | Media: {gdf_analisis['empleo_por_hogar'].mean():.2f}
""")

print("[OK] Analisis completado exitosamente.")
