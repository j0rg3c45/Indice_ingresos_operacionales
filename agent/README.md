# Agent - Notas del entorno

## Herramientas disponibles en este PC

- **uv** — Gestor de paquetes y entornos Python (instalado y disponible en PATH)
  - Usar `uv pip install` en lugar de `pip install`
  - Usar `uv venv` para crear entornos virtuales
  - Usar `uvx` para ejecutar herramientas sin instalarlas globalmente
  - Usar `uv run` para ejecutar scripts con el entorno activo

## Comandos rapidos

```bash
# Instalar dependencias del proyecto
uv pip install -r requirements.txt

# Ejecutar script de analisis
uv run notebooks_py/01_analisis_exploratorio.py
```

## Dependencias instaladas

- pandas, openpyxl (lectura de datos)
- numpy (calculo numerico)
- matplotlib, seaborn (visualizacion)
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
