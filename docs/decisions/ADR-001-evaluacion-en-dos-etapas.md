# ADR-001 — Evaluación en dos etapas

Fecha: 2026-10-07. Estado: aceptada por instrucción del usuario.

## Contexto

El plan original proponía entrenamiento hasta 2025 y evaluación sobre 2026. Se solicita un ensayo previo sobre 2025 para revisar el enfoque antes de la comprobación final.

## Decisión

1. Etapa experimental 1: desarrollar, seleccionar variables y ajustar hiperparámetros únicamente con datos hasta 2024-12-31. Usar validación temporal interna. Guardar configuración, versión de datos, parámetros y resultado inicial antes de aprender de los errores de 2025.
2. Registrar las mejoras posteriores inspiradas por 2025 como desarrollo, sin llamar prueba independiente a una nueva evaluación sobre el mismo año.
3. Etapa experimental 2: entrenar con información hasta 2025-12-31 y fijar modelo/configuración antes de evaluar 2026. No ajustar usando resultados de 2026.
4. En cada etapa, separar información totalmente congelada de actualización histórica secuencial con parámetros congelados.

Estas etapas experimentales son distintas de las fases de ingeniería del plan: la fase 2 de ingeniería sigue siendo el motor Elo.

## Alternativas

- Mantener solo el ensayo original sobre 2026: no proporciona la revisión previa solicitada.
- Ajustar y medir repetidamente sobre 2025 como si continuara siendo un conjunto no visto: produce una estimación optimista.

## Consecuencias

La configuración está en `configs/experiments.json`. La CLI actual solo habilita la primera etapa. Las temporadas que empiezan en el año anterior quedan en cuarentena hasta resolver fechas reales. Importar datos actuales no demuestra que sus correcciones fueran conocidas históricamente; esa limitación debe acompañar los resultados.
