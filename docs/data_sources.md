# Fuentes de datos y condiciones de uso

Revisión realizada el 2026-10-07. Que una página sea pública no demuestra que sus registros sean correctos ni que su licencia permita todos los usos. Los datos originales y derivados permanecen fuera de Git.

## 1. Jeff Sackmann / Tennis Abstract

```yaml
source_name: Jeff Sackmann / Tennis Abstract — ATP
source_url: https://github.com/JeffSackmann/tennis_atp
mirror_url: https://github.com/Aneeshers/tennis-sackmann-archive
revision: 83733587353df8a41f2fd4f516147d5aa83f5a8d
license: CC BY-NC-SA 4.0
commercial_use_allowed: false
redistribution_allowed: true, bajo las condiciones de la licencia
attribution_required: true
raw_data_committed_to_repo: false
notes: El repositorio original devolvió HTTP 404; se usa un espejo archivado.
```

La atribución corresponde a **Jeff Sackmann / Tennis Abstract**. La documentación original archivada confirma atribución, uso no comercial y compartir adaptaciones bajo la misma licencia. Se verificaron el [archivo y su documentación](https://github.com/Aneeshers/tennis-sackmann-archive) y las [condiciones de CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Se descargaron 58 archivos anuales de individuales de nivel tour (1968–2025), una tabla de jugadores, seis archivos de rankings por década y dos archivos de documentación. Se excluyeron dobles, clasificación, Challenger y archivos de partidos de 2026. Los archivos de nivel tour también contienen Davis Cup, otros eventos por equipos y Juegos Olímpicos: el alcance final requiere filtros explícitos.

`configs/sackmann_source.json` fija URLs y hashes Git del proveedor. `data/raw/sackmann/manifest.json` registra además SHA-256 y fecha de descarga. El espejo preserva la misma fuente y **no cuenta como comprobación independiente**.

## 2. TennisMyLife

```yaml
source_name: TennisMyLife — ATP historical match database
source_url: https://stats.tennismylife.org/tennis-match-database
catalog_url: https://stats.tennismylife.org/api/data-files
revision: snapshot-2026-10-07
license: MIT, declarada en la página de la base de datos
commercial_use_allowed: declarado por MIT; no se ha verificado la cadena de derechos de datos externos
redistribution_allowed: declarada por MIT; no se redistribuyen archivos en este proyecto
attribution_required: conservar los avisos aplicables; citar TennisMyLife y el origen
raw_data_committed_to_repo: false
notes: API pública de descarga; utiliza IDs de jugadores ATP y datos que pueden corregirse posteriormente.
```

La [página del proveedor](https://stats.tennismylife.org/tennis-match-database) ofrece descarga de CSV mediante una API pública y declara licencia MIT. También describe recopilación de datos ATP y enriquecimiento con otras referencias. Esa declaración **no prueba que cada fila sea independiente de Sackmann**, ni permite asumir que se hayan eliminado las condiciones de fuentes ajenas.

Se descargaron 58 archivos ATP anuales de 1968 a 2025. `configs/tml_source.json` contiene el SHA-256 de cada archivo obtenido; las siguientes ejecuciones deben coincidir con esos bytes. El proveedor publica archivos vivos y no una URL inmutable: si cambia un archivo, la descarga se detendrá por discrepancia. Los hashes permiten detectar cambios, pero la reproducción exacta futura depende de conservar el snapshot local o de que el proveedor mantenga esos bytes.

Las categorías 250/500 aportan detalle adicional respecto de `A` en Sackmann. Su `tourney_date` también representa la semana del torneo. No se importa como fecha de partido.

## 3. ATP Tour — comprobaciones oficiales

```yaml
source_name: ATP Tour — resultados y crónicas oficiales
source_url: https://www.atptour.com/en/scores/results-archive
license: no se ha verificado una licencia abierta para descarga masiva
commercial_use_allowed: no verificado
redistribution_allowed: no verificado para conjuntos completos
attribution_required: citar la página oficial consultada
raw_data_committed_to_repo: false
notes: comprobación puntual de hechos; parte del archivo devuelve HTTP 403.
```

Se verificaron cuatro finales de Grand Slam de 2024 y un walkover olímpico mediante crónicas oficiales indexadas. `configs/official_checks.json` conserva los hechos contrastados, las referencias y la fecha de consulta; no copia artículos ni representa una importación completa de ATP.

- [Australian Open](https://www.atptour.com/en/news/medvedev-sinner-australian-open-2024-final).
- [Roland Garros](https://www.atptour.com/en/news/alcaraz-zverev-roland-garros-2024-final).
- [Wimbledon](https://www.atptour.com/es/news/wimbledon-2024-domingo-final-alcaraz-djokovic).
- [US Open](https://www.atptour.com/en/news/sinner-fritz-us-open).
- [Walkover Moutet–Struff, París 2024](https://www.atptour.com/en/news/zverev-machac-paris-olympics-tuesday-2024), corroborado también por [ITF](https://www.itftennis.com/en/news-and-media/articles/tommy-paul-ends-the-hopes-of-moutet-and-france-at-paris-2024/).

Estas referencias corroboran ganador y marcador; Wimbledon también permite contrastar duración. Todavía no corroboran todos los contadores de saque, rankings o fechas de todos los partidos.

## Fuentes revisadas sin importar

**Tennis-Data:** la [página de contacto](https://www.tennis-data.co.uk/contact.php) restringe el uso para productos comerciales o de entrenamiento con bots/scrapers/IA. Solo se revisó su documentación, sin descargar sus archivos de partidos. Sus notas además distinguen fechas de partido de fechas de inicio de torneo en años antiguos; no ofrece los mismos contadores detallados de saque.

**Ultimate Tennis Statistics:** su [documentación de procedencia](https://www.ultimatetennisstatistics.com/about) indica que utiliza Sackmann con correcciones y adiciones. Puede servir para investigar diferencias, pero no cuenta como una fuente plenamente independiente de Sackmann.

## Cobertura y límites de la triangulación

| Información | Sackmann archivado | TennisMyLife | ATP consultado |
|---|---|---|---|
| Resultados históricos | CSV 1968–2025 descargados | CSV 1968–2025 descargados | Cuatro finales y un walkover verificados |
| Contadores de saque | Presentes en parte de los partidos | Presentes en parte de los partidos | No importados masivamente |
| Ranking en el torneo | Columnas y series históricas | Columnas por partido | No importado masivamente |
| Jugadores | Tabla de metadatos actual | IDs ATP y metadatos por partido | Referencia oficial de identidades |
| Fecha exacta de partido | No garantizada | No garantizada | Pendiente reconstrucción sistemática |
| ATP 250 / ATP 500 | Frecuentemente agrupados en `A` | Más detalle de categoría | Pendiente calendario completo |
| Cuadros históricos | Resultados por ronda; no snapshot previo | Resultados por ronda; no snapshot previo | Pendiente adquisición |

Hay **dos bases descargadas y una referencia oficial puntual**. Todavía no hay tres fuentes completas con toda la información solicitada ni independencia total demostrada. Los registros discrepantes quedan pendientes de resolución y no se decide su verdad por mayoría de proveedores.


## Match Charting Project — cobertura auditada el 07/10/2026

Fuente: [repositorio original](https://github.com/JeffSackmann/tennis_MatchChartingProject). Versión fijada: `1813a1309b7ed7ebf1c7e884b32bf675d00e4edf`. Se descargaron seis archivos: README/licencia, diccionario, metadatos masculinos, ShotTypes, Rally y NetPoints. Configuración con hashes y tamaños en `configs/mcp_source.json`; originales preservados en `data/raw/mcp`. El descargador existente admite `--source mcp` y verifica esta versión.

La [documentación del proyecto](https://github.com/JeffSackmann/tennis_MatchChartingProject#readme) describe captura por colaboradores y licencia CC BY-NC-SA 4.0. No contar esta fuente como validación completamente independiente de Sackmann. Se acepta como candidata para investigación no comercial; no se descargaron videos ni se asumieron derechos adicionales.

Auditoría reproducible: `scripts/audit_charting.py`. De 7.566 filas de metadatos, 763 tienen fecha posterior a 2024 y se excluyen antes de consultar estadísticas; dos filas con el mismo identificador se separan; una superficie inválida también se separa. Quedan 6.800 encuentros para explorar, con 951 nombres distintos, sin resolución canónica de identidades. Distribución: 4.347 dura, 1.669 arcilla, 784 césped. Solo 232 nombres tienen al menos diez encuentros, 141 al menos veinte y 59 al menos cincuenta. No son umbrales de suficiencia predictiva: solo descripción de cobertura.

Ejemplos: Alcaraz 149 encuentros (148 con filas de ShotTypes/Rally/NetPoints); Fognini 46 (46 con ShotTypes/Rally, 45 con NetPoints). Presencia de filas no demuestra integridad de cada característica, ausencia de errores ni disponibilidad histórica. Sus muestras de 2024 son 43 y dos encuentros, respectivamente. La selección por colaboradores puede sesgar superficies, rivales, rondas y jugadores; no extrapolar un perfil estático de carrera a cualquier año.

Artefactos locales: `charting_coverage.json` y `charting_players.json`, con distribución por nombre, año, superficie y presencia de cada tabla. No se asignaron etiquetas tácticas ni se entrenó un modelo.

Pendiente: comprobar significado de códigos de golpe, consistencia numérica y duplicados en agregados, cotejar una muestra con fuentes oficiales o video, resolver identidades/fechas efectivas y medir cobertura respecto de la población ATP objetivo. La fecha declarada de un partido no garantiza día efectivo de finalización ni timestamp de publicación del charting; un partido antiguo pudo haberse anotado recientemente.


## Challenger 2022–2024 incorporado

Mismo espejo y commit de Sackmann ya registrado: `83733587353df8a41f2fd4f516147d5aa83f5a8d`, carpeta `atp`, archivos `atp_matches_qual_chall_2022.csv`, `2023.csv` y `2024.csv`. Configuración independiente `configs/challenger_source.json`, con tamaño y Git blob hash comprobados contra el árbol del commit. Licencia del upstream ya documentada; no es una fuente independiente nueva. Originales en `data/raw/challenger`, descarga repetible con `--source challenger`.

Los archivos contienen 31.869 filas: 27.885 de nivel C y 3.984 de previas ATP, Grand Slam y Masters. Se selecciona solo C; clasificación Q1/Q2/Q3 separada de cuadro principal, sin confundir QF con clasificación. Dos encuentros duplicados (cuatro filas) quedan separados. En la ventana 2022–2024 quedan 27.883 filas C, de las cuales 18.128 son cuadro principal y 9.755 clasificación, antes de filtros de estadísticas. No afirmar que todas tienen contadores válidos.

El constructor del top 500 verifica integridad, excluye duplicados por torneo/ronda/IDs de participantes y agrega métricas básicas por oportunidades, superficie y grupo ATP/Challenger principal/Challenger clasificación. La suma conjunta es descriptiva: no equipara fuerzas de oposición entre niveles. No se descargaron años posteriores al corte ni datos de golpes nuevos. Queda pendiente contraste externo específico de Challenger.


## Búsqueda de golpes Challenger — 07/10/2026

En el snapshot MCP ya descargado se identificaron por etiqueta ` CH`/`Challenger` 122 partidos de 2022–2024 (38/8/76 por año), con 159 nombres. Todos tienen presencia de filas ShotTypes, Rally y NetPoints; esto no certifica contadores. Clasificación por etiqueta candidata, sin cotejo independiente torneo por torneo. Los perfiles existentes ya incluyen estos encuentros, así que no son cobertura nueva. De los candidatos de identidad del ranking, 111 del top 350 y 124 del top 500 aparecen en esos metadatos; solo cinco en cada universo tienen al menos cinco partidos CH. Resultado local: `challenger_charting_search.json`.

Fuentes revisadas: [MCP explica que incluye encuentros Challenger ocasionales](https://www.tennisabstract.com/blog/2017/04/03/3000-matches/). [Live Tennis API documenta que sus perfiles detallados proceden del MCP](https://docs.livetennisapi.com/shot-level-rally-data.html), por lo que no se demuestra cobertura independiente nueva. Su [dataset académico](https://livetennisapi.com/data/academic) incluye puntos pero excluye datos de golpes; no confundir marcador por punto con secuencia de golpes. No se contrataron servicios ni solicitaron credenciales.

[ATP Tennis IQ](https://www.atptour.com/en/news/atp-pif-tennis-iq-2025-announcement) anuncia acceso para jugadores ATP/Challenger y coaches, pero no se confirmó una descarga pública histórica de golpes. [Challenger TV](https://www.atptour.com/en/news/how-to-watch-atp-challenger-tv-schedule-scores) ofrece transmisiones; es una vía candidata para anotación manual de encuentros faltantes, previa comprobación de replays históricos y condiciones de uso. No se descargaron ni procesaron videos. La búsqueda no encontró una base pública nueva con cobertura amplia para 2022–2024; esto no prueba que no exista.
