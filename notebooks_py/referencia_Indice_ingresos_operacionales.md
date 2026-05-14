# Referencia Tecnica — Indice de Ingresos Operacionales

**Script principal:** `notebooks_py/01_analisis_exploratorio.py`  
**Equipo:** ITT Cali Inteligente - Gobierno de Datos  
**Fecha de documentacion:** Mayo 2026  
**Repositorio:** https://github.com/j0rg3c45/Indice_ingresos_operacionales.git

---

## 1. Objetivo del Proyecto

Construir un indice de ingresos operacionales a partir del Registro Mercantil 2025 de Cali,
que permita medir y comparar la actividad economica por territorio (comunas, barrios)
y hacer seguimiento en el tiempo como insumo para el Indice de Transformacion Territorial (ITT).

---

## 2. Fuente de Datos

| Campo | Valor |
|-------|-------|
| Archivo | `data/Registro mercantil 2025_.xlsx` |
| Registros | 122,535 |
| Columnas | 17 |
| Ciudad | Cali (100% de los registros) |
| Periodo | Matriculas historicas con renovacion a marzo 2025 |

---

## 3. Diccionario de Variables

| # | Variable original | Tipo | Descripcion |
|---|-------------------|------|-------------|
| 1 | num_inscrito | int64 | Numero de inscripcion en el registro |
| 2 | mes,_dia,_ano_de_fecha_matricula | str | Fecha de matricula original |
| 3 | mes,_dia,_ano_de_fecha_renovacion | str | Fecha de ultima renovacion |
| 4 | categoria | str | Persona Natural / Persona Juridica / 0 |
| 5 | nombre_sector | str | Sector economico (20 sectores) |
| 6 | codigo_ciiu | int64 | Codigo CIIU de actividad economica (466 codigos) |
| 7 | desc_ciiu | str | Descripcion de la actividad CIIU |
| 8 | tamano957 | str | Tamano de empresa: MICRO, PEQUENA, MEDIANA, GRANDE |
| 9 | ciudad | str | Ciudad (Cali en todos los registros) |
| 10 | comuna | str | Comuna de ubicacion (39 comunas) |
| 11 | barrio | str | Barrio de ubicacion (494 barrios) |
| 12 | direccion_comercial | str | Direccion del establecimiento |
| 13 | tipo_registro | str | MERCANTIL (95%) o ESAL (5%) |
| 14 | personal_ocupado | float64 | Numero de empleados |
| 15 | numero_de_hombres | int64 | Empleados hombres |
| 16 | numero_de_mujeres | int64 | Empleados mujeres |
| 17 | ingresos_actividad_ordinaria | float64 | Ingresos operacionales reportados |

---

## 4. Estadisticas Clave del Dataset

### 4.1 Distribucion por tamano

| Tamano | Cantidad | Porcentaje |
|--------|----------|-----------|
| MICRO | 116,544 | 95.1% |
| PEQUENA | 3,200 | 2.6% |
| PEQUENA (alt) | 1,360 | 1.1% |
| MEDIANA | 1,026 | 0.8% |
| GRANDE | 350 | 0.3% |

### 4.2 Distribucion por tipo de registro

| Tipo | Cantidad | Porcentaje |
|------|----------|-----------|
| MERCANTIL | 116,378 | 95.0% |
| ESAL | 6,157 | 5.0% |

### 4.3 Distribucion por categoria

| Categoria | Cantidad | Porcentaje |
|-----------|----------|-----------|
| PERSONA NATURAL | 71,928 | 58.7% |
| PERSONA JURIDICA | 44,449 | 36.3% |
| 0 (sin clasificar) | 6,158 | 5.0% |

### 4.4 Top 5 comunas

| Comuna | Cantidad | Porcentaje |
|--------|----------|-----------|
| Comuna 02 | 13,994 | 11.4% |
| Comuna 17 | 13,238 | 10.8% |
| Comuna 03 | 11,032 | 9.0% |
| Comuna 19 | 10,320 | 8.4% |
| Comuna 10 | 6,020 | 4.9% |

### 4.5 Top 5 sectores economicos

| Sector | Cantidad | Porcentaje |
|--------|----------|-----------|
| Comercio al por mayor y menor | 43,217 | 35.3% |
| Industrias manufactureras | 13,585 | 11.1% |
| Otras actividades de servicios | 11,430 | 9.3% |
| Alojamiento y servicios de comida | 10,211 | 8.3% |
| Actividades profesionales | 9,104 | 7.4% |

### 4.6 Ingresos operacionales

| Estadistica | Valor |
|-------------|-------|
| Media | $1,148M |
| Mediana | $0 |
| Percentil 75 | $52.4M |
| Maximo | $8.25B (billones) |
| Registros con ingresos > 0 | ~41,330 |
| Registros con ingresos = 0 | ~63,355 |
| Registros sin dato | 17,850 (14.6%) |

### 4.7 Empleo

| Estadistica | Valor |
|-------------|-------|
| Media | 4.7 empleados |
| Mediana | 1 |
| Maximo | 12,568 |
| Empresas con 0 empleados | 55,151 (45%) |

---

## 5. Valores Nulos

| Columna | Nulos | Porcentaje |
|---------|-------|-----------|
| ingresos_actividad_ordinaria | 17,850 | 14.57% |
| barrio | 7,938 | 6.48% |
| comuna | 7,636 | 6.23% |
| direccion_comercial | 544 | 0.44% |
| personal_ocupado | 225 | 0.18% |
| tamano957 | 55 | 0.04% |
| desc_ciiu | 25 | 0.02% |
| fecha_matricula | 4 | 0.00% |
| nombre_sector | 3 | 0.00% |

