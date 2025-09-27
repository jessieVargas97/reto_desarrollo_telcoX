# TelcoX - Reto Fullstack (Flask + Angular + MySQL + Docker)

Plataforma mínima de **autogestión** para visualizar **consumo en tiempo (casi) real**, saldo y minutos. Incluye:
- **Backend**: Flask + Flask-RESTX (docs en `/docs`) con MySQL como BSS simulado.
- **Frontend**: Angular + Bootstrap. Consulta cada 10s el API y permite simular consumo.
- **DevOps**: Dockerfiles y `docker-compose.yml` para levantar todo.
- **Tests**: Pruebas básicas de API con `pytest`.

## Levantar mediante docker
```bash
cd reto_desarrollo_vargas
docker compose up --build -d
# Frontend: http://localhost:4200
# API docs: http://localhost:8000/docs para swagger UI
