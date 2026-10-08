# Tennis Intelligence Lab
## Plan maestro del proyecto

**Nombre provisional:** Tennis Intelligence Lab  
**Caso de uso principal:** Predecir partidos y torneos de tenis ATP utilizando únicamente la información que habría estado disponible antes de la fecha de predicción.  
**Fecha de corte histórica inicial:** **2024-12-31**  
**Período principal de evaluación retrospectiva (backtest):** **Temporada 2025**  
**Estado:** Planificación / Fase 0  
**Función del documento:** Fuente de referencia a largo plazo del proyecto. Codex y los colaboradores deben leer este archivo antes de realizar trabajo significativo.

> Nota de traducción: los nombres de archivos, campos, variables, bibliotecas e identificadores técnicos se conservan en inglés para mantener su correspondencia con el código. La copia original en inglés se encuentra en `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.en.md`.

## Actualización acordada: evaluación en dos etapas (2026-10-07)

Este plan utiliza como experimento principal la **etapa experimental 1**: entrenamiento y ajuste solo con datos hasta el **2024-12-31**, y evaluación inicial sobre **2025**. La **etapa experimental 2** repetirá el procedimiento con entrenamiento hasta el **2025-12-31** y evaluación sobre **2026**. Estas etapas experimentales no reemplazan las fases de ingeniería 0–10 descritas más abajo.

Antes de examinar los errores de 2025 se guardarán la configuración y el resultado inicial. Las mejoras posteriores inspiradas por 2025 deberán registrarse como desarrollo, sin presentar una nueva evaluación sobre ese mismo año como una prueba independiente. Para la segunda etapa se fijarán las decisiones antes de evaluar 2026; sus resultados no se usarán para ajustar ese modelo.

Las dos etapas tendrán modos separados de información congelada y actualización histórica secuencial. La configuración ejecutable está en `configs/experiments.json` y el avance se registra en `docs/work_log.md`. El backup inglés permanece intacto y representa el plan original, anterior a esta actualización.

## Actualización acordada: validación de fuentes

Sackmann es una fuente candidata, no una garantía de corrección. Se contrastará con otras fuentes públicas: TennisMyLife para comparación de partidos y estadísticas, y ATP Tour para comprobaciones oficiales. Se documentarán cobertura, licencias, independencia de origen y discrepancias. Un espejo de Sackmann no cuenta como una segunda fuente independiente; tampoco se supondrá independencia total entre bases que podrían compartir datos ATP.

No hay todavía tres bases completas verificadas con la misma cobertura. Tennis-Data se descartó para la importación automatizada por sus restricciones publicadas. El acceso masivo a ATP está pendiente; sus comprobaciones iniciales son puntuales.

`tourney_date` no se utilizará como fecha exacta de partido, ni `match_num` como orden cronológico garantizado. Hasta resolver fechas y disponibilidad de resultados, las tablas serán de exploración y **no habilitarán un backtest por partido**. Los archivos históricos descargados hoy también pueden contener correcciones posteriores: reconstruir el pasado con ellos no equivale a disponer de la versión publicada en aquel momento.

---

# 1. Visión

Tennis Intelligence Lab es una plataforma integral de datos, análisis, aprendizaje automático y simulación para el tenis profesional.

El proyecto debe responder preguntas como:

- ¿Quién tiene más probabilidades de ganar un partido específico?
- ¿Cómo afecta la superficie de juego a esa probabilidad?
- ¿Cuánto influye el rendimiento reciente?
- ¿Hay estilos de juego sistemáticamente favorables o desfavorables frente a otros?
- ¿Qué tan difícil es el camino de cada jugador en el cuadro de un torneo?
- ¿Qué probabilidad tiene cada jugador de llegar a cada ronda?
- ¿Cuánto aumentó o redujo el cuadro real la probabilidad de ganar el título de un jugador?
- ¿Qué jugadores están sistemáticamente sobrevalorados o infravalorados por el ranking?
- ¿Qué estadísticas mejoran realmente la precisión predictiva?
- ¿Se pueden descubrir estilos de juego o arquetipos de enfrentamiento a partir de los datos?
- ¿Puede el sistema explicar *por qué* prefiere a un jugador frente a otro?

El objetivo a largo plazo es combinar:

1. Ingeniería de datos
2. Análisis de tenis
3. Modelado estadístico
4. Aprendizaje automático
5. Simulación Monte Carlo
6. Evaluación retrospectiva y evaluación de modelos
7. Visualización interactiva
8. Predicciones explicables
9. Más adelante, una capa de análisis con inteligencia artificial

El proyecto debe servir como trabajo de portafolio, espacio de investigación y plataforma reutilizable de análisis de tenis.

---

# 2. Objetivo rector

La experiencia final del producto debe permitir que un usuario seleccione un torneo, por ejemplo:

> Australian Open 2025

Y vea:

- el cuadro completo,
- las valoraciones de los jugadores,
- las probabilidades de ganar cada partido,
- la probabilidad de llegar a cada ronda,
- la probabilidad de ganar el título,
- la dificultad del cuadro,
- los candidatos a dar una sorpresa,
- los jugadores peligrosos que no son cabezas de serie,
- los caminos probables,
- y explicaciones de las dinámicas importantes de los enfrentamientos.

Ejemplo de resultado:

| Jugador | Octavos | Cuartos | Semifinal | Final | Campeón |
|---|---:|---:|---:|---:|---:|
| Jugador A | 95.1% | 83.2% | 66.5% | 48.8% | 29.4% |
| Jugador B | 96.8% | 88.7% | 71.9% | 51.3% | 31.2% |
| Jugador C | 84.3% | 63.9% | 38.4% | 19.7% | 8.4% |

El usuario también debe poder consultar:

> ¿Por qué el modelo le da al Jugador A un 61% frente al Jugador B?

La explicación debe basarse en variables reales del modelo, por ejemplo:

- un Elo ajustado por superficie más alto,
- un mejor rendimiento reciente al resto,
- más descanso,
- un enfrentamiento favorable entre estilos,
- una ventaja en partidos al mejor de cinco sets,
- u otros factores medidos.

El sistema nunca debe inventar explicaciones que no estén relacionadas con el modelo real.

---

# 3. Principio central de investigación: simular el pasado con honestidad

El proyecto se basa en la **corrección temporal**.

El primer gran experimento utilizará:

> **Toda la información disponible hasta el 2024-12-31 inclusive**

Para predecir:

> **La temporada de tenis 2025**

Esto significa que el sistema debe comportarse como si el futuro fuera desconocido.

## Filtración de información prohibida

Al predecir un partido en la fecha `D`, el proceso de generación de variables nunca debe utilizar:

- partidos ocurridos después de `D`,
- rankings publicados después de `D`,
- actualizaciones de Elo resultantes del partido que se está prediciendo,
- rondas posteriores del mismo torneo,
- estadísticas agregadas futuras de la temporada 2025,
- lesiones o retiros futuros,
- cambios futuros en el cuadro,
- rankings futuros,
- resultados futuros por superficie,
- conocimiento ingresado manualmente sobre lo que ocurrió después.

Este principio tiene prioridad sobre el rendimiento del modelo.

Es preferible un modelo menos potente con una evaluación histórica honesta a uno más potente con filtración de información.

---

# 4. Estrategia de evaluación retrospectiva

Cronología histórica inicial:

