# Registro de trabajo

Este archivo registra el avance del proyecto. Cada entrada debe indicar la fecha, el trabajo realizado, las decisiones o hallazgos, su verificación y lo que sigue. Una tarea solo se marca como completada cuando existe evidencia; preparar código no equivale a ejecutarlo con éxito.

## 2026-10-07 — 01. Lectura y traducción del plan

- **Realizado:** lectura completa del plan, traducción al español y creación del README con los objetivos y el primer hito.
- **Archivos:** `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md`, `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.en.md`, `README.md`.
- **Verificación:** la traducción conserva 84 secciones, 78 bloques de código y los esquemas técnicos. El backup conserva el original en inglés.
- **Estado:** completado.

## 2026-10-07 — 02. Acuerdo de evaluación en dos etapas

- **Decisión del usuario:** comenzar con información hasta el 31/12/2024 y probar sobre 2025. Después repetir con entrenamiento hasta el 31/12/2025 y evaluación sobre 2026.
- **Interpretación:** el primer resultado sobre 2025 se registra antes de ajustar el modelo a partir de sus errores. Si 2025 se usa después para mejorar el modelo, pasa a ser parte del desarrollo; 2026 será la comprobación independiente.
- **Realizado:** configuración explícita en `configs/experiments.json` y separación temporal en `src/tennis_lab/experiments.py`.
- **Pendiente:** ejecutar las pruebas, actualizar todas las referencias del plan y completar la revisión de la primera etapa antes de activar la segunda.

## 2026-10-07 — 03. Búsqueda y revisión de fuentes públicas

- **Decisión del usuario:** contrastar Sackmann con dos o tres fuentes públicas, sin asumir que sus datos son correctos.
- **Hallazgo:** el repositorio original `JeffSackmann/tennis_atp` devuelve HTTP 404. Se verificó el espejo `Aneeshers/tennis-sackmann-archive`, fijando la revisión `83733587353df8a41f2fd4f516147d5aa83f5a8d`.
- **Hallazgo temporal:** en Sackmann, `tourney_date` corresponde normalmente a la semana del torneo. `match_num` no garantiza orden cronológico. No se tratarán como fecha u orden real de cada partido.
- **Fuentes:** Sackmann archivado y TennisMyLife para comparación masiva; ATP Tour para comprobaciones oficiales puntuales. El espejo de Sackmann no cuenta como fuente independiente.
- **Descartado para ingesta automatizada:** Tennis-Data publica una restricción contra productos de entrenamiento con bots/scrapers/IA. Solo se consultó su documentación; no se descargaron sus conjuntos de partidos.
- **Limitación:** parte del archivo oficial de ATP devuelve HTTP 403. Las crónicas públicas indexadas permiten verificar casos puntuales, pero todavía no hay una tercera base completa descargada. La independencia de origen entre las dos bases también necesita revisión.
- **Verificación:** consulta de documentación de los proveedores y términos publicados. Las referencias se documentarán en `docs/data_sources.md`.
- **Estado:** selección provisional; auditoría de los datos todavía pendiente.

## 2026-10-07 — 04. Entorno local e importación verificable

- **Realizado:** entorno `.venv`, instalación de DuckDB y pytest, `pyproject.toml`, exclusión de datos y artefactos de Git, catálogos de fuentes e importador con comprobaciones de integridad.
- **Realizado:** descarga y verificación de 67 archivos de Sackmann: partidos de 1968 a 2025, jugadores, rankings por década y documentación original.
- **En curso al registrar esta entrada:** descarga de 58 CSV de TennisMyLife, temporadas 1968 a 2025. No se pidió descargar archivos de partidos de 2026.
- **Código preparado:** controles internos de calidad y construcción de tablas de exploración en DuckDB/Parquet, con particiones de entrenamiento, evaluación, futuro y cuarentena.
- **Verificación:** la descarga de Sackmann terminó correctamente y los archivos coinciden con los hashes Git del catálogo. La ejecución del constructor y sus pruebas aún están pendientes.
- **Próximo paso:** finalizar TennisMyLife, comparar cobertura y discrepancias, comprobar el corte temporal y emitir los informes.

## 2026-10-07 — 05. Descargas completadas y snapshot verificado

