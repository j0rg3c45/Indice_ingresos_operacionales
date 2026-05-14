# Indice de Ingresos Operacionales

Proyecto de analisis y gobierno de datos sobre ingresos operacionales a partir del Registro Mercantil.

## Estructura del proyecto

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

## Datos fuente

- Registro Mercantil 2025 (`.xlsx`)
- Diccionario de datos (`diccionario.txt`)

## Ejecucion

Este proyecto usa **uv** como gestor de paquetes Python.

```bash
# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar analisis exploratorio
uv run notebooks_py/01_analisis_exploratorio.py
```

## Script de analisis exploratorio

El archivo `notebooks_py/01_analisis_exploratorio.py` realiza:

1. Carga y normalizacion de datos del Excel
2. Informacion general del dataset (tipos, primeras filas, estadisticas)
3. Reporte de valores nulos
4. Reporte de valores unicos y repetidos por columna
5. Detalle de top 15 valores por columna categorica
6. Deteccion de filas duplicadas
7. Graficos basicos con formato abreviado en ejes (1M, 500K, etc.):
   - Distribucion de ingresos operacionales (histograma + boxplot)
   - Distribucion en escala logaritmica
   - Distribucion por tamano de empresa
   - Estado (activa/inactiva)
   - Nueva vs Renovada
   - Top 15 comunas
   - Top 15 actividades CIIU
   - Distribucion de empleo
   - Ingresos por tamano (boxplot comparativo)
   - Matriz de correlacion
   - Valores nulos por columna
8. Genera reporte `.txt` con todas las tablas en `outputs/`

## Salidas

- **Graficos**: Se muestran en pantalla (exportacion a PNG comentada, descomentar cuando se necesite)
- **Reporte**: `outputs/reporte_analisis_exploratorio.txt` con tablas completas
