# Indice de Ingresos Operacionales

Proyecto de analisis y gobierno de datos sobre ingresos operacionales a partir del Registro Mercantil 2025 de Santiago de Cali. Alimenta la dimension economica del Indice de Transformacion Territorial (ITT).

## Estructura del proyecto

```
Indice_ingresos_operacionales/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── agent/
│   ├── README.md                          # Convenciones, entorno, reglas git
│   ├── context/
│   │   ├── contexto_proyecto.md           # Contexto general del proyecto
│   │   ├── zonas_estudio.md               # Zonas ITT de referencia
│   │   └── glosario.md                    # Glosario de terminos
│   ├── knowledge_base/
│   │   └── Guia_ITT_Metodologia_Notebook.md
│   └── prompts/
│       └── system_prompt.md               # Reglas del agente
├── data/
│   ├── Registro mercantil 2025_.xlsx      # Fuente principal (122,535 registros)
│   └── info_geo/
│       ├── Comunas.zip
│       └── geojson_comunas/
│           └── Comunas.geojson            # 22 comunas de Cali
├── notebooks_py/
│   ├── 01_analisis_exploratorio.py        # Analisis EDA completo
│   ├── 02_carga_datos_mapa.ipynb          # Carga desde git + mapas geograficos
│   └── referencia_Indice_ingresos_operacionales.md
├── outputs/
│   ├── reporte_analisis_exploratorio.txt  # Reporte EDA
│   ├── consolidado.txt                    # Reporte consolidado con indicadores por comuna
│   ├── indicadores_territorio_cali.txt    # Propuesta de indicadores territoriales
│   └── *.png                              # Graficos generados
└── docs/
    ├── diccionario.txt
    └── metodologia.md
```

## Datos fuente

| Archivo | Registros | Descripcion |
|---------|-----------|-------------|
| Registro mercantil 2025_.xlsx | 122,535 | Matriculas mercantiles de Cali |
| Comunas.geojson | 22 poligonos | Comunas urbanas de Cali |

## Ejecucion

Este proyecto usa **uv** como gestor de paquetes Python. Tambien hay un ambiente conda disponible.

```bash
# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar analisis exploratorio (genera graficos PNG + reporte .txt)
uv run notebooks_py/01_analisis_exploratorio.py

# Notebook de mapas (ejecutar en Jupyter o Colab)
# notebooks_py/02_carga_datos_mapa.ipynb
```

## Scripts y notebooks

### 01_analisis_exploratorio.py

Analisis exploratorio completo del Registro Mercantil:
- Carga y normalizacion de 17 columnas
- Reporte de valores nulos, unicos y repetidos
- 11 graficos con formato abreviado (1K, 1M, 1B)
- Genera `outputs/reporte_analisis_exploratorio.txt`

### 02_carga_datos_mapa.ipynb

Carga de datos desde git y visualizacion geografica:
- Detecta entorno (Colab clona el repo, local usa carpeta directa)
- Calcula indicadores economicos por comuna (empresas, ingresos, empleo, % micro, diversidad CIIU)
- Cruza datos con GeoJSON de 22 comunas
- Genera mapas coropleticos (estaticos + interactivo Folium)
- Tablas formateadas de indicadores
- Genera `outputs/consolidado.txt`

## Salidas

| Archivo | Contenido |
|---------|-----------|
| reporte_analisis_exploratorio.txt | EDA completo con estadisticas y valores unicos |
| consolidado.txt | Indicadores por comuna, sectores, CIIU, estadisticas |
| indicadores_territorio_cali.txt | Propuesta de indicadores medibles en el tiempo |
| *.png | Graficos de distribucion, mapas coropleticos |
| mapa_interactivo_comunas.html | Mapa Folium con tooltips por comuna |

## Relacion con el ITT

Este proyecto alimenta la dimension economica del ITT:
- Densidad empresarial por comuna
- Ingresos promedio por zona
- Tasa de microempresas
- Empleo formal por territorio
- Diversidad economica (CIIU)
- Dinamismo (nuevas matriculas)