```text
Datos históricos:
1968 ─────────────────────────────── 2024-12-31
                                      │
                                      │ corte estricto de entrenamiento del modelo
                                      ▼
Período de predicción:
2025-01-01 ────────────────────────── 2025-12-31
```

Objetivos prioritarios de evaluación:

1. Australian Open 2025
2. Roland Garros 2025
3. Wimbledon 2025
4. US Open 2025
5. Masters 1000
6. ATP 500
7. ATP 250
8. Temporada ATP completa
9. Challenger Tour, más adelante

No seleccionar únicamente los torneos en los que el modelo tuvo éxito.

---

# 5. Distinción crucial: modelo congelado frente a información congelada

Deben separarse claramente dos experimentos.

## Modelo congelado

Los parámetros del modelo se entrenan únicamente con información hasta el **2024-12-31**.

## Variables históricas actualizadas secuencialmente

Al predecir un partido de julio de 2025, es legítimo utilizar partidos de enero a junio de 2025 porque esos resultados ya se conocían en el momento de la predicción.

Por lo tanto, la evaluación retrospectiva realista preferida es:

```text
parámetros del modelo congelados al 2024-12-31
+
variables actualizadas cronológicamente durante 2025
```

Esto permite que el Elo y el rendimiento reciente evolucionen naturalmente sin volver a entrenar el modelo de aprendizaje automático.

Un experimento secundario más estricto también puede utilizar:

```text
toda la información congelada al 2024-12-31
```

Ambos modos deben etiquetarse claramente y nunca mezclarse.

---

# 6. Alcance de V1

V1 debe admitir:

- individuales masculinos ATP,
- datos históricos de partidos,
- rankings,
- metadatos de jugadores,
- superficie de la cancha,
- categoría del torneo,
- ronda del torneo,
- valoraciones Elo,
- Elo por superficie,
- rendimiento reciente,
- estadísticas básicas de saque,
- estadísticas básicas de resto,
- variables de enfrentamientos directos,
- variables de fatiga y carga de juego,
- predicción probabilística de partidos,
- importación de cuadros de torneos,
- simulación Monte Carlo de torneos,
- probabilidades de avanzar ronda por ronda,
- probabilidades de ganar el título,
- evaluación retrospectiva histórica,
- evaluación de la calibración del modelo,
- una interfaz web básica.

## Fuera del alcance de V1

No retrasar V1 por:

- WTA,
- dobles,
- productos de apuestas,
- apuestas en vivo,
- predicción en vivo punto por punto,
- análisis de video,
- visión por computadora,
- análisis biomecánico,
- fuentes comerciales propietarias,
- arquitecturas complejas de aprendizaje profundo,
- aplicaciones móviles,
- funciones sociales,
- cuentas de usuario,
- monetización.

---

# 7. Fuentes de datos

La arquitectura debe tratar las fuentes de datos como adaptadores intercambiables.

Ningún modelo central debe depender directamente de un esquema externo específico.

## 7.1 Conjuntos de datos de tenis de Jeff Sackmann

Principal candidato para la base histórica.

Se espera que los datos incluyan:

- partidos ATP,
- torneos,
- jugadores,
- rankings,
- ganador y perdedor,
- superficie,
- ronda,
- ranking en el momento del partido,
- marcadores,
- estadísticas de saque para muchos partidos,
- datos de Challenger.

Probablemente sea la fuente histórica canónica inicial.

Los datos originales de la fuente no deben incorporarse automáticamente a Git.

## 7.2 Match Charting Project

Fuente avanzada opcional.

Usos potenciales:

- secuencias de puntos,
- información a nivel de golpe,
- direcciones de saque,
- estructura de los intercambios,
- golpes ganadores y errores,
- tendencias tácticas,
- modelado del estilo de los jugadores.

La cobertura es incompleta.

Por lo tanto, el modelo de predicción base **no** debe requerir esta fuente.

## 7.3 Rankings

Los rankings históricos siempre deben incorporarse tal como existían en el momento de la predicción.

Nunca utilizar el ranking actual para reproducir un partido histórico.

## 7.4 Cuadros de torneos

El simulador necesitará los cuadros históricos reales.

Más adelante deberá admitir:

- cabezas de serie,
- jugadores provenientes de la clasificación,
- perdedores afortunados (*lucky losers*),
- bajas,
- pases libres (*byes*),
- cuadros actualizados,
- el estado del cuadro conocido en una fecha y hora determinadas.

La reproducibilidad histórica es importante.

---

# 8. Licencias de los datos

Las licencias son una restricción de ingeniería fundamental.

Mantener:

```text
docs/data_sources.md
```

Para cada fuente:

```yaml
source_name:
source_url:
license:
commercial_use_allowed:
redistribution_allowed:
attribution_required:
raw_data_committed_to_repo:
notes:
```

No redistribuir datos públicamente sin verificar la licencia.

Si la fuente permite únicamente usos no comerciales, mantener la arquitectura intercambiable para un futuro uso comercial.

---

# 9. Filosofía del repositorio

Esto no debe convertirse en un cementerio de notebooks.

Los notebooks están permitidos para:

- exploración,
- gráficos,
- pruebas de hipótesis,
- diagnóstico de modelos.

La lógica de producción debe estar en módulos Python normales.

Principio rector:

```text
proceso reproducible > notebook impresionante
```

---

# 10. Estructura propuesta del repositorio

```text
tennis-intelligence-lab/
│
├── README.md
├── PROJECT_PLAN.md
├── AGENTS.md
├── CHANGELOG.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── configs/
│   ├── base.yaml
│   ├── features.yaml
│   ├── models.yaml
│   └── tournaments.yaml
│
├── data/
│   ├── raw/
│   ├── staging/
│   ├── processed/
│   └── external/
│
├── src/
│   └── tennis_lab/
│       ├── ingestion/
│       │   ├── sackmann.py
│       │   ├── rankings.py
│       │   ├── draws.py
│       │   └── match_charting.py
│       ├── cleaning/
│       │   ├── matches.py
│       │   ├── players.py
│       │   └── tournaments.py
│       ├── features/
│       │   ├── elo.py
│       │   ├── surface.py
│       │   ├── form.py
│       │   ├── serve.py
│       │   ├── return_stats.py
│       │   ├── head_to_head.py
│       │   ├── fatigue.py
│       │   ├── opponent_adjustment.py
│       │   └── matchup.py
│       ├── models/
│       │   ├── baseline.py
│       │   ├── logistic.py
│       │   ├── gradient_boosting.py
│       │   ├── calibration.py
│       │   └── registry.py
│       ├── simulation/
│       │   ├── match.py
│       │   ├── bracket.py
│       │   └── monte_carlo.py
│       ├── evaluation/
│       │   ├── metrics.py
│       │   ├── backtest.py
│       │   ├── calibration.py
│       │   └── reports.py
│       ├── api/
│       └── utils/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_elo_experiments.ipynb
│   ├── 03_feature_research.ipynb
│   └── 04_model_diagnostics.ipynb
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── regression/
│
├── scripts/
│   ├── download_data.py
│   ├── build_dataset.py
│   ├── train_model.py
│   ├── backtest.py
│   └── simulate_tournament.py
│
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   ├── data_dictionary.md
│   ├── modeling.md
│   ├── evaluation.md
│   └── decisions/
│
└── frontend/
```

