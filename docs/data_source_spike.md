# Exploración y auditoría de fuentes ATP

Etapa experimental 1: entrenamiento hasta **2024-12-31**, evaluación sobre **2025**.

## Estado

La descarga, importación local, separación de temporadas y auditoría inicial están ejecutadas. Las tablas son de exploración: todavía no existe un conjunto canónico validado ni un modelo entrenado. La fase 0 sigue abierta por la semántica temporal, las discrepancias y la cobertura de verificación oficial.

## Datos descargados

Las dos bases contienen archivos de partidos de 1968 a 2025. No se descargaron archivos de partidos de 2026. El bloque de rankings de la década de 2020 sí incluye fechas posteriores al corte; la tabla de entrenamiento las excluye.

| Fuente | Filas originales hasta 2025 | Entrenamiento provisional | Evaluación 2025 | Cuarentena temporal |
|---|---:|---:|---:|---:|
| sackmann | 197,940 | 193,526 | 2,862 | 1,552 |
| tml | 197,926 | 193,490 | 2,861 | 1,575 |

Cuarentena temporal significa que la fecha es inválida o que el año de inicio del torneo no coincide con la temporada del archivo. Los eventos que cruzan el cambio de año necesitan fechas reales; no se incorporan al entrenamiento por tener una fecha de torneo anterior al corte. La partición de entrenamiento es provisional: aún incluye anomalías de calidad, abandonos y walkovers; no debe usarse para entrenar modelos.

Rankings hasta el corte: **3,292,949** filas; fecha máxima **2024-12-30**.

## Comparación de fuentes

El emparejamiento usa temporada, código de torneo, ronda y los dos nombres normalizados, independientemente de quién ganó. No utiliza igualdad de IDs entre proveedores ni similitud aproximada de nombres. Las claves ambiguas se excluyen. Las estadísticas se alinean por jugador si el ganador difiere.

- Partidos emparejados en 1968–2024: **173,221**.
- Partidos con al menos un campo comparable diferente: **30,229**.
- Claves únicas sin correspondencia: Sackmann **21,745**; TennisMyLife **21,697**.
- Claves ambiguas sumadas entre fuentes: **47**.

Una discrepancia no demuestra qué proveedor está equivocado. Un registro sin correspondencia puede deberse a nombres distintos, IDs de torneo distintos, ronda o cobertura. Los campos faltantes no cuentan como acuerdos ni discrepancias. Las categorías ATP genéricas de Sackmann no se comparan directamente con ATP 250/500 de TennisMyLife. Las fechas de semana no se equiparan a fechas exactas de partido.

| Campo | Diferencias entre valores presentes |
|---|---:|
| `winner_rank` | 18,329 |
| `loser_rank` | 17,427 |
| `surface` | 3,377 |
| `winner_rank_points` | 2,552 |
| `loser_rank_points` | 2,316 |
| `score` | 1,093 |
| `best_of` | 976 |
| `w_SvGms` | 913 |
| `l_SvGms` | 908 |
| `w_bpSaved` | 463 |
| `w_1stIn` | 367 |
| `l_1stIn` | 361 |
| `minutes` | 357 |
| `w_svpt` | 357 |
| `l_1stWon` | 356 |
| `l_svpt` | 356 |
| `w_1stWon` | 353 |
| `l_2ndWon` | 351 |
| `w_2ndWon` | 349 |
| `w_bpFaced` | 346 |
| `l_bpFaced` | 333 |
| `l_bpSaved` | 329 |
| `w_ace` | 329 |
| `l_ace` | 324 |
| `w_df` | 312 |
| `l_df` | 293 |
| `winner_name` | 14 |

Detalle local reproducible: `data/processed/stage_1_2025/discrepancies.jsonl`. Los errores originales se conservan sin adjudicar ni corregir automáticamente.

## Coherencia interna

Los controles comprueban identidad de participantes, superficie, fecha, formato, ranking positivo y contadores enteros no negativos; también que primeros saques, puntos ganados y puntos de quiebre respeten sus límites. Un formato fuera de 3/5 se marca para revisión: puede corresponder a un formato especial legítimo, no necesariamente a un error.

