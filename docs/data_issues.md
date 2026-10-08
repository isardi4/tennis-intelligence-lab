# Casos de calidad de datos

Los archivos originales son inmutables. Una decisión de corrección exige evidencia externa y se aplica en una transformación explícita posterior, nunca editando el CSV descargado.

## Reglas definidas para la limpieza de la fase 1

Estas reglas cierran la decisión de cómo tratar datos dudosos. **Todavía deben implementarse y comprobarse en la base limpia.** No convierten las tablas de exploración actuales en datos listos para entrenar.

| Situación | Tratamiento |
|---|---|
| Error con corrección corroborada oficialmente | Aplicar la corrección en una transformación, conservando valor original, evidencia y motivo. |
| Fuentes que discrepan sobre ganador o marcador sin evidencia suficiente | Separar el encuentro; no usarlo para entrenamiento ni Elo hasta resolver la discrepancia. |
| Contadores de saque imposibles | Excluir las estadísticas de saque/resto de ese encuentro. Conservar el resultado solo si su validez se ha verificado por separado. |
| Estadísticas faltantes | Mantenerlas como desconocidas. No convertirlas en cero ni inventarlas. |
| Victoria sin jugar (walkover) | Registrar el avance en el cuadro; excluir de entrenamiento de resultados, carga de partidos y actualizaciones de Elo. |
| Abandono o descalificación | Clasificar por separado y excluir de los primeros modelos de partidos completados. |
| Identidad o fecha sin resolver | Mantener el registro separado hasta contar con una correspondencia o fecha verificable. |
| Superficie sin verificar | No asignarla por intuición ni utilizar el registro para Elo por superficie. |
| Ranking discrepante | Reconstruirlo desde la serie histórica disponible antes de la predicción; no decidirlo por mayoría de fuentes. |

La corrección de un campo no demuestra que todos los demás sean correctos. Se registrará cuántos encuentros y estadísticas quedan excluidos, por año y torneo, para no ocultar el efecto de la limpieza.

## Reglas temporales para continuar la investigación

- Distinguir inicio del torneo, inicio del partido, finalización y disponibilidad del resultado.
- No deducir el orden de los partidos de `match_num`, ni asignar fechas por ronda o sumar días arbitrariamente al inicio del torneo.
- Si solo conocemos el día real de finalización, usar el resultado a partir del día siguiente en la zona horaria del torneo. Si desconocemos el día de finalización, el resultado no habilita actualizaciones históricas.
- Si el partido termina después de medianoche o se reanuda otro día, utilizar la fecha efectiva de finalización, no la originalmente programada.
- El entrenamiento hasta 2024 requiere resultados finalizados y disponibles hasta el corte; la semana del torneo por sí sola no demuestra que lo estén.