- **Realizado:** descarga completa de 58 CSV ATP de TennisMyLife, 1968–2025; las dos fuentes están disponibles localmente.
- **Archivos:** originales y manifiestos en `data/raw/sackmann/` y `data/raw/tml/`; catálogos reproducibles en `configs/`.
- **Verificación:** segunda ejecución de ambos importadores: 67 archivos de Sackmann y 58 de TennisMyLife verificados sin sobrescribir originales.
- **Decisión:** registrar SHA-256 de TennisMyLife en el catálogo. Si cambia el archivo vivo del proveedor, el proceso debe fallar; conservar el snapshot local sigue siendo necesario para garantizar disponibilidad futura.
- **Estado:** completado para las temporadas solicitadas. No se descargaron archivos de partidos de 2026.

## 2026-10-07 — 06. Tablas locales y primera auditoría ejecutadas

- **Realizado:** creación de DuckDB y Parquet en `data/processed/stage_1_2025/`, exportación de rankings hasta 2024 y comparación de fuentes.
- **Particiones Sackmann:** 193.526 filas de entrenamiento provisional, 2.862 de evaluación y 1.552 en cuarentena temporal.
- **Particiones TennisMyLife:** 193.490 filas de entrenamiento provisional, 2.861 de evaluación y 1.575 en cuarentena temporal.
- **Rankings:** 3.292.949 filas; fecha máxima exportada 2024-12-30.
- **Comparación 1968–2024:** 173.221 partidos emparejados; 30.229 con algún campo comparable diferente. Una diferencia no determina automáticamente qué fuente está equivocada.
- **Comparación 2024:** 2.968 partidos emparejados; 89 con diferencias. Se observaron variantes de nombres que impiden emparejar otros registros con certeza.
- **Hallazgo:** ambas bases comparten contadores incoherentes en Machac–Navone, Roland Garros 2024. Se registra como DQ-001 sin inventar una corrección.
- **Verificación:** constructor ejecutado; corte comprobado en las tablas exportadas; cuatro finales de Grand Slam coinciden con referencias oficiales de ATP.
- **Entregables:** `docs/data_source_spike.md`, `docs/data_dictionary.md`, `docs/data_sources.md`, más `audit.json` y `discrepancies.jsonl` locales.
- **Estado:** auditoría inicial ejecutada. La fase 0 permanece abierta y `temporal_ready=false`; no hay modelo entrenado ni datos canónicos listos para entrenar.

## 2026-10-07 — 07. Discrepancia de ganador corroborada externamente

- **Hallazgo:** Sackmann registra a Struff como ganador del walkover ante Moutet en París 2024; TennisMyLife registra a Moutet.
- **Verificación externa:** ATP, crónica del 30/07/2024, e ITF, crónica posterior, confirman que Moutet avanzó sin jugar. Referencias completas en `docs/data_issues.md`.
- **Decisión:** DQ-002 queda corroborado; preservar el original y aplicar el tratamiento en la futura transformación canónica. Los walkovers no deberán alimentar Elo ni entrenamiento de resultados.
- **Archivos:** caso documentado y quinta comprobación oficial añadida a `configs/official_checks.json`.
- **Estado:** evidencia confirmada; aplicación de la limpieza todavía pendiente. La comprobación de Sackmann debe señalar la discrepancia, no ocultarla para que el informe parezca exitoso.

## 2026-10-07 — 08. Documentación y reglas de seguimiento

- **Realizado:** plan y README actualizados al esquema 2024→2025, después 2025→2026. Backup inglés preservado sin modificaciones.
- **Realizado:** registros de decisiones ADR-001 y ADR-002; `AGENTS.md` exige actualizar este log después de avances significativos.
- **Verificación:** el plan conserva sus 84 secciones y 78 bloques; el hash del backup inglés continúa siendo `8226029e8787b906809546bb7562f6c2ef721281fadbdd42692c2282fc6b338f`.
- **Reproducibilidad:** el constructor guarda un manifiesto con experimento, corte, versiones de Python/DuckDB, hashes del código/configuración y manifiestos de fuentes.
- **En curso:** ejecución final de pruebas y regeneración del informe con la quinta comprobación oficial.
- **Próximo trabajo:** resolver identidades y fechas/disponibilidad de resultados, clasificar estados de partido y aplicar limpieza trazable antes del primer motor Elo. La segunda etapa experimental sigue pendiente de la revisión de la primera.

