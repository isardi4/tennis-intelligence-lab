"""Informes en español generados a partir de resultados de la auditoría."""
from pathlib import Path


def write_spike_report(audit: dict, partitions: dict, path: Path) -> None:
    cutoff = audit["cutoff_year"]
    lines = ["# Exploración y auditoría de fuentes ATP", "",
             f"Etapa experimental 1: entrenamiento hasta **{cutoff}-12-31**, evaluación sobre **{cutoff + 1}**.", "",
             "## Estado", "",
             "La descarga, importación local, separación de temporadas y auditoría inicial están ejecutadas. "
             "Las tablas son de exploración: todavía no existe un conjunto canónico validado ni un modelo entrenado. "
             "La fase 0 sigue abierta por la semántica temporal, las discrepancias y la cobertura de verificación oficial.", "",
             "## Datos descargados", "",
             "Las dos bases contienen archivos de partidos de 1968 a 2025. No se descargaron archivos de partidos de 2026. "
             "El bloque de rankings de la década de 2020 sí incluye fechas posteriores al corte; la tabla de entrenamiento las excluye.", "",
             "| Fuente | Filas originales hasta 2025 | Entrenamiento provisional | Evaluación 2025 | Cuarentena temporal |",
             "|---|---:|---:|---:|---:|"]
    for source, profile in audit["profiles"].items():
        n = partitions[source]
        total = sum(y["rows"] for y in profile["years"])
        lines.append(f"| {source} | {total:,} | {n.get('train', 0):,} | {n.get('evaluation', 0):,} | {n.get('quarantine', 0):,} |")
    lines += ["", "Cuarentena temporal significa que la fecha es inválida o que el año de inicio del torneo no coincide con la temporada del archivo. "
              "Los eventos que cruzan el cambio de año necesitan fechas reales; no se incorporan al entrenamiento por tener una fecha de torneo anterior al corte. "
              "La partición de entrenamiento es provisional: aún incluye anomalías de calidad, abandonos y walkovers; no debe usarse para entrenar modelos.", "",
              f"Rankings hasta el corte: **{partitions['rankings']['rows']:,}** filas; fecha máxima **{partitions['rankings']['max_date']}**.", "",
              "## Comparación de fuentes", "",
              "El emparejamiento usa temporada, código de torneo, ronda y los dos nombres normalizados, independientemente de quién ganó. "
              "No utiliza igualdad de IDs entre proveedores ni similitud aproximada de nombres. Las claves ambiguas se excluyen. "
              "Las estadísticas se alinean por jugador si el ganador difiere.", ""]
    counts = audit["comparison"]["counts"]
    lines += [f"- Partidos emparejados en 1968–{cutoff}: **{counts.get('matched', 0):,}**.",
              f"- Partidos con al menos un campo comparable diferente: **{counts.get('matches_with_differences', 0):,}**.",
              f"- Claves únicas sin correspondencia: Sackmann **{counts.get('sackmann_unmatched', 0):,}**; TennisMyLife **{counts.get('tml_unmatched', 0):,}**.",
              f"- Claves ambiguas sumadas entre fuentes: **{counts.get('ambiguous_keys', 0):,}**.", "",
              "Una discrepancia no demuestra qué proveedor está equivocado. Un registro sin correspondencia puede deberse a nombres distintos, IDs de torneo distintos, ronda o cobertura. "
              "Los campos faltantes no cuentan como acuerdos ni discrepancias. Las categorías ATP genéricas de Sackmann no se comparan directamente con ATP 250/500 de TennisMyLife. "
              "Las fechas de semana no se equiparan a fechas exactas de partido.", "",
              "| Campo | Diferencias entre valores presentes |", "|---|---:|"]
    for field, value in sorted(audit["comparison"]["differences_by_field"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{field}` | {value:,} |")
    lines += ["", "Detalle local reproducible: `data/processed/stage_1_2025/discrepancies.jsonl`. "
              "Los errores originales se conservan sin adjudicar ni corregir automáticamente.", "",
              "## Coherencia interna", "",
              "Los controles comprueban identidad de participantes, superficie, fecha, formato, ranking positivo y contadores enteros no negativos; "
              "también que primeros saques, puntos ganados y puntos de quiebre respeten sus límites. Un formato fuera de 3/5 se marca para revisión: "
              "puede corresponder a un formato especial legítimo, no necesariamente a un error.", "",
              "| Fuente | Regla | Filas señaladas |", "|---|---|---:|"]
    for source, profile in audit["profiles"].items():
        for rule, value in profile["internal_issues"].items():
            lines.append(f"| {source} | `{rule}` | {value} |")
    lines += ["", "**Ejemplo confirmado de incoherencia compartida:** Machac–Navone, Roland Garros 2024: "
              "135 puntos de saque, 122 primeros saques dentro y 21 puntos ganados con segundo saque. "
              "135 − 122 = 13, de modo que 21 supera las oportunidades disponibles. Ambas bases contienen esa combinación. "
              "No se ha determinado cuál es el campo incorrecto ni se ha aplicado una corrección.", "",
              "## Comprobaciones oficiales de ATP", "",
              "Muestra inicial: cuatro finales de Grand Slam de 2024 y el walkover Moutet–Struff de París 2024. Se cotejaron ganador y marcador con crónicas de ATP; "
              "en Wimbledon también la duración de 147 minutos. Son comprobaciones puntuales verificadas al 2026-10-07, "
              "no una tercera base histórica completa ni una garantía para las estadísticas de los demás partidos. "
              "En el walkover, Sackmann invierte el ganador: ATP e ITF confirman que Moutet avanzó. "
              "El caso se documenta en `docs/data_issues.md`; los originales permanecen intactos.", "",
              "| Fuente contrastada | Torneo ATP | Resultado | Referencia oficial |", "|---|---|---|---|"]
    for item in audit["official_checks"]:
        status = "Coincide" if item["passed"] else "Revisar"
        lines.append(f"| {item['source']} | {item['tournament_code']} / {item['season']} | {status} | [ATP]({item['source_url']}) |")
    lines += ["", "## Cobertura por año", "",
              "Estadísticas completas significa que los 18 contadores de saque están presentes; no significa que sean correctos. "
              "Los conteos de 2025 describen disponibilidad; no son métricas de evaluación ni se usan para ajustar un modelo.", "",
              "| Año | Sackmann: partidos | Con estadísticas completas | TML: partidos | Con estadísticas completas |", "|---|---:|---:|---:|---:|"]
    a = {y["year"]: y for y in audit["profiles"]["sackmann"]["years"]}
    b = {y["year"]: y for y in audit["profiles"]["tml"]["years"]}
    for year in sorted(a.keys() | b.keys()):
        left, right = a.get(year, {}), b.get(year, {})
        lines.append(f"| {year} | {left.get('rows', 0):,} | {left.get('complete_stats_rows', 0):,} | {right.get('rows', 0):,} | {right.get('complete_stats_rows', 0):,} |")
    lines += ["", "Los esquemas observados, los valores de superficie/categoría, los faltantes por columna y año y los casos de incoherencia "
              "están en `data/processed/stage_1_2025/audit.json`.", "",
              "## Límites temporales y decisiones pendientes", "",
              "- `tourney_date` es la semana o inicio del torneo, no la fecha real del partido.",
              "- `match_num` no garantiza orden cronológico y puede numerar la final antes que las primeras rondas.",
              "- Falta reconstruir fechas, horarios o una política conservadora de disponibilidad de resultados antes de ejecutar Elo secuencial.",
              "- Las bases se descargaron en 2026 y pueden contener correcciones posteriores; no son snapshots publicados antes de cada partido histórico.",
              "- La tabla `players_snapshot` contiene metadatos de la descarga actual y no es una fuente histórica validada de variables predictivas.",
              "- Quedan pendientes correspondencias de identidades/torneos, resolución de discrepancias y clasificación de abandonos y walkovers.",
              "- La independencia total de origen entre proveedores no está probada. La coincidencia nunca se interpreta como certeza.",
              "- No se entrenó ni evaluó ningún modelo. `temporal_ready` permanece en `false`.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))
