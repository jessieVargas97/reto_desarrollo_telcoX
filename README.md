# TelcoX - Reto Fullstack (Flask + Angular + MySQL + Docker)
**Descripción**

Este proyecto busca implementar un módulo de visualización de consumo en tiempo real para usuarios de telecomunicaciones.
La idea central es simular un sistema BSS (Business Support System) con:

- **Backend (Flask + Flask-RESTX + SQLAlchemy + MySQL):** expone endpoints REST para consultar y actualizar el consumo (saldo, datos y minutos).

- **Frontend (Angular + Bootstrap + Nginx):** permite visualizar la información del cliente y su consumo.

- **DevOps (Docker Compose):** orquesta los servicios para levantar todo el stack con un solo comando.

Este reto fue desarrollado como ejercicio técnico y tiene implementaciones completas en algunos módulos, mientras que otros quedaron en desarrollo.

## Estado actual
### Backend
- Implementado en Flask con Flask-RESTX para exponer documentación en Swagger (/docs).
- Base de datos simulada con MySQL/SQLite y modelos Customer y Consumption.

#### Endpoints clave:

- /api/consumption → consultar consumo por cliente.
- /api/consumption/simulate → simular consumo y actualizar campos (saldo, datos, minutos) filtrando por msisdn.
- Soporta actualizaciones parciales de consumo vía JSON.

### Frontend
- Implementado en Angular 17 (parcial).
- Configuración básica para conectarse al backend.
- Se configuró proxy (proxy.conf.json) para redirigir peticiones al backend.
- Dockerfile multistage que compila Angular y sirve el resultado con Nginx.

### DevOps
docker-compose.yml orquesta:
- Backend -> api
- Frontend -> web
- Base de datos -> db


## Pendientes / Limitaciones

- La interfaz de Angular solo estructura inicial.
- Se puede pulir validaciones y pruebas adicionales para futuros requerimientos de los endpoints.
- Faltan pruebas de integración más completas en el backend.
- Mejorar frontend con UI intuitiva final.

# Cómo ejecutar
1. Clonar el repositorio
```bash
git clone <repo_url>
cd reto_desarrollo_vargas
```
2. Levantar con Docker
`docker compose up --build`
3. Accesos
- Backend API + Swagger → http://localhost:8000/docs
- Frontend Angular (Nginx) → http://localhost:4200

## BD

+-------------------+         +---------------------+
|    customers      |         |    consumption      |
+-------------------+         +---------------------+
| id (PK)           |◄───┐   | id (PK)             |
| msisdn (UNIQUE)   |    └───| msisdn (FK)         |
| name              |        | balance (FLOAT)     |
+-------------------+        | data_mb (FLOAT)     |
                             | minutes (INT)       |
                             | updated_at (DATETIME)|
                             +---------------------+