## 2026-10-07 — 09. Verificación final de este avance

- **Pruebas automatizadas:** 15 pruebas pasan. Cubren corte de las dos etapas, cuarentena de eventos que cruzan el año, exclusión de rankings posteriores, detección de archivos alterados/faltantes, incoherencias de saque, emparejamiento sin depender del ganador y comprobación oficial del walkover invertido.
- **Ejecución con datos reales:** constructor final completado; informes y tablas regenerados con las cinco referencias oficiales.
- **Contraste oficial:** 9 de 10 comprobaciones por proveedor coinciden. La restante señala el ganador incorrecto de Sackmann en Moutet–Struff; es una discrepancia esperada y documentada, no un error de ejecución.
- **Integridad temporal de exportación:** ninguna fila de las vistas de entrenamiento pertenece a 2025 o tiene fecha de torneo posterior al 31/12/2024; el último ranking exportado sigue siendo 2024-12-30. Esto no resuelve la disponibilidad real de resultados dentro de cada torneo.
- **Reproducibilidad:** hashes del código/configuración del manifiesto final comprobados contra los archivos actuales; paquete instalado localmente con Python 3.13.7 y DuckDB 1.5.6. Versiones de dependencias registradas en `requirements-dev.lock`.
- **Repositorio:** verificado que `data/`, `.venv/` y `build/` están excluidos de Git. No se realizaron commits ni publicaciones.
- **Estado final del avance:** base local y auditoría inicial listas; fase 0 abierta, sin entrenamiento de modelos. Continúa pendiente la limpieza canónica y la resolución de cronología antes del motor Elo.

## 2026-10-07 — 10. Seguimiento simplificado por fases

- **Pedido del usuario:** un documento claro con checklist por fase, lo listo y lo pendiente; reducir la cantidad de detalles técnicos en las actualizaciones.
- **Realizado:** `ESTADO_DEL_PROYECTO.md` como punto principal de seguimiento, con situación actual, próximo paso y checklists para las fases y las dos etapas experimentales.
- **Realizado:** enlace destacado en el README y regla de mantenimiento en `AGENTS.md`. El log conserva la historia; los informes quedan como apoyo técnico.
- **Verificación:** revisión de estados contra los avances registrados y comprobación de enlaces locales. No se cambió código ni datos.
- **Estado:** completado. Seguimos en fase 0; la próxima tarea es resolver la cronología y las reglas de uso de datos dudosos.

## 2026-10-07 — 11. Reglas para datos dudosos y próximo paso temporal

- **Pedido del usuario:** continuar y aclarar qué necesita aportar para terminar la fase 0.
- **Decisión:** no se necesitan por ahora datos ni decisiones técnicas del usuario; continuar con la investigación pública autorizada.
- **Realizado:** reglas de limpieza definidas en `docs/data_issues.md`: correcciones con evidencia, resultados dudosos separados, estadísticas imposibles excluidas, faltantes preservados y walkovers/abandonos fuera de los primeros modelos de partidos completados.
- **Realizado:** reglas temporales explícitas; no inventar fechas ni disponibilidad a partir de ronda, numeración o semana del torneo. Si solo se conoce el día efectivo de finalización, no usar el resultado hasta el día siguiente en la zona horaria del evento.
- **Verificación externa:** documentación oficial de Roland Garros confirma reprogramaciones por lluvia y finalizaciones después de medianoche. La ficha oficial de Machac–Navone permite revisar marcador/duración, pero no resolvió los contadores incorrectos.
- **Seguimiento:** checklist actualizado; reglas de tratamiento definidas, con implementación pendiente para la fase 1. Las fechas y el cierre de la validación de fuentes siguen pendientes en fase 0.
- **Verificación de cambios:** revisión de documentación y enlaces locales. No se modificaron código, datos ni modelos.
- **Próximo paso:** comprobar la reconstrucción temporal con una muestra verificable y medir su cobertura. No se declaró cerrada la fase 0.


## 2026-10-07 — 12. Muestra temporal y controles ejecutados

