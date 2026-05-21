# Agent - Notas del entorno

## Herramientas disponibles en este PC

- **uv** — Gestor de paquetes y entornos Python (instalado y disponible en PATH)
  - Usar `uv pip install` en lugar de `pip install`
  - Usar `uv venv` para crear entornos virtuales
  - Usar `uvx` para ejecutar herramientas sin instalarlas globalmente
  - Usar `uv run` para ejecutar scripts con el entorno activo
- **Ambiente Conda** — Existe un ambiente conda configurado con todas las dependencias del proyecto
- **Python 3.12** — Version instalada en el sistema

## Entorno de ejecucion

- Local: Windows, uv + conda disponibles, ejecutar directamente con `uv run` o `python`
- Colab: El notebook `02_carga_datos_mapa.ipynb` detecta automaticamente si esta en Colab y clona el repo

## Comandos rapidos

```bash
# Instalar dependencias del proyecto
uv pip install -r requirements.txt

# Ejecutar analisis exploratorio (genera EDA + consolidado + graficos resumen)
C:\Users\Jorge\.venv\Scripts\python.exe notebooks_py/01_analisis_exploratorio.py

# Ejecutar indicadores demograficos por barrio
C:\Users\Jorge\.venv\Scripts\python.exe notebooks_py/03_indicadores_demograficos_barrio.py

# Notebooks (ejecutar en Jupyter o Colab):
# - notebooks_py/02_carga_datos_mapa.ipynb
# - notebooks_py/03_indicadores_ingresos_comuna.ipynb
```

## Dependencias instaladas

- pandas, openpyxl (lectura de datos)
- numpy (calculo numerico)
- matplotlib, seaborn (visualizacion)
- geopandas (datos geoespaciales)
- folium, mapclassify (mapas interactivos)
- scikit-learn (analisis estadistico)

## Convenciones del proyecto

- Sin emojis ni caracteres especiales en el codigo
- Formato abreviado en ejes de graficos (1K, 1M, 1B)
- Reportes de texto plano (.txt) en outputs/
- Exportacion de graficos (.png) en outputs/
- **Despues de cada cambio, SIEMPRE hacer commit y push al repositorio git**

## Git - Regla obligatoria

Despues de cualquier modificacion (crear, editar o eliminar archivos), ejecutar:

```bash
git add .
git commit -m "descripcion breve del cambio"
git push
```

- Repositorio: https://github.com/j0rg3c45/Indice_ingresos_operacionales.git
- Rama: main
- No esperar a que el usuario lo pida. Hacerlo automaticamente.

## Actualizacion de contexto - Regla obligatoria

Cada cambio en el proyecto DEBE desencadenar la actualizacion de los archivos relacionados:

| Si cambias... | Actualiza tambien... |
|---------------|---------------------|
| Codigo (.py, .ipynb) | README.md, referencia tecnica, reportes en outputs/ |
| Datos o estructura de datos | docs/metodologia.md, agent/context/contexto_proyecto.md |
| Zonas de estudio | agent/context/zonas_estudio.md |
| Dependencias o entorno | requirements.txt, environment.yml, agent/README.md |
| Indicadores o metricas | outputs/indicadores_territorio_cali.txt, docs/metodologia.md |
| Metodologia | agent/knowledge_base/, agent/context/glosario.md |

Mantener SIEMPRE la coherencia entre codigo, documentacion y contexto del agente.