Esta es la estructura objetivo; no hay que crearla vacía el primer día.

En este repositorio, `PROJECT_PLAN.md` corresponde al archivo `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md`.

Evitar abstracciones que todavía no sean necesarias.

---

# 11. Modelo de datos canónico

El proyecto debe tener su propio esquema canónico de tenis.

Los nombres de columnas de las fuentes externas no deben propagarse por todo el código.

## Jugador

```text
player_id
source_player_id
first_name
last_name
full_name
hand
birth_date
country_code
height_cm
```

## Torneo

```text
tournament_id
name
season
start_date
surface
level
location
country
draw_size
best_of
```

Categorías posibles:

```text
GS
M1000
ATP500
ATP250
CH
ITF
```

## Partido

Representar a los participantes de manera neutral, incluso si la fuente original almacena ganador y perdedor.

```text
match_id
tournament_id
match_date
round
surface
best_of
player_1_id
player_2_id
winner_id
score
minutes
```

Las tablas de variables para el modelado nunca deben exponer `winner_id` como variable predictiva.

## Estadísticas por jugador y partido

Preferir el formato largo:

```text
match_id
player_id
aces
double_faults
serve_points
first_serves_in
first_serve_points_won
second_serve_points_won
service_games
break_points_saved
break_points_faced
```

Estadísticas derivadas:

```text
ace_rate
double_fault_rate
first_serve_in_pct
first_serve_win_pct
second_serve_win_pct
service_points_won_pct
break_points_saved_pct
```

## Rankings

```text
ranking_date
player_id
rank
ranking_points
```

Las uniones históricas deben utilizar el último ranking disponible en el momento de la predicción o antes.

---

# 12. Filosofía del almacén de variables

Cada variable debe responder:

> ¿Se podría haber conocido este valor en el momento en que se habría realizado la predicción?

Las variables deben incluir una fecha `as_of_date` explícita o generarse cronológicamente.

Evitar agregaciones sin restricciones sobre el conjunto de datos completo.

---

# 13. Modelos de referencia

Antes del aprendizaje automático, establecer modelos de referencia sólidos y transparentes.

## Referencia 0 — Ranking ATP

Propósito:

- comprobación de coherencia,
- punto de comparación mínimo.

## Referencia 1 — Elo general

Implementar Elo internamente.

Fórmula general de probabilidad esperada:

```text
expected_A = 1 / (1 + 10 ^ ((elo_B - elo_A) / scale))
```

Parámetros a investigar:

- Elo inicial,
- factor K,
- ponderación por torneo,
- tratamiento de la inactividad,
- abandonos durante el partido,
- efectos del formato al mejor de cinco sets.

## Referencia 2 — Elo por superficie

Mantener valoraciones para:

- cancha dura,
- arcilla,
- césped.

Combinación posible:

```text
effective_rating = alpha * surface_elo + (1 - alpha) * overall_elo
```

Ajustar `alpha` únicamente con datos de validación anteriores a 2025.

---

# 14. Hoja de ruta de investigación de Elo

Variantes posibles:

- Elo clásico,
- Elo con K dinámico,
- Elo por superficie,
- Elo con reducción del peso de resultados antiguos,
- Elo ponderado por torneo,
- Elo sensible al margen del resultado,
- Elo basado en sets,
- Elo basado en juegos,
- regresión por inactividad,
- Glicko,
- sistemas bayesianos de valoración.

No implementarlas todas al mismo tiempo.

Cada nueva versión debe justificar su utilidad frente al modelo de referencia existente.

---

# 15. Variables de rendimiento reciente

Ventanas candidatas:

```text
last_5_matches
last_10_matches
last_20_matches
last_52_weeks
last_90_days
last_180_days
```

Variables posibles:

```text
win_rate
opponent_adjusted_win_rate
average_opponent_elo
elo_change
sets_won_pct
games_won_pct
tiebreak_win_pct
```

Equivalentes por superficie:

```text
hard_recent_form
clay_recent_form
grass_recent_form
```

Controlar el efecto de las muestras pequeñas.

---

# 16. Variables de saque

Candidatas calculadas sobre ventanas móviles:

```text
ace_rate
double_fault_rate
first_serve_in_pct
first_serve_win_pct
second_serve_win_pct
service_points_won_pct
hold_rate
break_points_saved_pct
```

Posibles normalizaciones posteriores:

- ajustadas por rival,
- ajustadas por superficie,
- ponderadas por antigüedad de los resultados.

---

# 17. Variables de resto

Variables posibles:

```text
return_points_won_pct
first_serve_return_points_won_pct
second_serve_return_points_won_pct
break_rate
break_points_converted_pct
```

La calidad del resto debe recibir la misma atención analítica que el saque.

---

# 18. Ajuste por rival

Las estadísticas sin ajustar dependen del contexto.

Métodos posibles:

- cálculo de residuos respecto de la calidad del rival,
- ajuste basado en Elo,
- valoraciones iterativas de ataque y defensa,
- rendimiento esperado frente a rendimiento real,
- modelos jerárquicos, más adelante.

Esta es un área de investigación, no un requisito de la fase 0.

---

# 19. Enfrentamientos directos

Variables candidatas:

```text
h2h_matches
h2h_wins
h2h_win_pct
h2h_surface_matches
h2h_surface_win_pct
h2h_last_24_months
```

Los enfrentamientos directos (H2H) tienen muestras pequeñas.

El modelo debe poder concluir que el H2H aporta poco valor predictivo.

---

# 20. Fatiga y carga de juego

Variables posibles:

```text
days_since_last_match
matches_last_7_days
matches_last_14_days
matches_last_30_days
sets_last_7_days
sets_last_14_days
games_last_7_days
games_last_14_days
minutes_last_7_days
minutes_last_14_days
previous_match_duration
previous_match_sets
```

Las variables de viajes y husos horarios son ideas para etapas posteriores.

---

# 21. Edad y etapa de la carrera

Variables posibles:

```text
age
age_squared
career_matches
career_surface_matches
```

Evitar supuestos fijos sobre la edad de máximo rendimiento.

Dejar que los datos de evaluación de períodos posteriores determinen si el efecto es útil.

---

# 22. Partidos al mejor de cinco sets

Los partidos masculinos de Grand Slam tienen una estructura diferente.

Variables posibles:

```text
best_of_5
career_bo5_record
bo5_elo
fifth_set_record
```

Un indicador básico `best_of_5` debe preceder a las métricas especializadas.

---

# 23. Contexto del torneo

Variables posibles:

```text
tournament_level
round
surface
best_of
seeded_status
home_country
```

Posibles variables posteriores:

- altitud,
- interior o exterior,
- velocidad de la cancha,
- clima,
- tipo de pelota.

No son requisitos de V1.

---

# 24. Modelado de enfrentamientos

## Actualización acordada: perfiles y compatibilidad de estilos

El universo exploratorio acordado es el top 500 del ranking disponible al cierre de 2024, con un piloto inicial de perfiles para el top 350. Se conserva un perfil vacío cuando faltan datos; no se garantiza cobertura uniforme ni se selecciona por ranking actual. La selección fija de este piloto no debe reutilizarse para escoger jugadores de validaciones históricas anteriores: cada una requiere su ranking contemporáneo.