- **Realizado:** nueve casos con fecha efectiva respaldada por ATP/Roland Garros; incluye cuatro finales, lluvia y reanudación, finalización después de medianoche y temporada 2025 iniciada en diciembre de 2024.
- **Implementación:** disponibilidad conservadora desde el siguiente día local, zonas horarias y corte UTC explícito. Temporada posterior al corte queda excluida; fecha desconocida no habilita el resultado.
- **Ejecución real:** `scripts/audit_temporal.py` verificó integridad de CSV y 18 coincidencias únicas, nueve por proveedor. Artefacto local con hashes de configuración y manifiestos; no se modificaron originales ni tablas de entrenamiento.
- **Verificación:** 24 pruebas pasan; incluyen lluvia, medianoche, cambio de horario estacional, fechas desconocidas, predicción sin zona horaria y cruce de año.
- **Cobertura:** ocho casos de 2024 por base, aproximadamente 0,26 % de sus registros anuales. No extrapolar a todo el historial ni afirmar disponibilidad histórica de publicaciones.
- **Estado:** fase 0 continúa abierta, sin modelos. Checklist actualizado.
- **Próximo paso:** encontrar y comprobar una fuente de fechas con cobertura mayor, cuantificar qué historial puede usarse y cerrar el alcance de validación adicional.


## 2026-10-07 — 13. Perfiles y compatibilidad de estilos

- **Pedido:** incorporar características individuales y dificultades frente a perfiles similares, diferenciando nivel y estilo; influencia aprendida, sin porcentaje arbitrario.
- **Realizado:** alcance integrado al plan y checklist de fases 3 y 5. Catálogo de nueve métricas observables, cálculo de numeradores/denominadores y auditoría repetible de entradas de 2024. No se tocaron datos de evaluación 2025/2026.
- **Ejecución:** 5.866 observaciones jugador-partido con métricas en Sackmann y 5.842 en TennisMyLife sobre 6.152 por proveedor. Verificados hashes de originales; filtros básicos excluyen incoherencias y partidos no completados. Cobertura exploratoria, no certificación de calidad o cronología.
- **Verificación:** 27 pruebas pasan; las nuevas comprueban devolución desde el rival, estadísticas imposibles, walkovers/abandonos, datos ausentes y denominadores nulos.
- **Decisiones:** perfiles previos al encuentro y por superficie; similitud sin información futura; efecto relativo a nivel/forma; regularización y comparación con/sin ajuste hasta 2024. No asignar etiquetas de revés o agresividad con estadísticas que no las miden.
- **Pendiente:** fechas y limpieza, perfiles históricos, datos adicionales de golpes/estilo, aprendizaje del ajuste y evaluación. Fase 0 permanece abierta; sin modelos entrenados.


## 2026-10-07 — 14. Cobertura de golpes MCP comprobada

- **Pedido:** empezar a conseguir datos adicionales de golpes y estilos.
- **Realizado:** repositorio original accesible; commit fijado y seis archivos descargados con hashes/tamaños registrados. Descargador ampliado para MCP y auditoría de cobertura repetible.
- **Resultado real:** 6.800 partidos con metadatos que superan controles básicos hasta 2024; 951 nombres, 232 con al menos diez encuentros y 141 con veinte. Alcaraz 149 y Fognini 46; sus muestras de 2024 son 43 y dos.
- **Calidad:** superficie inválida y dos filas de un identificador duplicado se separan sin corregir originales. Anomalía de fecha/identidad candidata en Sinner registrada para cotejo.
- **Verificación:** descarga con integridad comprobada, ejecución real de auditoría y 30 pruebas pasan. Nuevas pruebas cubren corte temporal, fechas inválidas, duplicados y superficie inválida. Estadísticas posteriores al corte no se incorporan al informe.
- **Límites:** presencia de tablas no valida sus contadores; cobertura desigual y captura selectiva. Fecha histórica no demuestra cuándo fue publicado el charting. No se construyeron perfiles ni se entrenó. Fase 0 abierta.
- **Próximo paso:** validar códigos y estadísticas en una muestra, resolver correspondencias con partidos históricos y preparar perfiles piloto por fecha/superficie. Checklist actualizado.


## 2026-10-07 — 15. Primeros perfiles piloto calculados

