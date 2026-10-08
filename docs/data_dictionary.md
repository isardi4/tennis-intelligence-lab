# Diccionario inicial de datos

Este documento describe las tablas de exploración, no un esquema definitivo de entrenamiento. Las columnas originales se conservan para auditar y adaptar cada fuente; no deben propagarse como dependencias de los modelos.

## Partidos: `sackmann_matches` y `tml_matches`

| Campo | Significado | Precaución |
|---|---|---|
| `source_file` | Archivo original de la fila | Procedencia, no predictor |
| `source_season` | Año del archivo anual | No se deduce de la fecha de inicio |
| `tourney_id` | Identificador de torneo de la fuente | Los proveedores pueden usar códigos distintos |
| `tourney_name` | Nombre de torneo | No usar como clave de identidad |
| `tourney_date` | Fecha original `YYYYMMDD` | Normalmente semana o inicio del torneo |
| `tournament_start_date` | Fecha original interpretada como DATE | No es `match_date` ni `available_at` |
| `dataset_partition` | `train`, `evaluation`, `quarantine` o `future` | Separación provisional, no habilitación de entrenamiento |
| `surface` | Hard, Clay, Grass, Carpet o faltante | Puede discrepar entre fuentes |
| `draw_size` | Tamaño del cuadro | Puede estar redondeado a una potencia de dos |
| `tourney_level` | Categoría según proveedor | Sackmann `A` no distingue siempre ATP 250/500 |
| `indoor` | Interior/exterior, cuando está presente | Campo adicional de TennisMyLife |
| `match_num` | Número de registro del partido | No garantiza orden cronológico |
| `winner_id`, `loser_id` | IDs de cada participante en su fuente | Sackmann y ATP/TML usan sistemas distintos |
| `winner_name`, `loser_name` | Nombres de participantes | Exigen correspondencias verificadas |
| `winner_seed`, `loser_seed` | Cabeza de serie | Vacío significa desconocido o no aplicable |
| `winner_entry`, `loser_entry` | Vía de ingreso: Q, WC, LL, etc. | No garantiza estado previo al torneo |
| `winner_hand`, `loser_hand` | Mano de saque | Atributo de la fuente |
| `winner_ht`, `loser_ht` | Altura en cm | No se ha demostrado disponibilidad histórica |
| `winner_ioc`, `loser_ioc` | Código de país | Puede cambiar durante la carrera |
| `winner_age`, `loser_age` | Edad informada por fuente | Sackmann la calcula a la fecha de torneo |
| `winner_rank`, `loser_rank` | Ranking a la fecha del torneo o último previo | No sustituye una unión histórica por fecha de publicación |
| `winner_rank_points`, `loser_rank_points` | Puntos de ranking informados | Faltantes no equivalen a cero |
| `score` | Marcador desde la perspectiva del ganador | Incluye formatos especiales, RET, W/O y otros estados |
| `best_of` | Formato al mejor de 3 o 5 sets, normalmente | Otros formatos requieren clasificación, no eliminación automática |
| `round` | Ronda: R128, R64, R32, R16, QF, SF, F, RR, etc. | Códigos y cuadros pueden diferir |
| `minutes` | Duración del partido | Resultado posterior al partido, nunca predictor del mismo encuentro |

### Contadores de saque

Cada sufijo existe con prefijo `w_` para el ganador y `l_` para el perdedor. Los datos originales son contadores; los porcentajes todavía no se generan.

| Sufijo | Significado | Control |
|---|---|---|
| `ace` | Aces | Entero no negativo; no supera `svpt` |
| `df` | Dobles faltas | Entero no negativo; no supera `svpt` |
| `svpt` | Puntos de saque | Entero no negativo |
| `1stIn` | Primeros saques dentro | No supera `svpt` |
| `1stWon` | Puntos ganados con primer saque | No supera `1stIn` |
| `2ndWon` | Puntos ganados con segundo saque | No supera `svpt - 1stIn` |
| `SvGms` | Juegos de saque | Entero no negativo |
| `bpSaved` | Puntos de quiebre salvados | No supera `bpFaced` |
| `bpFaced` | Puntos de quiebre enfrentados | Entero no negativo |

Ganador, marcador, duración y estadísticas del partido son información posterior a su resultado. Para modelar el mismo partido solo pueden emplearse estadísticas de encuentros anteriores que ya hubieran terminado. Las tablas actuales no son tablas de variables predictivas.

## Rankings: `rankings`