Cada jugador tendrá un perfil histórico de golpes por fecha/período, unificado entre superficies. La superficie será contexto del encuentro, con posibles interacciones aprendidas con el perfil. Las estadísticas básicas de saque y devolución conservan su separación por superficie y circuito. La probabilidad base representará nivel y forma; un componente adicional aprenderá si la combinación de perfiles produce un rendimiento diferente del esperado. No se presupone ningún problema táctico de Alcaraz, Fognini u otro jugador.

El primer catálogo medible incluye tasa de aces, dobles faltas por punto de saque, primeros saques dentro, puntos ganados con primero y segundo, puntos totales ganados al saque y puntos de devolución ganados contra primero, segundo y en total. Estas son medidas de rendimiento observables; no prueban agresividad, calidad del revés o duración de intercambios. Para esas características se requiere evidencia adicional con cobertura y fechas comprobadas.

Las proporciones se calcularán sumando numeradores y denominadores, con tamaño de muestra y faltantes explícitos. No se promedian porcentajes por partido ni se combinan proveedores como observaciones distintas del mismo encuentro. Identidades, resultados, calidad y disponibilidad temporal deben estar resueltos antes de generar perfiles utilizables.

La similitud entre jugadores se construirá con perfiles anteriores al encuentro, estandarizados únicamente con datos de entrenamiento. Se buscará el rendimiento respecto de la probabilidad base, controlando superficie, nivel del rival y forma; no bastará una tasa bruta de victorias. Se combinará evidencia individual con la de perfiles similares y se reducirá el efecto hacia cero cuando haya pocos datos. La incertidumbre y el número de encuentros acompañarán el ajuste.

El ajuste se aprenderá conjuntamente con la referencia, por ejemplo como interacción regularizada sobre sus log-odds, manteniendo probabilidades válidas y coherentes al intercambiar jugadores. Su peso no será un porcentaje fijo. La comparación con/sin perfiles utilizará validación cronológica hasta 2024 y medirá log-loss, Brier y calibración. Similitudes, ventanas, regularización e hiperparámetros se fijarán antes de evaluar 2025; el ajuste solo se incorporará si mejora de forma consistente. Estadísticas del propio partido objetivo nunca forman parte de su perfil previo.


Un diferenciador a largo plazo.

Con el tiempo, el proyecto debe ir más allá de:

> El Jugador A es más fuerte que el Jugador B.

Y avanzar hacia:

> El estilo del Jugador A es especialmente favorable frente al estilo del Jugador B.

## Perfiles estadísticos de jugadores

Vector posible de un jugador:

```text
serve_strength
return_strength
ace_dependency
first_serve_dependency
second_serve_strength
aggression
break_rate
hold_rate
tiebreak_frequency
surface_bias
rally_profile
```

## Arquetipos de jugadores

Métodos posibles:

- K-Means,
- modelos de mezclas gaussianas,
- agrupamiento jerárquico,
- PCA + agrupamiento,
- UMAP para visualización.

Posibles arquetipos emergentes:

- gran sacador,
- atacante de saque y derecha,
- jugador agresivo de fondo,
- jugador equilibrado de toda la cancha,
- jugador de fondo orientado al resto,
- contraatacante defensivo.

Las etiquetas deben asignarse después de inspeccionar los grupos, en lugar de imponerse de antemano.

## Motor de similitud

Métodos posibles:

- distancia euclídea estandarizada,
- similitud del coseno,
- distancia de Mahalanobis,
- distancia en el espacio de PCA,
- representaciones aprendidas (*embeddings*), más adelante.

## Efectos de los enfrentamientos

Experimento posible:

```text
Tasa de victoria esperada del Jugador A según el modelo de referencia: 68%

contra grandes sacadores:      -4.1 puntos porcentuales
contra contraatacantes:        +3.7 puntos porcentuales
contra jugadores agresivos de fondo: +0.9 puntos porcentuales
```

Utilizar regularización hacia valores generales (*shrinkage*) y comprobaciones de significancia.

No presentar ruido estadístico como una verdad táctica.

---

# 25. Progresión de modelos

## Modelo A — Referencia basada en ranking

Sin aprendizaje automático.

## Modelo B — Elo

Sin aprendizaje automático.

## Modelo C — Regresión logística

Diferencias entre variables candidatas:

```text
elo_diff
surface_elo_diff
ranking_diff
age_diff
recent_form_diff
serve_strength_diff
return_strength_diff
fatigue_diff
```

Este debe ser el primer modelo de aprendizaje automático serio porque es interpretable.

## Modelo D — Árboles con potenciación por gradiente

Candidatos:

- XGBoost,
- LightGBM,
- CatBoost.

Solo cuando el proceso de regresión logística sea confiable.

## Modelo E — Modelos avanzados

Investigación posterior opcional:

- modelos bayesianos,
- redes neuronales,
- representaciones vectoriales (*embeddings*),
- modelos de secuencias.

---

# 26. Salida de las predicciones

Los modelos deben producir probabilidades.

No solo:

```text
El Jugador A gana
```

Sino:

```text
P(El Jugador A gana) = 0.643
P(El Jugador B gana) = 0.357
```

La calibración es importante.

Un modelo que predice un 70% debería acertar aproximadamente el 70% de las veces dentro de ese intervalo de probabilidad.

---

# 27. Métricas de evaluación

La tasa de aciertos por sí sola no alcanza.

Métricas principales:

- pérdida logarítmica (*Log Loss*),
- puntuación de Brier (*Brier Score*),
- tasa de aciertos (*Accuracy*),
- error de calibración,
- ROC-AUC, como métrica secundaria.

Intervalos de calibración:

```text
Predicción 50-55% → ¿tasa real de victorias?
Predicción 55-60% → ¿tasa real de victorias?
Predicción 60-65% → ¿tasa real de victorias?
...
```

Evaluación a nivel de torneo:

- calibración de probabilidades por ronda,
- calidad de la probabilidad asignada al campeón,
- identificación de sorpresas,
- verosimilitud de los resultados del cuadro.

---

# 28. Calibración

Métodos posibles:

- escalado de Platt,
- regresión isotónica,
- calibración beta.

La calibración también debe entrenarse únicamente con datos históricos anteriores al período de evaluación.

Nunca calibrar con el torneo que se está evaluando.

---

# 29. Validación cruzada temporal

La división aleatoria entre entrenamiento y prueba está prohibida para la evaluación de producción.

Ejemplo:

```text
Entrenamiento: <= 2022
Validación:    2023
Prueba:        2024

Entrenamiento: <= 2023
Validación:    2024
Prueba:        2024

Final:
Entrenamiento/ajuste: <= 2024-12-31
Evaluación retrospectiva: 2025
```

Las ventanas exactas pueden cambiar; la integridad cronológica, no.

---

# 30. Artefacto del modelo congelado de 2024

El primer modelo principal debe congelarse usando solo información anterior a 2025.

Una vez declarado congelado:

**No volver a ajustarlo con resultados de 2025.**

Estructura sugerida del artefacto:

```text
artifacts/
└── frozen_2024_model/
    ├── model.*
    ├── feature_config.yaml
    ├── training_manifest.json
    ├── metrics_pre_2025.json
    └── README.md
```

Etiqueta de Git sugerida:

```text
v0.1-frozen-2024
```

---

# 31. Simulación histórica de Grand Slams

Para cada Grand Slam de 2025:

1. reconstruir el cuadro tal como se conocía antes del inicio del torneo,
2. generar las variables de los jugadores a la fecha de inicio del torneo,
3. calcular las probabilidades necesarias para cada pareja de jugadores,
4. ejecutar simulaciones Monte Carlo,
5. guardar las tablas de probabilidades previas al torneo,
6. comparar con la realidad únicamente después.

Los artefactos de predicción deben ser inmutables.

Ejemplo:

```text
predictions/
└── 2025/
    ├── australian_open_pre_tournament.parquet
    ├── roland_garros_pre_tournament.parquet
    ├── wimbledon_pre_tournament.parquet
    └── us_open_pre_tournament.parquet
```

---

# 32. Motor de simulación de torneos

Entradas:

```text
draw
players
match_probability_function
number_of_simulations
```

Salidas por jugador:

```text
Probabilidad de segunda ronda
Probabilidad de tercera ronda
Probabilidad de cuarta ronda (octavos)
Probabilidad de cuartos de final
Probabilidad de semifinal
Probabilidad de final
Probabilidad de ser campeón
```

Requisitos:

- soporte de una semilla aleatoria para obtener resultados deterministas,
- resultados reproducibles,
- número de simulaciones configurable,
- propagación del cuadro verificada con pruebas unitarias,
- vectorización cuando sea útil.

Objetivo de V1:

```text
100.000 simulaciones de torneos
```

Optimizar solo si es necesario.

---

# 33. Dificultad del cuadro

Una de las principales métricas analíticas derivadas.

Pregunta:

> ¿Qué tan favorable o difícil fue el cuadro real para un jugador?

Metodología posible:

1. simular el cuadro real,
2. generar muchos cuadros hipotéticos válidos respetando las reglas de los cabezas de serie,
3. simular esos cuadros,
4. comparar la probabilidad real de título con la distribución neutral o aleatoria.

Métricas:

```text
actual_title_probability
median_random_draw_title_probability
draw_luck_delta
draw_difficulty_percentile
```

Ejemplo:

```text
Jugador A
Probabilidad de título con el cuadro real:     28.4%
Mediana de probabilidad con cuadros neutrales: 33.2%
Efecto del cuadro:                            -4.8 puntos porcentuales
Percentil de dificultad del cuadro:           89
```

---

# 34. Dificultad del camino

Estimar la dificultad por ronda para cada jugador.

Métricas posibles:

```text
Elo esperado del rival
Elo por superficie esperado del rival
Probabilidad esperada de ganar el partido
```

Los rivales futuros son inciertos, por lo que los valores esperados deben incorporar las probabilidades de las distintas ramas del cuadro.

---

# 35. Detección de sorpresas

Definiciones candidatas:

```text
probabilidad del modelo para el jugador peor ubicado en el ranking > 40%
```

O:

```text
probabilidad del modelo sustancialmente mayor que la probabilidad del modelo de referencia basado en ranking
```

Mantener la definición configurable y medible.

---

# 36. Páginas de jugadores

Secciones posibles:

```text
Nombre del jugador
País
Edad
Ranking
Elo general
Elo por superficie
Rendimiento reciente
Perfil de saque
Perfil de resto
Rendimiento por superficie
Jugadores similares
Probabilidades en torneos
Historial de partidos
```

Visualizaciones posibles:

- historial de Elo,
- historial de ranking,
- desglose por superficie,
- gráfico de percentiles de saque y resto,
- rendimiento en ventanas móviles,
- fortaleza estimada por el modelo a lo largo del tiempo.

---

# 37. Páginas de partidos

Ejemplo:

```text
Jugador A contra Jugador B
Roland Garros 2025
Cuartos de final
Arcilla
Al mejor de 5 sets
```

Mostrar:

```text
Probabilidad del modelo
Probabilidad según Elo
Probabilidad según Elo por superficie
Ranking ATP
Rendimiento reciente
Comparación de saque
Comparación de resto
Fatiga
Enfrentamientos directos
```

Explicar mediante factores reales del modelo.

---

# 38. Explicabilidad

Para modelos lineales:

- coeficientes,
- impactos estandarizados de las variables.

Para modelos de árboles potenciados:

- SHAP o equivalente.

Ejemplo de explicación estructurada:

```text
Jugador A: 64.2%

Factores positivos:
+ Ventaja de Elo por superficie
+ Mejor rendimiento reciente al resto
+ Más descanso

Factores negativos:
- Menor rendimiento reciente al saque
- Ligera desventaja en enfrentamientos directos
```

No introducir explicaciones generadas por modelos de lenguaje hasta que ya existan explicaciones estructuradas.

---

# 39. Analista de IA — Fase futura

Preguntas posibles:

> ¿Por qué el Jugador A es favorito frente al Jugador B?

> ¿Quién tiene el cuadro más difícil en Wimbledon?

> ¿Qué jugador que no es cabeza de serie tiene la mayor probabilidad de llegar a cuartos de final?

> Compará los perfiles de dos jugadores en cancha dura.

Arquitectura:

```text
Usuario
 ↓
Modelo de lenguaje / agente
 ↓
herramientas analíticas aprobadas
 ↓
resultados del modelo / capa semántica
 ↓
respuesta estructurada
```

El modelo de lenguaje nunca debe calcular probabilidades predictivas por su cuenta.

---

# 40. Proceso de datos

```text
Conjuntos de datos externos
       │
       ▼
Archivos originales inmutables
       │
       ▼
Validación
       │
       ▼
Tablas canónicas
       │
       ▼
Generación de variables
       │
       ▼
Conjunto de entrenamiento
       │
       ▼
Modelo
       │
       ▼
Predicciones
       │
       ▼
Simulador de torneos
       │
       ▼
API / interfaz de usuario
```

Los datos originales permanecen inmutables.

Las transformaciones deben ser reproducibles.

---

# 41. Almacenamiento

Tecnologías recomendadas para V1:

- Parquet,
- DuckDB.

Motivos:

- consultas analíticas rápidas,
- soporte de SQL,
- infraestructura mínima,
- integración sencilla con Python,
- ideal para desarrollo local y trabajos de portafolio.

Migraciones posibles más adelante:

- PostgreSQL,
- BigQuery.

No comenzar con infraestructura en la nube sin una necesidad concreta.

---

# 42. Tecnologías Python

Conjunto inicial de tecnologías candidatas:

```text
Python
Polars or Pandas
DuckDB
PyArrow
scikit-learn
XGBoost / LightGBM más adelante
Pydantic
FastAPI más adelante
pytest
```

Evitar Spark salvo que la escala lo requiera realmente.

---

# 43. Registro de experimentos

Como mínimo, guardar:

```text
experiment_id
timestamp
git_commit
data_cutoff
feature_set
model_type
hyperparameters
train_period
validation_period
test_period
metrics
```

Al principio basta con JSON o YAML.

Herramientas posibles más adelante:

- MLflow,
- Weights & Biases.

Incorporarlas solo cuando resulten útiles.

---

# 44. Reproducibilidad

Cada resultado publicado debe poder responder:

```text
¿Qué versión de los datos?
¿Qué commit del código?
¿Qué fecha de corte?
¿Qué conjunto de variables?
¿Qué modelo?
¿Qué parámetros?
¿Qué semilla aleatoria?
```

Las predicciones deben ser reproducibles.

---

# 45. Estrategia de pruebas