- **Pedido:** avanzar hacia un resultado concreto; considerar que llegar más lejos en torneos genera más partidos, además del sesgo de selección de charting.
- **Realizado:** constructor reproducible de perfiles MCP 2022–2024 para Alcaraz/Fognini, con once medidas, denominadores, cantidad de partidos y separación por superficie. Ocho perfiles, incluido Fognini/césped vacío.
- **Ejecución:** Alcaraz 129 partidos con métricas; Fognini once. Tasas de puntos 4–6 golpes: 2.834/5.151 (55,0 %) y 171/333 (51,4 %). Red: 2.072/2.831 y 118/149. No interpretar porcentajes como calidad pura ni ventaja H2H.
- **Verificación:** integridad de fuentes y ejecución real con conservación de puntos y validación numérica, sin rechazos de contadores en el piloto. Las 30 pruebas existentes siguen pasando; todavía no se añadieron pruebas específicas del constructor piloto.
- **Límites:** ventana elegida como exploración, sin optimizar en 2025; disponibilidad histórica no resuelta. No ajuste por fuerza/oponente ni similitud aprendida. Sin modelos y fase 0 abierta.
- **Próximo paso:** vincular partidos/perfiles a la base histórica, validar anotaciones y construir similitudes y comparación contra modelo de nivel. Checklist muestra resultados concretos.


## 2026-10-07 — 16. Universo top 500 y piloto top 350 ejecutados

- **Pedido:** avanzar con universo top 500 y piloto top 350 usando ranking histórico.
- **Realizado:** selección reproducible del ranking 30/12/2024; perfiles básicos agregados por jugador/superficie y generalización del constructor de estilos a candidatos del piloto. Faltantes y denominadores explícitos.
- **Resultado:** top 500: 356 con alguna estadística básica y 280 candidatos de identidad MCP; top 350: 296 con alguna estadística básica y 250 con alguna métrica de estilo. Solo 92 con al menos diez partidos de proporción de derecha.
- **Verificación:** ejecución con archivos originales verificados y 32 pruebas pasan. Dos nuevas pruebas verifican último ranking anterior al corte, ausencia de relleno con snapshots anteriores/futuros y rechazo de jugadores duplicados.
- **Límites:** candidatos por nombre exacto aún pendientes de revisión; ATP sin Challenger; limpieza/fechas y charting histórico sin resolver. Perfil presente no equivale a calidad suficiente. Sin entrenamiento ni similitudes todavía.
- **Seguimiento:** checklist y plan actualizados; fase 0 sigue abierta. Próximo paso: revisar identidades, completar Challenger y comparar perfiles para construir similitudes explicables.


## 2026-10-07 — 17. Challenger incorporado y cobertura ampliada

- **Pedido:** sumar estadísticas Challenger para jugadores de menor ranking.
- **Realizado:** descarga fijada de tres archivos 2022–2024 y manifiesto de integridad; descargador admite Challenger. Solo nivel C incorporado; previas ATP excluidas, cuadros/clasificación separados y duplicados puestos aparte.
- **Ejecución:** 18.128 filas Challenger principal y 9.755 clasificación en la ventana antes de filtros de estadísticas. Cuatro filas duplicadas excluidas. Perfiles top 350/500 regenerados.
- **Resultado:** cobertura básica 296→350 y 356→500, respectivamente; nueve métricas disponibles en All para los 500. 349/350 y 495/500 con al menos diez partidos de puntos ganados al saque; mínimo cinco. MCP no aporta nuevos golpes por esta descarga.
- **Verificación:** hashes/bytes y ejecución real; 33 pruebas pasan, incluida distinción QF vs Q2 y exclusión de previas ATP. Reconciliados numeradores/denominadores/conteos de los tres grupos con agregación conjunta en los 500 perfiles.
- **Límites:** perfiles descriptivos sin ajuste por rival; fuentes Challenger no contrastadas aún; fechas/identidades sin resolver para entrenamiento. No modelos. Fase 0 abierta.
- **Seguimiento:** checklist actualizado; siguiente tarea: revisión de identidades y similitudes explicables con muestras y nivel explícitos.


## 2026-10-07 — 18. Búsqueda de golpes detallados Challenger

