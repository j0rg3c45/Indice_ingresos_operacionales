# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project purpose
- Build and maintain the **Indice de Ingresos Operacionales** for Cali using Registro Mercantil 2025 data.
- Produce territorial economic indicators (comuna and barrio level) as input to ITT (Indice de Transformacion Territorial).

## Environment and dependency setup
- Primary package/runtime flow uses `uv`; conda environment is also available.
- Install dependencies:
  - `uv pip install -r requirements.txt`
- Optional conda flow:
  - `conda env create -f environment.yml`
  - `conda activate indice_ingresos`

## Core run commands
- Run exploratory analysis pipeline (reads Excel, generates TXT + PNG outputs):
  - `uv run notebooks_py/01_analisis_exploratorio.py`
- Run barrio demographic/economic indicator pipeline (requires Personas por Hogar ZIP in `data/info_geo/`):
  - `uv run notebooks_py/03_indicadores_demograficos_barrio.py`
- Open map and comuna-level analysis notebooks:
  - `notebooks_py/02_carga_datos_mapa.ipynb`
  - `notebooks_py/03_indicadores_ingresos_comuna.ipynb`

## Testing and validation reality in this repo
- There is currently **no automated test suite** (`tests/`, `pytest.ini`, and `pyproject.toml` with test tooling are absent).
- “Single test” equivalent in this project is running a single pipeline entrypoint and validating generated artifacts:
  - `uv run notebooks_py/01_analisis_exploratorio.py`
  - Then check updated files under `outputs/` (for example `reporte_analisis_exploratorio.txt`, `consolidado.txt`, and generated PNGs).

## High-level architecture (big picture)
1. **Data layer (`data/`)**
   - Main business source: `data/Registro mercantil 2025_.xlsx`
   - Geospatial layers:
     - `data/info_geo/geojson_comunas/Comunas.geojson` (comuna maps)
     - ZIP shapefiles for barrio-level demographic enrichment (Personas por Hogar).
2. **Computation layer (`notebooks_py/`)**
   - `01_analisis_exploratorio.py`: batch-style EDA script, column normalization, null/duplicate analysis, chart generation, and text reports.
   - `02_carga_datos_mapa.ipynb`: comuna indicators + geospatial merge + choropleth outputs.
   - `03_indicadores_demograficos_barrio.py`: merges Registro Mercantil with demographic shapefile to derive normalized territorial metrics (for example empresas/1000hab, empleo/1000hab, empleo/hogar).
   - `03_indicadores_ingresos_comuna.ipynb`: additional comuna-level income indicator analysis.
3. **Documentation/methodology layer (`docs/`, `notebooks_py/referencia_*.md`)**
   - `docs/metodologia.md` is the canonical methodology narrative for indicators and assumptions.
   - `docs/diccionario.txt` and `notebooks_py/referencia_Indice_ingresos_operacionales.md` document variables, expected outputs, and interpretation context.
4. **Output layer (`outputs/`)**
   - Generated reports and visual artifacts are first-class deliverables (`*.txt`, `*.png`, and HTML maps).
   - Most code changes in analysis scripts should be validated by regenerated output artifacts.

## Implementation conventions observed in code
- Scripts rely on relative project roots via `Path(__file__).resolve().parent.parent`, so preserve repository layout assumptions.
- Column matching is mostly pattern-based (searching substrings like `ingreso`, `comuna`, `barrio`, `ciiu`, `tama`, `personal`); schema/column-name changes can silently break downstream logic.
- Plot formatting convention uses abbreviated magnitudes (`K`, `M`, `B`) via shared helper functions in analysis scripts.

## Repository-specific guidance from existing agent docs
- `agent/prompts/system_prompt.md` and `agent/README.md` emphasize:
  - Keep methodology/context/docs consistent when indicator logic changes.
  - Keep generated reports in `outputs/` aligned with code and documentation updates.
- `agent/knowledge_base/README.md` indicates methodology guide files should take precedence over short summaries when they conflict.