## Pruebas unitarias

Casos críticos:

- cálculo de actualizaciones de Elo,
- lógica de la fecha de corte histórica,
- filtrado por superficie,
- variables calculadas en ventanas móviles,
- uniones de rankings disponibles a una fecha determinada,
- propagación del cuadro,
- simulación de partidos,
- totales de probabilidades.

## Pruebas de filtración de información

Obligatorias.

Para un partido objetivo:

```text
max(source_match_date_used_for_features) < target_match_date
```

Automatizar esta comprobación.

## Pruebas de integración

Ejemplo:

```text
partidos originales
→ datos limpios
→ variables
→ predicción
```

## Pruebas de regresión

Congelar resultados conocidos seleccionados para que las refactorizaciones no los cambien silenciosamente.

---

# 46. Controles de calidad de datos

Ejemplos:

```text
winner != loser
los identificadores de jugadores existen
surface pertenece al conjunto permitido
rank > 0 si está presente
0 <= percentage <= 1
serve_points >= first_serves_in
first_serve_points_won <= first_serves_in
```

Registrar los datos faltantes por:

- año,
- torneo,
- categoría,
- jugador.

Nunca convertir silenciosamente estadísticas faltantes en cero.

---

# 47. Estrategia para datos faltantes

Enfoques posibles:

- indicadores explícitos de valores faltantes,
- medianas por época y superficie,
- manejo de valores faltantes propio del modelo,
- exclusión de variables para períodos históricos tempranos.

Documentar cada decisión.

No inventar datos.

---

# 48. Abandonos y victorias sin jugar

Se necesita una clasificación explícita:

```text
completed
retirement
walkover
default
```

Política inicial posible:

- excluir las victorias sin jugar (*walkovers*) del entrenamiento de resultados de partidos,
- excluir los abandonos durante el partido del entrenamiento normal con partidos completos o analizarlos por separado,
- utilizar normalmente los partidos completados.

Más adelante, el riesgo de lesión o abandono puede convertirse en un problema de modelado independiente.

---

# 49. Identidad de los jugadores

Utilizar identificadores estables de la fuente siempre que sea posible.

Los nombres son atributos de presentación, no claves.

Problemas posibles:

- tildes y otros signos diacríticos,
- cambios en la escritura del nombre,
- nombres duplicados,
- cambios de nacionalidad.

Construir una capa de correspondencias canónicas.

---

# 50. Semántica temporal

Los datos analíticos deben distinguir claramente:

```text
event_date
available_at
as_of_date
```

Estos conceptos pueden diferir.

Un ranking del lunes no debe poder utilizarse para una predicción del domingo anterior.

---

# 51. Fase 0 — Exploración de la fuente de datos

## Objetivo

Demostrar que los datos históricos de la fuente son suficientes.

Tareas:

- obtener el conjunto de datos ATP,
- inspeccionar los archivos,
- inspeccionar las temporadas hasta 2024,
- identificar las tablas de jugadores,
- identificar los rankings,
- identificar las estadísticas de partidos,
- medir los datos faltantes,
- inspeccionar la cobertura por superficie,
- inspeccionar las categorías de torneos,
- inspeccionar los partidos de Grand Slam,
- documentar las licencias,
- crear un diccionario de datos inicial.

Entregable:

```text
docs/data_source_spike.md
```

Condición de éxito:

Podemos reconstruir una tabla limpia de partidos ATP hasta el **2024-12-31** y excluir claramente 2025.

---

# 52. Fase 1 — Conjunto histórico canónico

Construir:

```text
matches.parquet
players.parquet
rankings.parquet
```

Tareas:

- normalizar fechas,
- normalizar superficies,
- normalizar identificadores de jugadores,
- normalizar categorías de torneos,
- tratar valores faltantes,
- clasificar el estado de los partidos,
- validar la unicidad,
- agregar pruebas.

Entregable:

```text
scripts/build_dataset.py
```

---

# 53. Fase 2 — Motor Elo

Implementar:

- Elo general,
- Elo por superficie,
- valoraciones previas al partido,
- actualizaciones posteriores al partido,
- tabla histórica de Elo.

Las filas de variables deben utilizar el **Elo previo al partido**.

Entregables:

```text
src/tennis_lab/features/elo.py
tests/unit/test_elo.py
```

Comparar Elo con el ranking ATP.

---

# 54. Fase 3 — Proceso histórico de generación de variables

Conjunto inicial de variables:

```text
overall_elo_diff
surface_elo_diff
ranking_diff
age_diff
recent_win_rate_diff
recent_elo_change_diff
serve_strength_diff
return_strength_diff
rest_days_diff
```

Cada variable debe ser válida cronológicamente.

Entregable:

```text
training_matches.parquet
```

---

# 55. Fase 4 — Modelos de referencia

Entrenar y comparar:

1. modelo de referencia basado en ranking,
2. modelo de referencia Elo,
3. Elo por superficie,
4. regresión logística.

Evaluar con validación temporal.

Documentar en:

```text
docs/model_baselines.md
```

No avanzar a árboles potenciados antes de que esta fase sea confiable.

---

# 56. Fase 5 — Ingeniería avanzada de variables

Experimentar con:

- variables de saque,
- variables de resto,
- ajuste por rival,
- fatiga,
- categoría del torneo,
- ronda,
- formato al mejor de cinco sets,
- enfrentamientos directos,
- curvas de edad,
- rendimiento por superficie.

Cada nueva variable debe probarse mediante un análisis de ablación, comparando el modelo con y sin esa variable.

Pregunta central:

> ¿Esta variable mejora la pérdida logarítmica en datos de períodos posteriores al entrenamiento?

Si no, eliminarla o conservarla únicamente para análisis exploratorio.

---

# 57. Fase 6 — Congelar el modelo anterior a 2025

Requisitos:

- ajuste de hiperparámetros completado,
- definiciones de variables congeladas,
- artefacto del modelo guardado,
- métricas de validación documentadas,
- commit de Git etiquetado.

Ningún resultado de 2025 puede influir en este modelo congelado.

---

# 58. Fase 7 — Australian Open 2025

Primera gran demostración histórica del proyecto.

Pasos:

1. cargar el cuadro real previo al torneo,
2. reconstruir las variables de los jugadores al inicio del torneo,
3. generar probabilidades de partidos,
4. ejecutar una simulación Monte Carlo,
5. guardar las predicciones,
6. comparar después con el resultado real.

Resultados:

- probabilidades de título,
- probabilidades por ronda,
- dificultad del cuadro,
- candidatos a dar una sorpresa,
- explicación de los favoritos,
- evaluación posterior al evento.

---

# 59. Fase 8 — Todos los Grand Slams de 2025

Repetir la misma metodología para:

- Roland Garros,
- Wimbledon,
- US Open.

No volver a ajustar el modelo para un torneo específico usando los resultados de Grand Slams anteriores de 2025 si el experimento pretende representar el modelo congelado de 2024.

Al final, comparar el rendimiento por:

- superficies,
- rondas,
- franjas de ranking,
- favoritos frente a no favoritos.

---

# 60. Fase 9 — Evaluación retrospectiva de todo 2025

Predecir secuencialmente cada partido ATP que cumpla los criterios de inclusión.

Mantener modos de evaluación separados:

## Modo de información congelada

Todo queda fijado al 2024-12-31.