La [crónica oficial de Roland Garros del 30/05/2024](https://www.rolandgarros.com/en-us/article/rg2024-day-5-as-it-happens-thursday-30-may) documenta encuentros reprogramados por lluvia y uno finalizado después de medianoche. Esto confirma que un calendario o día programado no basta para conocer cuándo estuvo disponible un resultado. La [ficha oficial Machac–Navone de 2024](https://www.rolandgarros.com/fr-fr/matches/2024/SM046) también permite corroborar el marcador y la duración; no se recuperaron allí los contadores necesarios para corregir DQ-001.

**Siguiente comprobación:** probar la reconstrucción de fechas con una muestra de partidos y fuentes oficiales, incluyendo reprogramaciones, cruces de año y encuentros del mismo día. Luego medir cuánto del historial puede cubrirse. La cronología completa continúa pendiente y `temporal_ready` sigue siendo `false`.

## DQ-001 — Contadores de segundo saque incoherentes

- **Evento:** Roland Garros 2024, Tomas Machac frente a Mariano Navone.
- **Fuentes afectadas:** Sackmann y TennisMyLife.
- **Evidencia interna:** `w_svpt=135`, `w_1stIn=122`, `w_2ndWon=21`. Las oportunidades de segundo saque son 135 − 122 = 13; 21 puntos ganados no pueden caber en 13 oportunidades.
- **Conclusión:** al menos uno de los contadores es incorrecto. Que ambas bases coincidan no resuelve la inconsistencia.
- **Estado:** pendiente de corroboración oficial de los contadores exactos. No se adivina el valor correcto.
- **Tratamiento pendiente:** marcar estadísticas como no válidas para generar variables hasta resolver la contradicción. Esto no demuestra que el ganador o el marcador estén mal.

## DQ-002 — Ganador invertido en un walkover

- **Evento:** Juegos Olímpicos de París 2024, segunda ronda (`R32`), Corentin Moutet frente a Jan-Lennard Struff.
- **Registro Sackmann:** `2024-0096`, ganador Struff, perdedor Moutet, marcador `W/O`.
- **Registro TennisMyLife:** `2024-96`, ganador Moutet, perdedor Struff, marcador `W/O`.
- **Evidencia externa:** la [crónica oficial de ATP del 30/07/2024](https://www.atptour.com/en/news/zverev-machac-paris-olympics-tuesday-2024) confirma que Moutet recibió el walkover. La [crónica oficial de ITF](https://www.itftennis.com/en/news-and-media/articles/tommy-paul-ends-the-hopes-of-moutet-and-france-at-paris-2024/) también confirma que avanzó sin jugar contra Struff.
- **Conclusión:** el ganador informado por Sackmann en ese registro está invertido; el registro de TennisMyLife coincide con ambas referencias oficiales.
- **Estado:** hecho corroborado; transformación canónica todavía pendiente. Se conserva el registro original y la comprobación en `configs/official_checks.json`.
- **Tratamiento pendiente:** reflejar que Moutet avanzó por walkover, sin computarlo como partido disputado ni usarlo para actualizar Elo o entrenar resultados. La clasificación de walkovers se implementará en la limpieza canónica.

## Alcance

Estos casos no demuestran que toda una base sea correcta o incorrecta. El informe registra otras discrepancias; sus causas permanecen pendientes. El próximo paso es incorporar una cola de revisión y reglas de limpieza trazables, con controles antes del entrenamiento.


## Muestra temporal ejecutada — 07/10/2026

Se contrastaron nueve encuentros con publicaciones oficiales. El registro reproducible está en `configs/temporal_sample.json`; `.venv/bin/python scripts/audit_temporal.py` verifica los hashes de los CSV usados, exige una coincidencia única por proveedor y escribe `data/processed/stage_1_2025/temporal_audit.json`. No modifica los originales ni habilita las tablas de exploración para entrenar.

| Caso | Finalización comprobada, día local | Evidencia |
|---|---|---|
| Final Australian Open, Sinner–Medvedev | 28/01/2024 | [ATP](https://www.atptour.com/en/news/medvedev-sinner-australian-open-2024-final) |
| Final Roland Garros, Alcaraz–Zverev | 09/06/2024 | [ATP](https://www.atptour.com/en/news/alcaraz-zverev-roland-garros-2024-final) |
| Final Wimbledon, Alcaraz–Djokovic | 14/07/2024 | [ATP](https://www.atptour.com/en/news/alcaraz-djokovic-wimbledon-2024-final) |
| Final US Open, Sinner–Fritz | 08/09/2024 | [ATP](https://www.atptour.com/en/news/sinner-fritz-us-open) |
| Hurkacz–Nakashima, Roland Garros R64 | 30/05/2024; iniciado el 29/05 | [Lluvia, ATP](https://www.atptour.com/en/news/rain-roland-garros-2024-wednesday), [reanudación y resultado, Roland Garros](https://www.rolandgarros.com/en-us/article/rg2024-day-5-as-it-happens-thursday-30-may) |
| Djokovic–Musetti, Roland Garros R32 | 02/06/2024, después de medianoche | [Roland Garros](https://www.rolandgarros.com/fr-fr/article/novak-djokovic-victoire-lorenzo-musetti-troisieme-tour-cinq-sets-nuit/) |
| Djokovic–Carballes Baena, Roland Garros R64 | 30/05/2024 | [Roland Garros](https://www.rolandgarros.com/en-us/article/rg2024-day-5-as-it-happens-thursday-30-may) |
| Dimitrov–Marozsan, Roland Garros R64 | 30/05/2024 | [Roland Garros](https://www.rolandgarros.com/en-us/article/rg2024-day-5-as-it-happens-thursday-30-may) |
| Djokovic–Hijikata, Brisbane R32, temporada 2025 | 31/12/2024 | [ATP](https://www.atptour.com/en/news/djokovic-hijikata-brisbane-2025-tuesday) |

**Resultado:** 9 casos y 18 vínculos únicos comprobados. Los ocho casos de 2024 representan aproximadamente el 0,26 % de los 3.076 registros de ese año en cada base; la muestra es dirigida y no permite estimar precisión global. La fecha de torneo de Roland Garros aparece como 27/05 en Sackmann y 26/05 en TennisMyLife: ninguna sustituye el día efectivo de estos encuentros.

**Control implementado:** un resultado con día conocido se considera utilizable por política desde la medianoche siguiente en la zona del evento, convertida a UTC. No se usa el mismo día, ni se inventa una hora. Fechas de finalización desconocidas no habilitan resultados; predicciones sin zona horaria se rechazan. Para entrenamiento, el corte inclusivo de fecha se interpreta en UTC, con límite exclusivo al comienzo del día siguiente; además se exige temporada no posterior al año de corte. Por eso Brisbane de la temporada 2025 queda excluido, aunque el encuentro haya terminado en 2024.

**Límites:** esta política no demuestra cuándo se publicó el resultado ni cuándo se corrigieron las estadísticas. Las fechas se registran con evidencia revisada manualmente; el script automatiza vinculación y reglas, no verifica automáticamente el contenido actual de las páginas. No se han validado todos los resultados o estadísticas de la muestra, ni construido una cronología completa. `temporal_ready` sigue en `false`.


## MCP-001 — Metadatos desplazados y duplicados

En el snapshot MCP fijado, `20240915-M-Davis_Cup_World_Group-RR-Tallon_Griekspoor-Flavio_Cobolli` tiene `Surface=Eva Asderaki-Moore`, que no es una superficie válida. Se excluye del listado exploratorio; no se corrige por inferencia. El identificador `20240915-M-Davis_Cup_World_Group-RR-Botic_Van_De_Zandschulp-Matteo_Berrettini` aparece duplicado, incluida una fila con `Date=RR` y nombres `R`. Ambas filas del identificador quedan separadas para revisión. Originales conservados.

La distribución de Jannik Sinner contiene además un registro fechado en 2013. Se registra como candidato para cotejo de identidad/fecha, no como error demostrado ni como evidencia de su perfil en ese año. Los listados exploratorios aún pueden contener incoherencias no detectadas.
