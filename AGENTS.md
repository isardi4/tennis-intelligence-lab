# Instrucciones del proyecto

Antes de trabajo significativo, leer `ESTADO_DEL_PROYECTO.md`, `TENNIS_INTELLIGENCE_LAB_PROJECT_PLAN.md`, `README.md` y las últimas entradas de `docs/work_log.md`.

- Etapa experimental inicial: entrenamiento y ajuste hasta 2024-12-31; evaluación inicial sobre 2025. La segunda etapa usa entrenamiento hasta 2025-12-31 y evaluación sobre 2026, después de revisar la primera.
- No confundir las etapas experimentales con las fases de ingeniería del plan.
- No presentar una evaluación usada para ajustar el modelo como una prueba independiente.
- No equiparar `tourney_date` con fecha de partido ni ordenar actualizaciones Elo con `match_num` sin verificar su semántica.
- Contrastar las fuentes y documentar discrepancias. Un espejo o derivado no demuestra independencia. No corregir datos silenciosamente.
- Mantener datos originales, entorno virtual y artefactos fuera de Git.
- Actualizar `docs/work_log.md` después de cada avance significativo: trabajo, hallazgos, verificación y pendientes. No marcar como completado lo que no se ejecutó y verificó.
- Actualizar también `ESTADO_DEL_PROYECTO.md`, el documento principal de seguimiento del usuario. Mantener checklists fieles al estado real. Comunicar cada entrega con fase actual, lo terminado, lo pendiente y el próximo paso; reservar detalles técnicos y listas de archivos para documentación de apoyo.
- Verificar cambios relevantes con `.venv/bin/python -m pytest -q`. La construcción local se ejecuta con `.venv/bin/python scripts/build_dataset.py`.
