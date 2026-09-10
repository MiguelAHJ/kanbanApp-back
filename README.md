# issue-flow

App para llevar reuniones → minuta → issues (GitLab) → tablero → reportes,
con captura por audio en reunión, fotos de notas a mano, y un flujo aparte
para issues rápidos sin reunión formal.

Ver `SETUP.md` para la bitácora de instalación paso a paso (útil para
replicar el entorno en otra máquina).

## Estructura

- `python-service/` — servicio local (FastAPI) que hace transcripción de
  audio, lectura de fotos de notas y armado de minuta con IA. Corre en
  `localhost`; la app de escritorio (Flutter, aún no iniciada) le habla por
  HTTP.
- `docker-compose.yml` — Postgres local, pensado para apuntar más adelante al
  servidor de la empresa solo cambiando la configuración de conexión.

## Estado actual

En desarrollo — por ahora solo existe el servicio de Python (el "corazón" de
la app: transcripción, lectura de fotos, minuta). La app de escritorio en
Flutter y la integración con GitLab vienen después.
