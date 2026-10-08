# Estado del proyecto y checklist

**Este es el documento principal para seguir el avance.** Se actualizará con cada entrega. Última actualización: 07/10/2026.

## Dónde estamos hoy

**Estamos en la fase 0: comprobar si los datos sirven.**

Ya descargamos dos bases históricas y las comparamos. Encontramos diferencias y algunos errores concretos. Todavía no entrenamos un modelo ni calculamos predicciones.

El punto principal por resolver es la fecha de cada partido: las bases suelen indicar la semana del torneo. Necesitamos saber qué resultados ya se conocían antes de predecir el siguiente encuentro.

**Próximo paso concreto:** revisar correspondencias de jugadores y vincular sus encuentros con fechas comprobadas. Eso permitirá construir una referencia Elo y medir rendimiento frente a perfiles respecto del nivel esperado; las similitudes sensibles quedarán como exploración.

**Qué necesitamos de vos ahora:** ningún dato ni decisión técnica. Podemos avanzar con las fuentes públicas. Si aparece una decisión que cambie el alcance del proyecto, te la presentaré en lenguaje sencillo con una recomendación.

## Qué queremos conseguir

Elegir dos jugadores y una fecha, obtener una probabilidad de victoria y entender sus motivos. Queremos incorporar también si sus perfiles de juego hacen el enfrentamiento más favorable o difícil de lo que su nivel sugiere. Más adelante, simular un torneo completo.

Lo comprobaremos en dos etapas:

| Etapa | Datos para entrenar y ajustar | Año para comprobar el modelo | Estado |
|---|---|---|---|
| Primera | Hasta el 31/12/2024 | 2025 | Preparando los datos |
| Segunda | Hasta el 31/12/2025 | 2026 | Pendiente de la primera |

Primero guardaremos el resultado inicial sobre 2025. Luego podremos aprender de sus errores para preparar la segunda etapa. Los resultados de 2026 no se usarán para ajustar el modelo que evaluamos sobre 2026.

## Cómo leer el checklist

**[x] significa terminado y comprobado. [ ] significa pendiente.** Tener una fase pendiente no significa que esté bloqueada: simplemente todavía no llegamos a ella. Las fases 0–10 son pasos de construcción; las dos etapas de la tabla anterior son las pruebas del modelo.

### Fase 0 — Revisar las fuentes de datos · EN CURSO

**Objetivo:** comprobar qué información tenemos, qué tan confiable es y cuáles son sus límites.

- [x] Leer el plan y dejarlo en español, conservando el original inglés.
- [x] Preparar el entorno de trabajo y la descarga repetible de datos.
- [x] Descargar Sackmann y TennisMyLife para 1968–2025.
- [x] Comparar las bases y detectar datos faltantes e incoherencias.
- [x] Contrastar casos puntuales con publicaciones oficiales de ATP e ITF.
- [x] Comprobar que la selección provisional de entrenamiento excluye 2025.
- [x] Comprobar el método de fechas con 9 casos oficiales: lluvia, medianoche y cruce de año.
- [x] Automatizar el control que impide usar resultados antes de su disponibilidad.
- [ ] Extender las fechas verificadas al historial y medir la cobertura utilizable.
- [x] Descargar una versión fija del Match Charting Project y medir cobertura hasta 2024.
- [ ] Validar una muestra de sus golpes y resolver errores de metadatos.
- [ ] Cerrar la selección de fuentes y el alcance de la validación adicional.
- [x] Definir las reglas para tratar datos dudosos antes de limpiar la base.

**Qué significa lo que ya hicimos:** hay dos bases descargadas y comprobaciones oficiales puntuales. Todavía no tenemos tres bases completas e independientes, ni una base lista para entrenar. Las pruebas automáticas verifican controles concretos; no garantizan que todos los datos sean correctos.

**Último avance:** tenemos una página para ver y probar el proyecto: [abrir explorador](docs/index.html). Muestra los 350 jugadores, permite buscar, comparar perfiles y explorar vecinos con sus motivos y evidencia. Funciona como HTML local y está preparada para GitHub Pages. No está publicada aún: falta identificar el repositorio destino. Pasaron 39 pruebas Python y las comprobaciones de interacción en Chrome.