- **Pedido:** buscar fuentes de derecha/revés, intercambios y red en Challenger.
- **Realizado:** búsqueda web en fuentes originales y conteo local MCP, verificando hashes y corte 2022–2024.
- **Hallazgo:** 122 encuentros etiquetados CH/Challenger, con tablas de golpes/intercambios/red ya incluidos en perfiles. Candidatos del top 350/500: 111/124, solo cinco con al menos cinco encuentros CH. No se amplió la cobertura anterior.
- **Fuentes adicionales:** API de perfiles revisada deriva del MCP; dataset de puntos no contiene golpes. Tennis IQ anuncia acceso para jugadores/coaches sin descarga pública confirmada. Challenger TV posible vía para anotación manual, pendiente revisar archivo histórico.
- **Verificación:** conteo ejecutado y artefacto local; no cambió código ni se entrenó. Clasificación por etiqueta y vínculos de nombre siguen siendo candidatos.
- **Estado:** fase 0 abierta. Recomendación: aprovechar datos existentes y anotar selectivamente videos si hace falta, en vez de asumir cobertura universal o comprar un derivado del mismo MCP.


## 2026-10-07 — 19. Primeras similitudes explicables

- **Pedido:** avanzar tras la búsqueda de golpes Challenger.
- **Realizado:** comparación top 350 con distancias estandarizadas, siete métricas básicas por circuito y seis de golpes; superficies separadas, mínimo diez partidos por cada métrica, faltantes excluidos. Top cinco vecinos con motivos/diferencia principal y evidencia.
- **Ejecución:** población All ATP 187, Challenger principal 307, clasificación 179, MCP 92. Vecinos iniciales: Alcaraz/Nadal en básico y Alcaraz/Griekspoor en golpes; Fognini/Karatsev y Fognini/Cobolli, respectivamente. No interpretarlos como equivalencia táctica.
- **Verificación:** ejecución real, hash de entrada y escalas conservadas; 36 pruebas pasan. Nuevas pruebas verifican faltantes/muestra mínima, exclusión del propio jugador, invariancia al cambio de escala, simetría y ausencia de resultados falsos con características constantes.
- **Límites:** umbral exploratorio, sin ajuste por oposición ni validación de estabilidad, datos retrospectivos e identidades candidatas. No aprendizaje del efecto sobre probabilidades. Fase 0 abierta.
- **Seguimiento:** checklist muestra ejemplos y límites. Próximo: estabilidad por superficie/muestra y vinculación con modelo de nivel y encuentros históricamente elegibles.


## 2026-10-07 — 20. Estabilidad del conjunto top 350 medida

- **Pedido:** comprobar estabilidad y producir un informe del conjunto antes de atribuir influencia predictiva a perfiles.
- **Realizado:** tres pruebas retirando un año; perfiles básicos y de golpes recalculados por circuito/superficie; misma población común para comparar top cinco vecinos. Exportado diagnóstico y lista de revisión de 350 jugadores.
- **Resultado real:** comparables en todas/retención ≥3 en todas: ATP 134/44, Challenger principal 254/30, clasificación 88/10, MCP 44/28. No extrapolar a toda la población ni sumar grupos. Césped MCP no evaluable (3–5 participantes por prueba).
- **Verificación:** originales verificados, hashes de perfiles y ejecución completa; 39 pruebas pasan. Nuevas pruebas verifican retención completa sin cambios, ausencia de resultado con muestra insuficiente y eliminación del jugador no elegible de ambas poblaciones.
- **Conclusión:** vecindades sensibles especialmente en datos básicos Challenger; no asignarles aún influencia en probabilidades. Cambios pueden ser evolución/oposición/selección además de ruido. Umbral de tres vecinos exploratorio.
- **Pendiente:** revisión de identidades, fechas y anotaciones, referencia de nivel/Elo y efecto relativo de perfiles. No se entrenó ni se declaró completada la fase 0.
- **Seguimiento:** checklist actualizado con resultados del conjunto. Próximo: cotejar correspondencias y vincular encuentros temporalmente elegibles antes de Elo.


## 2026-10-07 — 21. Perfil de golpes unificado entre superficies

- **Pedido:** no dividir el tipo de golpes por superficie.
- **Realizado:** perfil MCP global por jugador/período; constructores de perfiles, similitudes y estabilidad generan únicamente All para golpes. Saque/devolución conserva circuito y superficie; cancha permanece como contexto del futuro modelo. Plan y checklist actualizados.
- **Ejecución:** perfiles top 350, piloto inicial, similitudes y tres pruebas de estabilidad regenerados. Se verificó que no quedan vistas de golpes Hard/Clay/Grass en los artefactos actuales. Los globales conservan 92 elegibles y 28/44 que cumplen retención en las tres pruebas.
- **Verificación:** 39 pruebas pasan; inspección automática de los perfiles y vistas actuales confirma el cambio y la conservación de separación básica.
- **Límites:** unificar aumenta el uso de evidencia conjunta, pero la mezcla de superficies observadas aún puede influir en las tasas. No se entrenó; fase 0 abierta y continúa trabajo de identidades/cronología.


