# Metodologia del Indice de Ingresos Operacionales

## Objetivo

Construir un indice que permita medir y comparar los ingresos operacionales
reportados en el Registro Mercantil.

## Fuentes de datos

- Registro Mercantil 2025 (Superintendencia / Camara de Comercio)
- Diccionario de datos: `docs/diccionario.txt`

## Variables del dataset

| # | Variable | Descripcion |
|---|----------|-------------|
| 1 | CIIU | Codigo de actividad economica |
| 2 | Tamano | Clasificacion por tamano de empresa |
| 3 | Empleo | Numero de empleados reportados |
| 4 | Direccion | Ubicacion fisica del establecimiento |
| 5 | Estado | Estado de la matricula (activa/inactiva) |
| 6 | Nueva/Renovada | Si la matricula es nueva o renovada |
| 7 | Comuna | Comuna donde opera la empresa |
| 8 | Barrio | Barrio donde opera la empresa |
| 9 | Fecha inscripcion | Fecha de inscripcion en el registro |
| 10 | Ingresos operacionales | Ingresos operacionales reportados |

## Proceso

1. **Extraccion**: Lectura del archivo fuente `.xlsx`
2. **Exploracion**: Analisis exploratorio con `01_analisis_exploratorio.py`
   - Identificacion de valores nulos, duplicados, unicos y repetidos
   - Visualizacion de distribuciones y relaciones
   - Generacion de reporte `.txt` con tablas consolidadas
3. **Transformacion**: Limpieza, normalizacion y enriquecimiento de variables
4. **Calculo del indice**: Definicion de la formula y ponderaciones
5. **Validacion**: Controles de calidad y consistencia
6. **Publicacion**: Generacion de reportes y visualizaciones finales

## Formato de visualizacion

Los graficos usan formato abreviado para valores grandes:
- 1,000 -> 1K
- 1,000,000 -> 1M
- 1,000,000,000 -> 1B

## Salidas del analisis exploratorio

- Graficos interactivos (visualizacion en pantalla)
- `outputs/reporte_analisis_exploratorio.txt` — Tablas completas del analisis

## Supuestos y limitaciones

_(Documentar aqui conforme avance el proyecto)_