## Modo histórico con actualización secuencial

Los parámetros del modelo están congelados, pero el Elo, el rendimiento reciente y las estadísticas se actualizan con los partidos de 2025 que ya terminaron.

El modo histórico con actualización secuencial es la principal referencia realista.

---

# 61. Fase 10 — Interfaz del producto

Solo cuando el proceso del modelo sea estable.

Tecnologías candidatas:

```text
FastAPI
React / Next.js
```

Rutas posibles:

```text
/
/players
/players/{id}
/matches/{id}
/tournaments
/tournaments/{id}
/model
```

---

# 62. Preguntas de investigación pendientes

Son preguntas, no promesas.

- ¿Cuánto mejor es el Elo por superficie que el Elo general?
- ¿Cuál es la mejor combinación entre Elo por superficie y Elo general?
- ¿Con qué rapidez debe reducirse el peso de los resultados antiguos?
- ¿El H2H mejora las predicciones en períodos posteriores al entrenamiento?
- ¿El rendimiento reciente aporta valor más allá del Elo?
- ¿El ranking ATP sigue siendo útil una vez incluido el Elo?
- ¿Las métricas de saque y resto mejoran sustancialmente las predicciones?
- ¿Cómo deben ponderarse los resultados de Challenger?
- ¿Cuánto reduce el formato al mejor de cinco sets la probabilidad de sorpresa?
- ¿Los arquetipos de jugadores pueden mejorar las predicciones de enfrentamientos?
- ¿Podemos identificar ventajas de enfrentamiento específicas de cada estilo?
- ¿Se puede medir la fatiga únicamente con el historial de partidos?
- ¿Qué tan predictivos son los resultados de los tiebreaks?
- ¿Las métricas de puntos de quiebre son principalmente ruido una vez incluida la calidad del saque y el resto?
- ¿Se puede resumir la dificultad del cuadro con una métrica intuitiva?

---

# 63. Expansión a Challenger

Casos de uso posibles más adelante:

- jugadores emergentes,
- detección temprana,
- ineficiencias del ranking,
- transición de Challenger a ATP.

Posible función futura:

> Detector de jugadores en ascenso

Esto debe venir después de que funcione el proceso ATP central.

---

# 64. Expansión a WTA

La arquitectura debe evitar supuestos específicos de ATP cuando no sean necesarios.

WTA no forma parte de V1.

Cuando ATP sea estable:

- agregar la importación de datos WTA,
- entrenar de manera independiente,
- comparar el comportamiento de las variables.

No asumir que los coeficientes del modelo ATP se transfieren a WTA.

---

# 65. Comparación con el mercado de apuestas — Opcional

No es un objetivo central del producto.

Si se dispone legalmente de probabilidades históricas de casas de apuestas, pueden utilizarse como referencia:

```text
pérdida logarítmica de nuestro modelo
vs
pérdida logarítmica de la probabilidad implícita del mercado
```

El proyecto no está pensado como un sistema de apuestas.

---

# 66. Principio de diseño del producto

La interfaz debe responder:

> ¿Qué estima el modelo y por qué?

Preferir:

- probabilidades claras,
- percentiles,
- comparaciones,
- explicaciones concisas,
- detalle progresivo.

Evitar abrumar al usuario con tablas de datos sin procesar por defecto.

---

# 67. Definición de éxito

## Éxito técnico

- procesos reproducibles,
- corrección temporal,
- pruebas automatizadas,
- simulaciones deterministas,
- trazabilidad clara.

## Éxito de modelado

El modelo mejora sustancialmente sobre el ranking ATP e idealmente sobre el Elo estándar en métricas probabilísticas evaluadas en períodos posteriores al entrenamiento.

## Éxito del producto

Un usuario puede inspeccionar un torneo y comprender:

- favoritos,
- caminos,
- rivales peligrosos,
- probabilidades,
- motivos.

## Éxito como portafolio

Un evaluador técnico puede ver competencias en:

- ingeniería de datos,
- ingeniería analítica,
- estadística,
- aprendizaje automático,
- ingeniería de software,
- criterio de producto,
- comunicación.

---

# 68. Lo que no debemos hacer

Evitar:

- filtración de información,
- divisiones aleatorias de entrenamiento y prueba para la evaluación final,
- ajustes con datos de 2025,
- uso de rankings futuros,
- uso de resultados finales de torneos al construir variables previas al torneo,
- arquitectura en la nube excesivamente compleja al principio,
- aprendizaje profundo por prestigio,
- modelos de lenguaje antes de que funcione el sistema analítico,
- redistribución indebida de datos sujetos a licencia,
- afirmaciones de causalidad basadas en variables predictivas,
- ocultamiento de malas predicciones,
- selección exclusiva de torneos exitosos.

---

# 69. Principios de ingeniería

1. **Corrección antes que sofisticación**
2. **Reproducibilidad histórica antes que puntuación del modelo**
3. **Modelo de referencia simple antes que modelo complejo**
4. **Calibración antes que una tasa de aciertos llamativa**
5. **Fuentes de datos modulares**
6. **Pruebas automatizadas contra la filtración de información**
7. **Configuración en lugar de valores fijos en el código**
8. **Notebooks para investigar, módulos para reproducir**
9. **Toda mejora del modelo debe superar una referencia**
10. **Nunca ocultar fallos**

---

# 70. Trabajo con Codex

Codex debe tratar este documento como la fuente estratégica de referencia del proyecto.

Antes de realizar trabajo significativo:

1. Leer `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md` (el `PROJECT_PLAN.md` mencionado en la propuesta original).
2. Leer `AGENTS.md`.
3. Inspeccionar la arquitectura existente.
4. Identificar la fase actual.
5. Realizar la implementación coherente más pequeña que avance esa fase.

Codex no debe redefinir por su cuenta los objetivos del producto.

Si una implementación propuesta entra en conflicto con este documento, comunicar el conflicto antes de continuar.

---

# 71. Reglas de trabajo de Codex

## Hacer

- escribir pruebas,
- preferir código legible,
- documentar supuestos,
- preservar la corrección temporal,
- utilizar interfaces tipadas cuando sean útiles,
- aislar los adaptadores de fuentes,
- mantener determinista la generación de variables,
- registrar metadatos de experimentos,
- actualizar la documentación cuando cambie la arquitectura.

## No hacer

- cambiar esquemas silenciosamente,
- crear abstracciones innecesarias,
- introducir infraestructura sin una necesidad concreta,
- incorporar grandes conjuntos de datos originales a Git,
- utilizar resultados de 2025 para ajustar el modelo congelado anterior a 2025,
- reescribir grandes áreas que funcionan sin una razón.

---

# 72. Registros de decisiones de arquitectura

Las decisiones importantes se guardan en:

```text
docs/decisions/
```

Archivos de ejemplo:

```text
ADR-001-use-duckdb.md
ADR-002-canonical-player-schema.md
ADR-003-elo-update-method.md
```

Cada registro de decisión de arquitectura (ADR) contiene:

```text
Contexto
Decisión
Alternativas
Consecuencias
```

---

# 73. Registro de investigación

Mantener opcionalmente:

```text
docs/research_log.md
```

Cada entrada:

```text
date
question
experiment
result
interpretation
next_step
```

Los experimentos con resultados negativos son valiosos y deben registrarse.

---

# 74. Primer hito concreto

Objetivo inicial:

> Dado cualquier partido ATP completado antes de 2025, reconstruir lo que se podía conocer inmediatamente antes de su inicio y calcular una probabilidad válida de victoria basada en Elo.

Proceso:

```text
partidos históricos originales
       ↓
ordenamiento cronológico
       ↓
Elo de A previo al partido
Elo de B previo al partido
       ↓
probabilidad
       ↓
resultado real
       ↓
evaluación
```

Si esto no es correcto, no construir modelos más sofisticados.

---

# 75. Primera misión de Codex

Instrucción sugerida:

> Leé `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md` completo antes de cambiar código.
>
> Estamos comenzando la fase 0 de Tennis Intelligence Lab.
>
> La primera fecha de corte para el entrenamiento del modelo es 2024-12-31. La temporada 2025 debe tratarse como datos de evaluación no vistos.
>
> Creá la estructura mínima del proyecto necesaria para explorar los conjuntos de datos ATP de Jeff Sackmann.
>
> No construyas el frontend, modelos potenciados, agentes de IA ni infraestructura en la nube.
>
> Objetivos:
> 1. Crear un proceso reproducible de descarga e importación de datos.
> 2. Inspeccionar los conjuntos de datos disponibles de partidos ATP, jugadores y rankings hasta 2024.
> 3. Producir un informe con esquemas, cantidades de filas, cobertura por año, datos faltantes, cobertura de estadísticas de partidos, superficies y categorías de torneos.
> 4. Verificar que 2025 pueda excluirse claramente mediante una fecha de corte explícita.
> 5. Agregar pruebas automatizadas básicas.
> 6. Documentar las licencias de los datos y los requisitos de atribución.
>
> Preferí tecnologías locales sencillas con Python, Parquet y DuckDB, salvo que el repositorio existente ofrezca una razón sólida para elegir otra opción.
>
> Antes de implementar, resumí el enfoque y enumerá los archivos que pensás crear o modificar.

---

# 76. Criterios de finalización de la fase 0

La fase 0 está completa cuando:

- el proyecto se instala localmente,
- los datos originales se pueden obtener de manera reproducible,
- se pueden consultar los partidos hasta 2024,
- los jugadores son identificables,
- se pueden consultar los rankings,
- la cobertura de estadísticas de partidos está documentada,
- 2025 queda excluido mediante un corte automatizado,
- las licencias están documentadas,
- las pruebas básicas de importación de datos pasan.

---

# 77. Definición del MVP

El primer producto mínimo viable (MVP) utilizable es:

> Seleccionar dos jugadores ATP y una fecha histórica de partido, y obtener una probabilidad previa al partido que sea históricamente válida.

Debe incluir:

```text
Elo general
Elo por superficie
Ranking ATP
recent form
variables básicas de saque y resto
probabilidad
explicación del modelo
```

No se requiere una interfaz de torneos para este MVP.

---

# 78. Definición de la V1 principal

La V1 principal está completa cuando el sistema puede:

1. importar un cuadro de Grand Slam,
2. crear variables de jugadores históricamente válidas,
3. predecir todos los enfrentamientos necesarios,
4. simular el torneo,
5. calcular probabilidades por ronda y de título,
6. medir la dificultad del cuadro,
7. mostrar los resultados en una interfaz utilizable,
8. reproducir las predicciones a partir de una versión guardada del modelo y los datos.

Demostración principal:

> **Pronósticos de los Grand Slams de 2025 generados con un modelo entrenado únicamente con información hasta 2024.**

---

# 79. Diferenciadores a largo plazo

## Inteligencia sobre el cuadro

No solo la probabilidad de título, sino cómo la modifica el cuadro real.

## Inteligencia sobre los enfrentamientos

No solo quién es más fuerte, sino qué estilo de juego resulta favorable frente al rival.

## Explicabilidad

Razones claras detrás de las probabilidades del modelo.

## Reconstrucción histórica

Viajar a cualquier fecha histórica y reproducir lo que el modelo habría estimado en ese momento.

## Laboratorio de modelos

Comparar:

```text
Ranking ATP
Elo
Elo por superficie
modelo logístico
modelo de árboles potenciados
```

Bajo reglas idénticas de evaluación temporal.

## Arquetipos de jugadores

Descubrir estilos de juego a partir de los datos.

---

# 80. Preguntas abiertas

No retrasar la fase 0 por estas preguntas:

- ¿Cuál será el año inicial exacto para entrenar?
- ¿Se incluirán partidos Challenger en el Elo?
- ¿Cómo debe interactuar el Elo Challenger con el Elo ATP?
- ¿Cómo deben tratarse los abandonos durante los partidos?
- ¿Separar cancha dura bajo techo y al aire libre?
- ¿Cómo debe afectar la inactividad a las valoraciones?
- ¿Cuál es la mejor combinación de Elo por superficie y Elo general?
- ¿Qué ventanas móviles son estables para las métricas de saque y resto?
- ¿Qué tan completa es la cobertura histórica de estadísticas de partidos?
- ¿Qué fuente debe proporcionar los cuadros históricos?
- ¿El simulador debe modelar partidos directamente o simular sets?
- ¿Cómo deben tratarse los jugadores provenientes de la clasificación?
- ¿Cómo modelar a jugadores con poco historial ATP?
- ¿Cómo deben incorporarse las lesiones?
- ¿Puede Match Charting Project aportar información útil sobre estilos pese a su cobertura limitada?

Registrar las preguntas resueltas como ADR.

---

# 81. Resumen de la hoja de ruta

```text
FASE 0
Exploración de la fuente de datos
      ↓
FASE 1
Conjunto histórico canónico
      ↓
FASE 2
Motor Elo
      ↓
FASE 3
Proceso histórico de generación de variables
      ↓
FASE 4
Referencias de ranking / Elo / regresión logística
      ↓
FASE 5
Variables avanzadas
      ↓
FASE 6
Congelar el modelo con datos hasta el 2024-12-31
      ↓
FASE 7
Evaluación retrospectiva del Australian Open 2025
      ↓
FASE 8
Todos los Grand Slams de 2025
      ↓
FASE 9
Evaluación retrospectiva de toda la temporada 2025
      ↓
FASE 10
Interfaz del producto
      ↓
FASE 11+
Estilos / enfrentamientos / análisis con IA
```

---

# 82. La regla que hay que recordar

Cuando el proyecto se complique, volver a esta pregunta:

> **¿Podemos utilizar solo información disponible en ese momento para estimar quién ganará, explicar por qué y propagar esas probabilidades a través del cuadro de un torneo?**

Si una variable, decisión de arquitectura, visualización o componente de IA no ayuda a responder esa pregunta, probablemente no sea una prioridad.

---

# 83. Próximo paso inmediato

**No** comenzar con React.

**No** comenzar con XGBoost.

**No** comenzar con un agente de IA.

**No** comenzar prediciendo Roland Garros.

Comenzar por demostrar:

```text
¿Podemos construir un conjunto histórico confiable de tenis hasta 2024
y reproducir el estado previo a un partido sin ver el futuro?
```

Una vez que eso funcione, todo lo demás será posible.

---

# 84. Objetivo rector del proyecto

**Construir un motor honesto, reproducible y explicable de pronósticos de tenis, capaz de simular torneos y evaluarse contra la temporada 2025 no vista durante el entrenamiento.**