---

## 6. Script de Analisis Exploratorio

### 6.1 Archivo

`notebooks_py/01_analisis_exploratorio.py`

### 6.2 Ejecucion

```bash
uv run notebooks_py/01_analisis_exploratorio.py
```

### 6.3 Funcionalidades

| Seccion | Descripcion |
|---------|-------------|
| 1 | Configuracion de rutas |
| 2 | Carga y normalizacion de columnas |
| 3 | Informacion general (tipos, head, describe) |
| 4 | Reporte de valores nulos |
| 5 | Reporte de valores unicos y repetidos |
| 6 | Deteccion de filas duplicadas |
| 7 | Graficos basicos (11 graficos PNG) |
| 8 | Generacion de reporte .txt consolidado |
| 9 | Resumen final en consola |

### 6.4 Formato de ejes en graficos

Los valores grandes se abrevian automaticamente:
- 1,000 -> 1K
- 1,000,000 -> 1M
- 1,000,000,000 -> 1B

### 6.5 Graficos generados

| # | Archivo | Contenido |
|---|---------|-----------|
| 01 | 01_distribucion_ingresos.png | Histograma + Boxplot de ingresos |
| 02 | 02_distribucion_ingresos_log.png | Distribucion en escala logaritmica |
| 03 | 03_distribucion_tamano.png | Barras por tamano de empresa |
| 04 | 04_distribucion_estado.png | Pie chart de estado |
| 05 | 05_tipo_registro.png | Pie chart MERCANTIL vs ESAL |
| 06 | 06_categoria.png | Barras horizontales por categoria |
| 07 | 06_top_comunas.png | Top 15 comunas |
| 08 | 07_top_ciiu.png | Top 15 actividades CIIU |
| 09 | 08_distribucion_empleo.png | Histograma + Boxplot de empleo |
| 10 | 09_ingresos_por_tamano.png | Boxplot comparativo |
| 11 | 10_correlacion.png | Heatmap de correlacion |
| 12 | 11_valores_nulos.png | Barras de % nulos |

---

## 7. Salidas del Proyecto

### 7.1 Reporte de texto

- **Archivo:** `outputs/reporte_analisis_exploratorio.txt`
- **Contenido:** Tablas consolidadas de todo el analisis (info general, estadisticas, nulos, unicos/repetidos, top categoricas, duplicados)

### 7.2 Indicadores de territorio

- **Archivo:** `outputs/indicadores_territorio_cali.txt`
- **Contenido:** Propuesta de indicadores territoriales medibles en el tiempo por zona/comuna

### 7.3 Graficos PNG

- **Directorio:** `outputs/`
- **Formato:** PNG 150 DPI

---

## 8. Relacion con el ITT

Este proyecto alimenta la dimension economica del Indice de Transformacion Territorial (ITT):

| Dimension ITT | Indicador derivable | Variable fuente |
|---------------|--------------------|-----------------| 
| Economia territorial | Densidad empresarial por comuna | comuna + conteo |
| Economia territorial | Ingresos promedio por zona | ingresos_actividad_ordinaria + comuna |
| Economia territorial | Tasa de microempresas | tamano957 + comuna |
| Empleo | Empleo promedio por empresa | personal_ocupado + comuna |
| Empleo | Concentracion de empleo formal | personal_ocupado + tamano957 |
| Diversificacion | Indice de diversidad economica (CIIU) | codigo_ciiu + comuna |
| Dinamismo | Tasa de nuevas matriculas | fecha_matricula + comuna |

### 8.1 Uso territorial con GeoJSON

Los indicadores se pueden cruzar espacialmente con capas GeoJSON de comunas/barrios de Cali
para generar mapas coropleticos y analisis por zona de intervencion ITT.

---

## 9. Estructura del Repositorio

```
Indice_ingresos_operacionales/
├── README.md                 # Descripcion general del proyecto
├── requirements.txt          # Dependencias Python (pip)
├── environment.yml           # Entorno Conda
├── .gitignore                # Archivos excluidos del control de versiones
├── agent/                    # Notas del entorno y automatizacion
├── data/                     # Datos crudos y procesados
├── notebooks_py/             # Scripts de analisis
│   └── 01_analisis_exploratorio.py
├── outputs/                  # Resultados, reportes y visualizaciones
│   └── reporte_analisis_exploratorio.txt
└── docs/                     # Documentacion del proyecto
    ├── diccionario.txt       # Diccionario de datos
    └── metodologia.md        # Metodologia del indice
```

---

## 10. Dependencias

```
pandas>=2.0
openpyxl>=3.1
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
```

### Gestor de paquetes

Este proyecto usa **uv** como gestor de paquetes Python.

```bash
uv pip install -r requirements.txt
```

---

## 11. Proximos Pasos

1. Limpiar la variable `tamano957` (unificar PEQUENA y PEQUENA)
2. Parsear fechas de matricula y renovacion a formato datetime
3. Calcular indicadores territoriales por comuna y trimestre
4. Cruzar con GeoJSON de comunas para mapas coropleticos
5. Construir el indice compuesto de ingresos operacionales
6. Integrar como dimension economica en el ITT por zona de intervencion
7. Definir ref_min / ref_max para normalizacion de indicadores economicos