| Comparación, todas las superficies | Comparables en las tres pruebas | Conservan al menos 3 de 5 vecinos en cada prueba |
|---|---:|---:|
| Saque/devolución ATP | 134 | 44 |
| Saque/devolución Challenger principal | 254 | 30 |
| Saque/devolución Challenger clasificación | 88 | 10 |
| Golpes detallados MCP | 44 | 28 |

**Qué aprendimos:** tener estadísticas no garantiza una lista de similares estable. Las similitudes básicas, especialmente Challenger, cambian bastante según los años usados. Eso puede reflejar evolución real, rivales distintos o selección de partidos, además de ruido. No conviene darles todavía un peso fijo en la predicción.

**Decisión sobre los golpes:** usamos un único perfil de golpes por jugador y período, reuniendo todas las superficies. La superficie se conserva como contexto de cada encuentro y podrá interactuar con ese perfil en el modelo. Saque y devolución siguen separados por superficie y circuito. La distribución de superficies observadas puede influir en el perfil global; pooling no elimina ese sesgo.

**Revisión del conjunto:** los 350 tienen una ficha de diagnóstico por grupo, con casos sensibles y casos sin muestra comparable. Las 250 correspondencias MCP siguen siendo candidatas por nombre; las otras 100 no están vinculadas. El criterio de conservar tres vecinos es exploratorio, no un porcentaje de confianza ni validación de identidad.

**Todavía falta:** cotejar identidades y anotaciones, vincular fechas efectivas y ajustar por nivel del rival. No hay modelo entrenado ni efecto táctico demostrado.


### Fase 1 — Construir la base limpia · PENDIENTE

**Objetivo:** tener una versión consistente y confiable de partidos, jugadores y rankings.

- [ ] Identificar al mismo jugador y torneo aunque las fuentes usen nombres o códigos distintos.
- [ ] Aplicar correcciones con evidencia y separar registros que no podemos resolver.
- [ ] Distinguir partidos completados, abandonos y victorias sin jugar.
- [ ] Comprobar fechas, duplicados y rankings; guardar la base limpia.

### Fase 2 — Crear el primer modelo: Elo · PENDIENTE

**Objetivo:** estimar la fuerza de cada jugador a partir de sus resultados anteriores.

- [ ] Calcular Elo general y Elo por superficie.
- [ ] Obtener una probabilidad antes de cada partido y actualizar Elo después del resultado.
- [ ] Verificar que ningún cálculo utiliza resultados que todavía no se conocían.

### Fase 3 — Preparar la información previa a cada partido · PENDIENTE

**Objetivo:** reunir los datos que el modelo podrá usar para predecir.

- [x] Definir el catálogo inicial de nueve características medibles de saque y devolución.
- [x] Implementar sus cálculos por partido y comprobar cobertura exploratoria en 2024.
- [x] Calcular perfiles descriptivos piloto de Alcaraz y Fognini para 2022–2024 por superficie.
- [x] Medir cobertura del top 500 histórico al cierre de 2024.
- [x] Preparar perfiles exploratorios del top 350 con métricas, faltantes y muestras.
- [x] Ampliar estadísticas básicas con Challenger 2022–2024 y separar cuadros/clasificación.
- [ ] Revisar correspondencias de identidad y validar las similitudes entre jugadores.
- [ ] Construir perfiles históricos previos a cada partido, con tamaño de muestra y fechas verificadas.
- [ ] Investigar datos de golpes y estilo: derecha, revés, agresividad y juego de fondo.
- [ ] Incorporar ranking, edad, rendimiento reciente y descanso.
- [ ] Incorporar estadísticas históricas básicas de saque y resto.
- [ ] Comprobar que cada dato estaba disponible antes del partido objetivo.

### Fase 4 — Comparar modelos simples · PENDIENTE

**Objetivo:** saber si el modelo aporta valor frente a alternativas sencillas.

- [ ] Comparar ranking ATP, Elo general y Elo por superficie.
- [ ] Entrenar una regresión logística, que combina factores de forma interpretable.
- [ ] Evaluar y ajustar usando solamente períodos hasta 2024.

### Fase 5 — Probar mejoras · PENDIENTE

**Objetivo:** agregar información solo cuando mejora los resultados.