| Fuente | Regla | Filas señaladas |
|---|---|---:|
| sackmann | `invalid_best_of` | 36 |
| sackmann | `same_player` | 3 |
| sackmann | `invalid_l_bpSaved` | 2 |
| sackmann | `w_second_serve_wins_exceed_opportunities` | 1 |
| tml | `invalid_best_of` | 189 |
| tml | `same_player` | 1 |
| tml | `w_1stWon_exceeds_1stIn` | 12 |
| tml | `l_bpSaved_exceeds_bpFaced` | 2 |
| tml | `w_1stIn_exceeds_svpt` | 1 |
| tml | `w_second_serve_wins_exceed_opportunities` | 3 |
| tml | `l_second_serve_wins_exceed_opportunities` | 1 |

**Ejemplo confirmado de incoherencia compartida:** Machac–Navone, Roland Garros 2024: 135 puntos de saque, 122 primeros saques dentro y 21 puntos ganados con segundo saque. 135 − 122 = 13, de modo que 21 supera las oportunidades disponibles. Ambas bases contienen esa combinación. No se ha determinado cuál es el campo incorrecto ni se ha aplicado una corrección.

## Comprobaciones oficiales de ATP

Muestra inicial: cuatro finales de Grand Slam de 2024 y el walkover Moutet–Struff de París 2024. Se cotejaron ganador y marcador con crónicas de ATP; en Wimbledon también la duración de 147 minutos. Son comprobaciones puntuales verificadas al 2026-10-07, no una tercera base histórica completa ni una garantía para las estadísticas de los demás partidos. En el walkover, Sackmann invierte el ganador: ATP e ITF confirman que Moutet avanzó. El caso se documenta en `docs/data_issues.md`; los originales permanecen intactos.