| Campo canónico | Campo original | Tipo | Significado |
|---|---|---|---|
| `ranking_date` | `ranking_date` | DATE | Fecha del ranking informado |
| `source_player_id` | `player` | VARCHAR | ID Sackmann |
| `rank` | `rank` | INTEGER | Puesto |
| `ranking_points` | `points` | INTEGER nullable | Puntos |

Solo se exportan registros con `ranking_date <= training_cutoff`. La validación de unicidad y de la disponibilidad exacta de la publicación queda pendiente para la fase canónica.

## Jugadores: `players_snapshot`

| Campo | Origen | Tipo |
|---|---|---|
| `source_player_id` | `player_id` | VARCHAR |
| `first_name` | `name_first` | VARCHAR |
| `last_name` | `name_last` | VARCHAR |
| `hand` | `hand` | VARCHAR |
| `birth_date` | `dob` | DATE nullable |
| `country_code` | `ioc` | VARCHAR |
| `height_cm` | `height` | INTEGER nullable |
| `wikidata_id` | `wikidata_id` | VARCHAR nullable |

Es una copia de los metadatos descargados actualmente. No tiene una fecha histórica `available_at` comprobada. Las fechas o alturas no interpretables quedan nulas en la tabla de exploración; el archivo original permanece intacto.

## Auditoría y procedencia

- `manifest.json`: URL, revisión, fecha de descarga, tamaño, SHA-256 y hash Git de cada archivo.
- `audit.json`: esquemas por año, filas, faltantes por columna, cobertura de estadísticas, superficies, categorías, incoherencias y comparación entre fuentes.
- `discrepancies.jsonl`: clave de emparejamiento y los valores que difieren en ambas fuentes.
- `configs/official_checks.json`: hechos contrastados con páginas oficiales y referencias.

Los faltantes se mantienen como desconocidos. Ninguna incoherencia se corrige silenciosamente y todavía no se ha creado una correspondencia definitiva entre IDs de proveedores.


## Catálogo inicial de perfiles

`src/tennis_lab/profiles.py` extrae numerador y denominador de nueve medidas: `ace_rate`, `double_fault_rate` (dobles faltas / puntos de saque), `first_serve_in_rate`, `first_serve_points_won`, `second_serve_points_won`, `serve_points_won`, `first_serve_return_points_won`, `second_serve_return_points_won` y `return_points_won`. La devolución se calcula desde los contadores de saque del oponente. Los puntos ganados al segundo incluyen el efecto de dobles faltas conforme a los contadores de la fuente.

Se excluyen conservadoramente filas con incoherencias detectadas, marcador vacío, walkover, abandono o descalificación. Una oportunidad nula o un dato ausente no genera una tasa cero. Estos controles son preliminares: no resuelven discrepancias externas, identidades ni fechas. Las sumas deben realizarse sobre partidos únicos y temporalmente elegibles antes de dividir.

Auditoría ejecutada: `.venv/bin/python scripts/audit_profile_inputs.py`; salida local `profile_input_audit.json`. En 2024 hay 6.152 observaciones jugador-partido por proveedor: 5.866 con cada métrica en Sackmann y 5.842 en TennisMyLife (aproximadamente 95,35 % y 94,96 %). No sumar ambos proveedores ni interpretar estas cifras como cobertura de fechas verificadas. No se generaron perfiles por jugador ni etiquetas de estilo.


## Perfiles descriptivos piloto MCP — 2022–2024

Ejecución: `.venv/bin/python scripts/build_style_pilot.py`; salida local `style_pilot.json`. Ocho perfiles: dos jugadores por todas las superficies/dura/arcilla/césped. Los 130 metadatos de Alcaraz aportan 129 encuentros con estadísticas; los once de Fognini aportan once. Se verifican hashes, corte, duplicados de filas agregadas, contadores no negativos, numeradores dentro de denominadores y conservación de puntos ganados entre jugadores. Un fallo de contadores retira las contribuciones del partido en ese perfil. No hubo fallos de estos controles en la ejecución piloto.

