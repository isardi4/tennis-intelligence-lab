# ADR-002 — Fuentes múltiples y semántica temporal

Fecha: 2026-10-07. Estado: implementada para exploración; resolución canónica pendiente.

## Contexto

El usuario solicita verificar Sackmann contra otras fuentes públicas. El repositorio original devuelve 404 y los proveedores no garantizan datos sin errores. Las columnas de fecha y numeración no describen necesariamente el momento real de cada partido.

## Decisión

- Usar la revisión fija del espejo de Sackmann y un snapshot local con hashes de TennisMyLife para la comparación masiva.
- Usar ATP Tour como referencia oficial de hechos puntuales hasta contar con acceso y condiciones adecuados para una comparación más amplia.
- Excluir Tennis-Data de la ingesta automatizada por sus restricciones publicadas. No contar espejos ni servicios derivados como fuentes independientes.
- Conservar las discrepancias sin decidir por mayoría cuál es el dato correcto.
- Mantener `tournament_start_date` separado de una futura `match_date`; no inventar fecha de partido ni cronología a partir de `match_num`.
- Poner en cuarentena las temporadas que no coinciden con el año de inicio del torneo; no entrenar con eventos de 2025 iniciados en diciembre de 2024.
- Mantener `temporal_ready=false` hasta verificar disponibilidad histórica de resultados o definir una política conservadora verificable.

## Alternativas

- Usar solo Sackmann: no satisface la validación solicitada.
- Usar un espejo o Ultimate Tennis Statistics como confirmación independiente: comparten procedencia y pueden compartir errores.
- Ordenar partidos por `tourney_date, match_num`: no garantiza que un resultado fuera conocido antes del siguiente.

## Consecuencias

La auditoría detectó un registro de 2024 con contadores de saque imposibles que ambas bases comparten. Sus datos se preservan para revisión. Todavía no hay tres bases completas, independencia total demostrada, fechas exactas de todos los partidos ni modelos entrenados. La descarga de 2026 puede contener correcciones retrospectivas: cualquier reconstrucción histórica deberá declarar esta diferencia frente a un snapshot publicado en aquel momento.