| Fuente contrastada | Torneo ATP | Resultado | Referencia oficial |
|---|---|---|---|
| sackmann | 580 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/medvedev-sinner-australian-open-2024-final) |
| tml | 580 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/medvedev-sinner-australian-open-2024-final) |
| sackmann | 520 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/alcaraz-zverev-roland-garros-2024-final) |
| tml | 520 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/alcaraz-zverev-roland-garros-2024-final) |
| sackmann | 540 / 2024 | Coincide | [ATP](https://www.atptour.com/es/news/wimbledon-2024-domingo-final-alcaraz-djokovic) |
| tml | 540 / 2024 | Coincide | [ATP](https://www.atptour.com/es/news/wimbledon-2024-domingo-final-alcaraz-djokovic) |
| sackmann | 560 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/sinner-fritz-us-open) |
| tml | 560 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/sinner-fritz-us-open) |
| sackmann | 96 / 2024 | Revisar | [ATP](https://www.atptour.com/en/news/zverev-machac-paris-olympics-tuesday-2024) |
| tml | 96 / 2024 | Coincide | [ATP](https://www.atptour.com/en/news/zverev-machac-paris-olympics-tuesday-2024) |

## Cobertura por año

Estadísticas completas significa que los 18 contadores de saque están presentes; no significa que sean correctos. Los conteos de 2025 describen disponibilidad; no son métricas de evaluación ni se usan para ajustar un modelo.

| Año | Sackmann: partidos | Con estadísticas completas | TML: partidos | Con estadísticas completas |
|---|---:|---:|---:|---:|
| 1968 | 4,377 | 0 | 3,723 | 0 |
| 1969 | 3,165 | 0 | 3,596 | 0 |
| 1970 | 3,287 | 0 | 3,236 | 0 |
| 1971 | 3,640 | 0 | 3,791 | 0 |
| 1972 | 3,617 | 0 | 3,813 | 0 |
| 1973 | 4,327 | 0 | 4,296 | 0 |
| 1974 | 4,200 | 0 | 4,193 | 0 |
| 1975 | 4,164 | 0 | 4,129 | 0 |
| 1976 | 3,979 | 0 | 3,952 | 0 |
| 1977 | 4,140 | 0 | 4,168 | 0 |
| 1978 | 3,852 | 0 | 3,865 | 0 |
| 1979 | 3,959 | 0 | 3,961 | 0 |
| 1980 | 4,013 | 0 | 3,909 | 0 |
| 1981 | 3,910 | 0 | 3,916 | 0 |
| 1982 | 4,070 | 0 | 4,074 | 0 |
| 1983 | 3,489 | 0 | 3,464 | 0 |
| 1984 | 3,248 | 0 | 3,222 | 0 |
| 1985 | 3,392 | 0 | 3,395 | 0 |
| 1986 | 3,249 | 0 | 3,251 | 0 |
| 1987 | 3,546 | 0 | 3,550 | 0 |
| 1988 | 3,733 | 0 | 3,733 | 0 |
| 1989 | 3,583 | 0 | 3,583 | 0 |
| 1990 | 3,681 | 0 | 3,683 | 0 |
| 1991 | 3,727 | 3,236 | 3,727 | 3,293 |
| 1992 | 3,792 | 3,373 | 3,792 | 3,492 |
| 1993 | 3,890 | 3,483 | 3,890 | 3,530 |
| 1994 | 3,938 | 3,480 | 3,938 | 3,562 |
| 1995 | 3,800 | 3,375 | 3,800 | 3,435 |
| 1996 | 3,774 | 3,325 | 3,774 | 3,347 |
| 1997 | 3,623 | 3,224 | 3,623 | 3,236 |
| 1998 | 3,591 | 3,225 | 3,591 | 3,223 |
| 1999 | 3,334 | 2,943 | 3,334 | 2,968 |
| 2000 | 3,378 | 2,942 | 3,378 | 2,961 |
| 2001 | 3,307 | 2,969 | 3,311 | 2,984 |
| 2002 | 3,213 | 2,839 | 3,213 | 2,873 |
| 2003 | 3,218 | 2,809 | 3,218 | 2,870 |
| 2004 | 3,288 | 2,880 | 3,288 | 2,896 |
| 2005 | 3,264 | 2,912 | 3,263 | 2,924 |
| 2006 | 3,267 | 2,908 | 3,267 | 2,924 |
| 2007 | 3,192 | 2,808 | 3,192 | 2,838 |
| 2008 | 3,123 | 2,764 | 3,123 | 2,778 |
| 2009 | 3,085 | 2,726 | 3,085 | 2,742 |
| 2010 | 3,030 | 2,686 | 3,030 | 2,689 |
| 2011 | 3,015 | 2,687 | 3,015 | 2,687 |
| 2012 | 3,009 | 2,680 | 3,009 | 2,617 |
| 2013 | 2,944 | 2,613 | 2,944 | 2,614 |
| 2014 | 2,901 | 2,574 | 2,901 | 2,575 |
| 2015 | 2,943 | 2,620 | 2,945 | 2,622 |
| 2016 | 2,941 | 2,916 | 2,970 | 2,920 |
| 2017 | 2,911 | 2,870 | 2,936 | 2,873 |
| 2018 | 2,897 | 2,862 | 2,926 | 2,859 |
| 2019 | 2,806 | 2,694 | 2,806 | 2,679 |
| 2020 | 1,462 | 1,415 | 1,466 | 1,388 |
| 2021 | 2,733 | 2,636 | 2,735 | 2,637 |
| 2022 | 2,917 | 2,745 | 2,918 | 2,746 |
| 2023 | 2,986 | 2,815 | 2,995 | 2,814 |
| 2024 | 3,076 | 3,015 | 3,076 | 3,014 |
| 2025 | 2,944 | 2,685 | 2,944 | 2,751 |

Los esquemas observados, los valores de superficie/categoría, los faltantes por columna y año y los casos de incoherencia están en `data/processed/stage_1_2025/audit.json`.

## Límites temporales y decisiones pendientes

- `tourney_date` es la semana o inicio del torneo, no la fecha real del partido.
- `match_num` no garantiza orden cronológico y puede numerar la final antes que las primeras rondas.
- Falta reconstruir fechas, horarios o una política conservadora de disponibilidad de resultados antes de ejecutar Elo secuencial.
- Las bases se descargaron en 2026 y pueden contener correcciones posteriores; no son snapshots publicados antes de cada partido histórico.
- La tabla `players_snapshot` contiene metadatos de la descarga actual y no es una fuente histórica validada de variables predictivas.
- Quedan pendientes correspondencias de identidades/torneos, resolución de discrepancias y clasificación de abandonos y walkovers.
- La independencia total de origen entre proveedores no está probada. La coincidencia nunca se interpreta como certeza.
- No se entrenó ni evaluó ningún modelo. `temporal_ready` permanece en `false`.
