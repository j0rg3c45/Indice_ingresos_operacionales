# Metodologia del Indice de Ingresos Operacionales

## Objetivo

Construir un indice que permita medir y comparar los ingresos operacionales
reportados en el Registro Mercantil, desagregado por territorio (comunas de Cali),
con capacidad de seguimiento en el tiempo.

## Fuentes de datos

| Fuente | Archivo | Descripcion |
|--------|---------|-------------|
| Registro Mercantil 2025 | data/Registro mercantil 2025_.xlsx | 122,535 matriculas |
| GeoJSON Comunas | data/info_geo/geojson_comunas/Comunas.geojson | 22 comunas urbanas |
| Diccionario | docs/diccionario.txt | Descripcion de variables |

## Variables del dataset (17 columnas reales)

| # | Variable | Tipo | Descripcion |
|---|----------|------|-------------|
| 1 | num_inscrito | int64 | Numero de inscripcion |
| 2 | mes,_dia,_ano_de_fecha_matricula | str | Fecha de matricula |
| 3 | mes,_dia,_ano_de_fecha_renovacion | str | Fecha de renovacion |
| 4 | categoria | str | Persona Natural / Juridica |
| 5 | nombre_sector | str | Sector economico (20 sectores) |
| 6 | codigo_ciiu | int64 | Codigo CIIU (466 codigos) |
| 7 | desc_ciiu | str | Descripcion actividad CIIU |
| 8 | tamano957 | str | MICRO / PEQUENA / MEDIANA / GRANDE |
| 9 | ciudad | str | Cali (100%) |
| 10 | comuna | str | Comuna (39 zonas) |
| 11 | barrio | str | Barrio (494 barrios) |
| 12 | direccion_comercial | str | Direccion del establecimiento |
| 13 | tipo_registro | str | MERCANTIL (95%) / ESAL (5%) |
| 14 | personal_ocupado | float64 | Empleados totales |
| 15 | numero_de_hombres | int64 | Empleados hombres |
| 16 | numero_de_mujeres | int64 | Empleados mujeres |
| 17 | ingresos_actividad_ordinaria | float64 | Ingresos operacionales |

## Proceso implementado

1. **Extraccion**: Lectura del archivo fuente `.xlsx` (122,535 registros)
2. **Exploracion**: Analisis exploratorio con `01_analisis_exploratorio.py`
   - Identificacion de valores nulos, duplicados, unicos y repetidos
   - Visualizacion de distribuciones y relaciones
   - Generacion de reporte `.txt` con tablas consolidadas
   - 11 graficos PNG con formato abreviado en ejes
3. **Indicadores por comuna**: Calculados en `02_carga_datos_mapa.ipynb`
   - Total empresas, ingresos promedio/mediana/total
   - Empleo total y promedio por empresa
   - Tasa de microempresas (%)
   - Diversidad economica (CIIU distintos)
   - Densidad empresarial (empresas/hectarea)
4. **Cruce geografico**: Merge con GeoJSON de 22 comunas
   - Normalizacion de nombres (zero-padding: "Comuna 6" -> "Comuna 06")
   - Calculo de area en hectareas
5. **Visualizacion territorial**: Mapas coropleticos
   - Estaticos: densidad empresarial, ingresos, empleo (matplotlib)
   - Interactivo: Folium con tooltips y multiples capas base
6. **Reportes**: Generacion automatica de .txt consolidados

## Indicadores calculados por comuna

| Indicador | Descripcion | Uso ITT |
|-----------|-------------|---------|
| total_empresas | Conteo de matriculas activas | Densidad empresarial |
| ingresos_promedio | Media de ingresos operacionales | Nivel economico |
| ingresos_mediana | Mediana de ingresos | Nivel economico (robusto) |
| ingresos_total | Suma de ingresos | Peso economico territorial |
| empleo_total | Suma de personal ocupado | Empleo formal |
| empleo_promedio | Media de empleados por empresa | Tamano promedio |
| pct_micro | % de microempresas | Estructura productiva |
| n_ciiu_distintos | Actividades economicas unicas | Diversidad economica |
| densidad_empresarial | Empresas por hectarea | Concentracion economica |

## Formato de visualizacion

Los graficos usan formato abreviado para valores grandes:
- 1,000 -> 1K
- 1,000,000 -> 1M
- 1,000,000,000 -> 1B

## Salidas del proyecto

| Archivo | Contenido |
|---------|-----------|
| outputs/reporte_analisis_exploratorio.txt | EDA completo |
| outputs/consolidado.txt | Indicadores por comuna + estadisticas |
| outputs/indicadores_territorio_cali.txt | Propuesta de indicadores temporales |
| outputs/*.png | Graficos de distribucion y mapas |
| outputs/mapa_interactivo_comunas.html | Mapa Folium interactivo |

## Proximos pasos

1. Limpiar variable tamano957 (unificar PEQUENA y PEQUENA)
2. Parsear fechas a datetime para analisis temporal
3. Definir formula del indice compuesto de ingresos
4. Calibrar ref_min / ref_max para normalizacion (metodologia ITT)
5. Integrar como dimension economica en el ITT por zona
6. Incorporar datos de multiples periodos para seguimiento temporal

## Supuestos y limitaciones

- El 14.6% de registros no reportan ingresos (nulos)
- El 51.7% reportan ingresos = $0 (microempresas informales o sin actividad)
- El GeoJSON solo cubre 22 de las 39 zonas del Registro (faltan corregimientos)
- Las fechas estan en formato texto, no datetime
- La variable tamano957 tiene duplicados (PEQUENA vs PEQUENA)