- [x] Definir cómo separar nivel del jugador y compatibilidad entre perfiles.
- [x] Construir similitudes exploratorias explicables, por superficie y nivel, con muestra mínima.
- [x] Ejecutar diagnóstico de estabilidad de vecinos por años y superficies para todo el piloto.
- [ ] Revisar similitudes sensibles y medir rendimiento contra perfiles respecto de lo esperado.
- [ ] Aprender el ajuste por estilos, reduciendo su peso cuando hay poca evidencia.
- [ ] Comparar predicciones con y sin ese ajuste usando solamente datos hasta 2024.
- [ ] Probar fatiga, enfrentamientos directos, superficie y formato del partido.
- [ ] Comparar cada mejora con el modelo anterior usando datos hasta 2024.
- [ ] Registrar qué sirve y qué se descarta.

### Fase 6 — Fijar el modelo antes de probar 2025 · PENDIENTE

**Objetivo:** dejar guardado exactamente qué modelo vamos a evaluar.

- [ ] Guardar el modelo entrenado hasta 2024 y su configuración.
- [ ] Guardar los datos utilizados y los resultados de validación.
- [ ] Comprobar que podemos reproducir las mismas predicciones.

### Fase 7 — Primera prueba: Australian Open 2025 · PENDIENTE

**Objetivo:** comprobar el sistema con un torneo completo.

- [ ] Reconstruir el cuadro y la información conocida antes del torneo.
- [ ] Simularlo y guardar probabilidades de avanzar y ganar el título.
- [ ] Comparar las predicciones guardadas con los resultados reales.

### Fase 8 — Repetir con los otros Grand Slams de 2025 · PENDIENTE

**Objetivo:** comprobar si el método funciona en diferentes superficies.

- [ ] Evaluar Roland Garros, Wimbledon y US Open con el mismo modelo fijado.
- [ ] Comparar resultados y explicar dónde funciona mejor o peor.

### Fase 9 — Evaluar toda la temporada 2025 · PENDIENTE

**Objetivo:** medir el rendimiento general, incluyendo las malas predicciones.

- [ ] Predecir los partidos elegibles en orden histórico.
- [ ] Medir aciertos y calidad de las probabilidades.
- [ ] Separar resultados con información congelada de los que incorporan resultados ya conocidos durante el año.
- [ ] Guardar la evaluación inicial y revisar qué aprendimos antes de preparar 2026.

### Segunda etapa experimental — Repetir la comprobación sobre 2026 · PENDIENTE

**Objetivo:** comprobar con otro año el modelo desarrollado en la primera etapa.

- [ ] Documentar las mejoras decididas después de revisar 2025.
- [ ] Entrenar hasta el 31/12/2025 y volver a fijar modelo y configuración.
- [ ] Evaluar sobre 2026 sin usar sus resultados para ajustar ese modelo.
- [ ] Comparar ambas etapas y documentar las limitaciones.

### Fase 10 — Crear la interfaz · PROTOTIPO EXPLORATORIO LISTO

**Objetivo:** poder consultar jugadores, partidos y torneos de manera sencilla.

- [x] Crear un explorador HTML del piloto con búsqueda, comparación y similitudes.
- [x] Preparar página estática y snapshot con atribución para GitHub Pages.
- [ ] Publicar en el repositorio GitHub destino.
- [ ] Mostrar probabilidades y sus motivos.
- [ ] Mostrar resultados de simulaciones de torneos.
- [ ] Permitir reproducir una predicción histórica.

## Qué documento leer

**Para seguir el proyecto, alcanza con este archivo.** Los demás quedan como apoyo:

| Documento | Para qué sirve |
|---|---|
| [Log de trabajo](docs/work_log.md) | Consultar la historia de lo que hicimos, paso a paso. |
| [Plan maestro](TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md) | Consultar los objetivos y el alcance detallado a largo plazo. |
| [Informe de auditoría](docs/data_source_spike.md) | Revisar los números y resultados técnicos de la comparación. |
| [Casos de errores](docs/data_issues.md) | Ver ejemplos concretos y la evidencia para tratarlos. |

## Cómo vamos a comunicar los avances

Cada entrega actualizará este checklist y resumirá: **fase actual, qué quedó listo, qué falta y próximo paso**. Los detalles técnicos y nombres de archivos irán en la documentación de apoyo. Un archivo nuevo no significa que hayamos completado una nueva fase.
