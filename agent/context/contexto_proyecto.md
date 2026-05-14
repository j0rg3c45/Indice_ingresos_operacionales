# Contexto del Proyecto - Indice de Ingresos Operacionales

## Repositorio

- URL: https://github.com/j0rg3c45/Indice_ingresos_operacionales.git
- Rama: main
- Equipo: ITT Cali Inteligente - Gobierno de Datos

## Objetivo del proyecto

Construir un indice de ingresos operacionales a partir del Registro Mercantil 2025 de Cali,
que permita medir y comparar la actividad economica por territorio (comunas, barrios)
y hacer seguimiento en el tiempo como insumo para el Indice de Transformacion Territorial (ITT).

## Relacion con el ITT

Este proyecto alimenta la **dimension economica** del ITT. Los indicadores derivados son:
- Densidad empresarial por comuna
- Ingresos promedio/mediana por zona
- Tasa de microempresas
- Empleo promedio por empresa
- Concentracion de empleo formal
- Indice de diversidad economica (CIIU)
- Tasa de nuevas matriculas (dinamismo)

## Datos disponibles

### Registro Mercantil 2025
- Archivo: `data/Registro mercantil 2025_.xlsx`
- Registros: 122,535
- Columnas: 17
- Ciudad: Cali (100%)
- Periodo: Matriculas historicas con renovacion a marzo 2025

### GeoJSON de comunas
- Archivo: `data/info_geo/geojson_comunas/Comunas.geojson`
- Poligonos: 22 comunas urbanas de Cali
- CRS: EPSG:4326
- Columnas: comuna (int), nombre, area, geometry

## Estado actual de implementacion

| Componente | Estado | Archivo |
|-----------|--------|---------|
| Analisis exploratorio | Completo | notebooks_py/01_analisis_exploratorio.py |
| Carga datos + mapas | Completo | notebooks_py/02_carga_datos_mapa.ipynb |
| Indicadores por comuna | Completo | Calculados en notebook 02 |
| Cruce con GeoJSON | Completo | 22 comunas mapeadas |
| Mapas coropleticos | Completo | Estaticos (PNG) + interactivo (HTML) |
| Reporte EDA | Completo | outputs/reporte_analisis_exploratorio.txt |
| Reporte consolidado | Completo | outputs/consolidado.txt |
| Indicadores territorio | Propuesta | outputs/indicadores_territorio_cali.txt |
| Indice compuesto | Pendiente | Por definir formula y ponderaciones |
| Seguimiento temporal | Pendiente | Requiere datos de multiples periodos |

## Hallazgos clave del dataset

- 95.1% son microempresas
- 58.7% son persona natural
- 14.6% no reportan ingresos (nulos)
- 51.7% reportan ingresos = $0
- Top comunas: Comuna 02 (11.4%), Comuna 17 (10.8%), Comuna 03 (9.0%)
- Top sector: Comercio al por mayor y menor (35.3%)
- Ingreso promedio: $1,148M (sesgado por grandes empresas)
- Ingreso mediana: $0 (mayoria sin ingresos reportados)

## Entorno de ejecucion

- Local: Windows, uv + conda disponibles
- Colab: Notebook 02 detecta automaticamente y clona el repo
- Python: 3.12
- Dependencias: pandas, openpyxl, numpy, matplotlib, seaborn, geopandas, folium

## Reglas del agente

1. Cada cambio debe desencadenar actualizacion de contextos, .md y reportes
2. Cada cambio debe hacer commit + push automaticamente
3. Sin emojis en codigo
4. Formato abreviado en ejes (1K, 1M, 1B)
5. Reportes en texto plano (.txt) en outputs/