Once medidas: proporción de golpes `Fside` y `Bside` sobre `Total`; winners y errores no forzados de cada lado sobre golpes de ese lado; puntos ganados en la red sobre oportunidades de red; puntos ganados en las cuatro bandas de intercambios `1-3`, `4-6`, `7-9`, `10`. Las bandas se usan una sola vez, sin sumar las subdivisiones de servicio. `pl1_won`/`pl2_won` se asignan según Player 1/2 de los metadatos, no según ganador o nombre ordenado. La convención [documentada por MCP](https://github.com/JeffSackmann/tennis_MatchChartingProject/blob/master/data_dictionary.txt) incluye saque y excluye golpe de error para rallyCount.

Los perfiles guardan numerador, denominador y cantidad de partidos por medida. Proporciones ponderadas por oportunidades, sin promediar porcentajes por partido. Ausencia de datos produce perfil vacío. Lados derecha/revés incluyen las categorías agregadas de MCP, no solo golpes de fondo; su interpretación detallada aún requiere revisar las instrucciones y cotejar anotaciones.

Son resúmenes retrospectivos del snapshot, no evidencia de que el charting estaba publicado antes de 2025. No hay calificación de agresividad, ajuste por rival, corrección por selección ni probabilidad de victoria. Muestras por superficie: Alcaraz 71 dura/45 arcilla/14 césped en metadatos; Fognini cuatro/siete/cero. No atribuir el porcentaje de red a calidad pura del jugador ni confundir perfil descriptivo con ventaja causal de estilo.


## Universo top 500 y piloto top 350

Constructor: `scripts/build_ranked_profiles.py`. Ranking seleccionado como último snapshot no posterior a 31/12/2024: 30/12/2024, exactamente 500 jugadores con rank ≤500, de los que 350 tienen rank ≤350. Ventana descriptiva 2022–2024. Verifica integridad de rankings, directorio de jugadores y tres CSV ATP, además de las tablas MCP. No usa rankings ni resultados de 2025.

Identidad básica por ID Sackmann; nombre del directorio actual solo como etiqueta, sin usar atributos actuales como variables. Correspondencias MCP por nombre normalizado exacto, con alias de encuentros anteriores al corte; candidatos múltiples o nombres compartidos entre IDs quedan sin vínculo. No hay coincidencias difusas y una correspondencia exacta no prueba identidad.

Métricas básicas se agregan por oportunidades y superficie con controles de `profile_observations`; todavía falta deduplicación canónica y contraste de discrepancias entre proveedores. Universo: 356 con alguna métrica básica y 280 candidatos MCP. Piloto: 296 con alguna métrica básica, 250 candidatos MCP y 250 con alguna métrica de estilo. De estos, 92 tienen al menos diez partidos de `Fside_shot_share`; umbral descriptivo, no criterio validado de confianza.

Artefactos locales: `top500_coverage.json` (roster, métricas básicas y correspondencias); `top350_profiles.json` (350 jugadores, perfiles básicos y de estilo por superficie); `top350_styles.json`; `ranked_profiles_summary.json`. `ready_for_training=false`. La población ATP objetivo no tiene cubierta toda su actividad: falta Challenger. La ausencia de registros no significa que el jugador no disputó partidos. No usar el top de diciembre de 2024 para seleccionar la población de una validación anterior sin reconstruir su ranking contemporáneo.


## Ampliación Challenger del universo clasificado

`basic_profile_by_level` conserva contribuciones separadas de ATP, Challenger_main y Challenger_qualifying, con numeradores/denominadores/partidos por superficie. `basic_profile` es la suma descriptiva, no un ajuste por dificultad. Comprobada reconciliación de las contribuciones para los 500 jugadores.

Tras incorporar Challenger: top 350 pasa de 296 a 350 jugadores con datos básicos; top 500 de 356 a 500. Los 500 tienen las nueve métricas en agregación All; 349/350 y 495/500 tienen al menos diez partidos de `serve_points_won`, mínimo cinco. Esto no garantiza esa muestra en cada superficie ni que los resultados sean comparables entre circuitos. Las tablas de estilo conservan cobertura MCP; las identidades candidatas siguen pendientes de revisión. Artefactos del constructor regenerados, `ready_for_training=false`.


## Similitudes exploratorias del top 350

`scripts/build_similarities.py` produce `player_similarities.json` y registra el hash del archivo de perfiles. Cada vista conserva las medias/desviaciones utilizadas. Se estandarizan las métricas con la población elegible de cada vista, restringida al piloto 2022–2024; para un backtest anterior deberán recalcularse sin datos futuros y con población contemporánea. No se usa 2025.

Saque/devolución: siete tasas (aces, dobles faltas, primeros dentro, puntos ganados al primero/segundo y devolución contra primero/segundo), separadas por ATP/Challenger principal/Challenger clasificación. Golpes: seis medidas MCP (proporción Fside, winners/errores Fside/Bside y conversión de puntos en red); no se usa Bside share para evitar duplicar su relación con Fside. Las medidas siguen mezclando tendencia y rendimiento y no son un embedding táctico validado.

Distancia: raíz de la media de diferencias estandarizadas al cuadrado. No es porcentaje de similitud ni probabilidad. Se exigen al menos diez partidos y denominador positivo en todas las métricas seleccionadas, sin rellenar faltantes ni comparar subconjuntos distintos por pareja. Características constantes se descartan; sin características activas no se generan vecinos. Top cinco por jugador, sin incluirse a sí mismo. Se guardan tres características cercanas, principal diferencia y mínimo de partidos del vecino.

Poblaciones All: ATP 187, Challenger principal 307, clasificación 179 y MCP 92. La estandarización y distancia se interpretan dentro de cada vista, no entre vistas. Identidades siguen candidatas, muestras selectivas, sin ajuste por oponente ni validación de estabilidad; no hay efecto táctico ni predicción y `ready_for_prediction=false`.


## Diagnóstico de estabilidad de similitudes

`scripts/audit_similarity_stability.py` retira un año por vez (2022, 2023, 2024), recalcula perfiles básicos y MCP, y compara vecinos sobre la intersección de jugadores con al menos diez partidos por métrica en ambas ventanas. Se separan las mismas vistas de circuito y superficie. Solo con seis o más jugadores comparables puede medirse retención de los cinco vecinos; datos insuficientes y características constantes no equivalen a estabilidad cero.

Se informa cuántos de los cinco vecinos se conservan, su mediana y cantidad con al menos tres conservados. Tres de cinco es una regla exploratoria de sensibilidad, no un nivel de confianza validado. Las ventanas comparten dos años, por lo que este diagnóstico no es validación independiente ni bootstrap. Cambios pueden reflejar evolución real, oposición distinta o selección de partidos.

El universo fijo del top 350 al cierre de 2024 sirve para describir ese grupo retrospectivamente, no para elegir jugadores de un backtest anterior. Los medios/desviaciones se recalculan en cada ventana con población común; las distancias resultantes no se comparan entre ventanas, solo los conjuntos de vecinos. Se verifica integridad de originales y se guarda hash del perfil base. Artefacto local: `similarity_stability.json`. Identidades siguen pendientes; estabilidad estadística no certifica identidad ni disponibilidad histórica.


Resultado ejecutado: comparables en las tres pruebas/retención ≥3 en todas: ATP 134/44, Challenger principal 254/30, clasificación 88/10, MCP 44/28. No sumar grupos: hay jugadores compartidos. La mediana MCP por prueba es 4, 3 y 3 vecinos; en Challenger principal 3, 3 y 2. El requisito de cumplir en las tres pruebas es más exigente que una mediana por prueba.

Se exporta también `profile_review_queue.json` con los 350 jugadores y un estado por grupo: criterio de retención cumplido, sensible o comparación insuficiente. Estos estados no son una calificación definitiva de calidad. Todas las identidades MCP siguen pendientes de comprobación independiente. En césped MCP ninguna de las tres pruebas alcanza seis participantes; no hay resultado de retención.


## Revisión acordada — perfil de golpes global

El perfil MCP reúne todas las superficies por jugador y período. Los constructores de perfil, similitudes y estabilidad generan solo la vista de golpes `All`; las vistas básicas ATP/Challenger continúan separadas por superficie. Se mantiene el campo `surface=All` para compatibilidad del esquema, sin perfiles de golpes separados Hard/Clay/Grass. La superficie del partido original se preserva y podrá actuar como contexto/interacción del modelo. Esta decisión reemplaza las vistas de golpes por superficie descritas en avances anteriores. No se infiere que el estilo sea invariable entre superficies; la mezcla observada puede sesgar el perfil agregado.


## Afinidad descriptiva en la interfaz

La web transforma la distancia d en índice `100/(1+d)`, mostrado con signo % para facilitar lectura en una escala 0–100. No es proporción medida de golpes coincidentes ni probabilidad ni confianza. El orden de vecinos permanece idéntico porque la transformación es monótona. Cada una de las tres áreas más cercanas usa `d=abs(tasaA-tasaB)/desviación` de su vista; debajo se muestran ambas tasas observadas y la diferencia en puntos porcentuales. Los métodos y contadores de base permanecen iguales. Las afinidades se interpretan dentro de cada vista, no entre circuitos ni familias de características. La fórmula y límites están en un desplegable accesible.