## 2026-10-07 — 22. Explorador HTML listo para probar

- **Pedido:** tener una interfaz visible y alojable en GitHub para explorar.
- **Realizado:** página estática en docs, CSS adaptable y JavaScript sin dependencias; búsqueda de 350 jugadores, comparador de tasas/evidencia, filtros de circuito/superficie para básico, golpes globales y cinco vecinos explicados con acceso al comparador. Faltantes y límites explícitos.
- **Datos:** exportador de agregados con hashes y detección de perfiles/similitudes/estabilidad desactualizados. Snapshot incluido, originales excluidos. Funciona sin fetch, apto para abrir HTML local y rutas relativas Pages. Atribución/licencia de derivados en la interfaz.
- **Verificación:** snapshot regenerado, sintaxis JavaScript comprobada, 39 pruebas Python pasan. Chrome headless: vista visual revisada y ocho comprobaciones de roster, búsqueda, golpes globales, métricas, selección de vecino, filtro de evidencia, Challenger y faltantes pasan. Se retiró el arnés temporal del sitio.
- **Publicación:** preparada carpeta docs/.nojekyll y procedimiento oficial en README; no publicada. Sin remoto configurado y raíz Git en directorio padre. Se solicitó URL del repositorio destino. No commits/pushes ni cambios de Git del padre.
- **Estado:** fase 0 sigue abierta; prototipo exploratorio de interfaz adelantado para facilitar seguimiento. Sin probabilidades ni modelo entrenado.


## 2026-10-07 — 23. Repositorio público y publicación inicial

- **Pedido explícito:** crear repositorio, subir el proyecto y configurar GitHub para usar una URL pública.
- **Realizado:** cuenta isardi4 verificada; Git inicializado en la carpeta del proyecto sin alterar el padre. Repositorio público `isardi4/tennis-intelligence-lab` creado y remoto origin asociado.
- **Preparación:** 39 pruebas pasan y sintaxis JavaScript comprobada. Publicar solo código/documentación y agregado web; originales/entorno/artefactos permanecen excluidos.
- **En curso:** commit inicial, push y activación GitHub Pages desde main/docs. Falta comprobar respuesta pública.


## 2026-10-07 — 24. Publicación verificada en GitHub Pages

- **Completado:** commit inicial subido a main en https://github.com/isardi4/tennis-intelligence-lab. Pages activado desde main/docs, URL https://isardi4.github.io/tennis-intelligence-lab/, HTTPS obligatorio y homepage del repositorio configurada.
- **Verificación externa:** GitHub informa build built sin errores. Descargados HTML, JavaScript, CSS y snapshot desde la URL pública; hashes coinciden con archivos locales. Los archivos raw, entorno y artefactos locales no están versionados.
- **Seguimiento:** README y checklist enlazan página y repositorio; publicación marcada completada. Futuras actualizaciones de docs en main se publican automáticamente.
- **Estado del producto:** explorador público funcional, sin probabilidades; fase 0 de datos sigue abierta.


## 2026-10-07 — 25. Comparador compacto con barras verticales

- **Pedido:** comparaciones más amigables, menos espacio vacío y menos desplazamiento vertical.
- **Realizado:** gráfico de columnas agrupadas, dos colores con leyenda, porcentajes visibles y escala común 0–100 %. Nombres cortos con definición completa accesible, evidencia en desplegable/tooltip y desplazamiento horizontal del gráfico en móvil. Ausencia explícita S/D sin inventar valores.
- **Verificación:** inspección visual en Chrome y comprobaciones de siete/seis categorías, altura exacta según tasa, evidencia cerrada, tooltip de muestra, gráfico inferior a 300 px, cambio de vecino y datos faltantes. 39 pruebas Python pasan y sintaxis JavaScript válida. Se retiró el arnés temporal.
- **Datos:** snapshot y métricas permanecen iguales. No cambia ninguna predicción o modelo.
- **Publicación:** actualización preparada para push a main, que publica automáticamente mediante Pages; comprobar recursos públicos tras la construcción.
