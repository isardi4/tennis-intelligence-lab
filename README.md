# Tennis Intelligence Lab

**[Abrir el explorador público](https://isardi4.github.io/tennis-intelligence-lab/)** · [Repositorio](https://github.com/isardi4/tennis-intelligence-lab)

**Para seguir el proyecto, empezá por [Estado y checklist por fase](ESTADO_DEL_PROYECTO.md).** Ahí está lo terminado, lo pendiente y el próximo paso, explicado sin necesidad de leer los informes técnicos.

Plataforma de análisis y predicción de tenis ATP. El objetivo es estimar probabilidades de victoria, explicar los factores del modelo y simular torneos usando solo información disponible antes de cada predicción.

El [plan maestro en español](TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md) es la referencia estratégica. El [backup original en inglés](TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.en.md) conserva el plan anterior a la revisión del esquema experimental.

## Evaluación acordada

| Etapa experimental | Entrenamiento y ajuste hasta | Evaluación | Estado |
|---|---|---|---|
| 1 | 2024-12-31 | Temporada 2025 | Auditoría de datos en curso |
| 2 | 2025-12-31 | Temporada 2026 | Después de revisar la primera etapa |

Primero se registra el resultado inicial sobre 2025. Las mejoras inspiradas por sus errores se consideran desarrollo; una nueva medición sobre ese mismo año no es una prueba independiente. El modelo de la segunda etapa se fija antes de evaluar 2026.

Cada etapa tendrá dos modos separados: información totalmente congelada y actualización histórica secuencial de Elo/rendimiento con parámetros del modelo congelados. Las etapas experimentales no cambian la numeración de las fases de ingeniería del plan.

## Objetivos

1. Construir un conjunto histórico confiable de partidos, jugadores y rankings ATP, contrastando fuentes públicas.
2. Reconstruir el estado previo a cada partido sin utilizar información futura.
3. Comparar ranking ATP, Elo general y Elo por superficie antes de entrenar regresión logística.
4. Producir probabilidades calibradas y explicaciones basadas en variables reales del modelo.
5. Simular cuadros y calcular probabilidades de avance, título y dificultad del camino.
6. Reproducir los resultados con datos, configuración y versiones de código identificables.

## Avance actual

**Fase de ingeniería actual: 0, exploración y auditoría de fuentes.**

- Descargados y verificados 67 archivos de Sackmann archivado y 58 CSV ATP de TennisMyLife, con partidos de 1968 a 2025.
- Tablas locales de exploración en DuckDB y Parquet; entrenamiento provisional hasta 2024 separado de evaluación 2025.
- Rankings exportados hasta el corte de 2024.
- Comparación de ambas bases y controles internos de calidad ejecutados.
- Comprobaciones oficiales puntuales de cuatro finales de Grand Slam de 2024 y un walkover olímpico.
- Muestra temporal de 9 partidos contrastados con evidencia oficial y vinculados a ambas bases.
- Pruebas automatizadas del corte, disponibilidad temporal, integridad de archivos y coherencia de estadísticas.

**Todavía no hay un modelo entrenado ni un backtest válido por partido.** Las bases informan la semana del torneo; falta reconstruir la fecha y disponibilidad de cada resultado. También quedan pendientes la resolución de discrepancias, correspondencias de identidades y clasificación de abandonos/walkovers. La partición `train` es de exploración y todavía contiene registros que necesitan limpieza.

Hay dos bases descargadas y una referencia oficial puntual, no tres bases completas independientes. El espejo de Sackmann no se cuenta como otra fuente.

## Ejecutar localmente

Requiere Python 3.11 o posterior y `curl`. Desde la raíz del proyecto:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
.venv/bin/python scripts/download_data.py --source sackmann
.venv/bin/python scripts/download_data.py --source tml
.venv/bin/python scripts/download_data.py --source mcp
.venv/bin/python scripts/download_data.py --source challenger
.venv/bin/python scripts/build_dataset.py
.venv/bin/python scripts/audit_temporal.py
.venv/bin/python scripts/audit_profile_inputs.py
.venv/bin/python scripts/audit_charting.py
.venv/bin/python scripts/build_style_pilot.py
.venv/bin/python scripts/build_ranked_profiles.py
.venv/bin/python scripts/build_similarities.py
.venv/bin/python scripts/audit_similarity_stability.py
.venv/bin/python -m pytest -q
```

Las descargas conservan los originales y verifican hashes. Sackmann está fijado a un commit; TennisMyLife publica archivos vivos y debe coincidir con el snapshot registrado. Si cambian, el proceso falla y exige revisar la nueva versión. Los datos quedan excluidos de Git.

La construcción escribe `data/processed/stage_1_2025/`: base `exploration.duckdb`, tablas Parquet, `audit.json`, `discrepancies.jsonl` y un manifiesto de ejecución. También actualiza el informe de exploración. La segunda etapa aún no está habilitada en la CLI.

## Documentación y seguimiento

- [Estado y checklist por fase — documento principal de seguimiento](ESTADO_DEL_PROYECTO.md).
- [Registro de trabajo paso a paso](docs/work_log.md).
- [Informe de exploración y auditoría](docs/data_source_spike.md).
- [Fuentes, licencias y cobertura](docs/data_sources.md).
- [Diccionario inicial de datos](docs/data_dictionary.md).
- [Casos de calidad de datos y evidencias](docs/data_issues.md).
- [Decisión sobre evaluación en dos etapas](docs/decisions/ADR-001-evaluacion-en-dos-etapas.md).

**Próximo hito:** resolver identidades, anomalías y cronología para construir el conjunto canónico y después calcular probabilidades Elo históricamente válidas.

El MVP permitirá seleccionar dos jugadores y una fecha histórica para obtener una probabilidad previa al partido con una explicación. La V1 principal añadirá simulación de cuadros y una interfaz. WTA, dobles, apuestas, video y agentes de IA quedan fuera del alcance inicial.


## Explorador visual para probar el proyecto

Abrí [`docs/index.html`](docs/index.html) directamente en el navegador. Permite buscar entre 350 jugadores, comparar perfiles básicos o de golpes y seleccionar vecinos explicados con su muestra. La superficie y circuito aplican a métricas básicas; los golpes tienen perfil global. No ofrece probabilidades de victoria.

También puede servirse localmente:

```bash
.venv/bin/python -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Abrir `http://127.0.0.1:8765/`. No requiere instalar JavaScript ni un backend. El snapshot es un agregado derivado incluido con la página, no una descarga de archivos originales. Para regenerarlo después de construir perfiles, similitudes y estabilidad:

```bash
.venv/bin/python scripts/export_web_snapshot.py
```

### Publicar en GitHub Pages

La página está preparada para publicar desde `docs/`: subir los archivos del proyecto al repositorio elegido, ir a **Settings → Pages → Deploy from a branch**, elegir la rama y carpeta **/docs**, y guardar. [Instrucciones oficiales](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Los recursos usan rutas relativas y funcionan en la URL de un proyecto. `.nojekyll` conserva el sitio estático.

Repositorio del proyecto: https://github.com/isardi4/tennis-intelligence-lab. Se inicializó Git dentro del proyecto, independiente del directorio padre. GitHub Pages configurado desde `main:/docs`, con HTTPS obligatorio. URL del explorador: https://isardi4.github.io/tennis-intelligence-lab/. Cada push a main que actualice docs publica automáticamente los cambios.

Los agregados derivados publicados en el snapshot se ofrecen bajo CC BY-NC-SA 4.0, con atribución a Jeff Sackmann, colaboradores del Match Charting Project y el espejo archivado. Uso no comercial; la página incluye los enlaces de atribución/licencia.
