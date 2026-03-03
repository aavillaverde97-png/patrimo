
# Patrimo Maintenance Management Module

This repository contains a complete backend implementation for managing properties,
components, maintenance history and inspections. It is built with FastAPI,
SQLAlchemy and PostgreSQL, and includes financial impact and Excel import
capabilities.

## Features

- CRUD API for properties, components, maintenance and inspections
- SQLAlchemy models with relationships and indexes
- Maintenance scheduling utilities and alert levels
- Financial impact calculations and risk scoring
- Excel import endpoints and services
- Dashboard summary endpoint
- CORS and global exception handling
- Docker support with PostgreSQL container

## Requirements

- Python 3.11+
- PostgreSQL (12+)
- Docker & docker-compose (optional but recommended)

## Environment Variables
Create a `.env` file in the project root (a template has been provided):

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

When using Docker, the compose file sets defaults (`postgres:postgres@db:5432/patrimo`).

## Running Locally Without Docker

```bash
cd patrimo_maintenance_module
python -m venv venv
source venv/bin/activate     # on Windows use venv\Scripts\activate
pip install -r requirements.txt
# make sure DATABASE_URL is configured and the target database exists
uvicorn backend.app:app --reload
```

## Running with Docker

```bash
# build and start services
docker-compose up --build
```

The FastAPI server will be available at [http://localhost:8000](http://localhost:8000)
and PostgreSQL at port `5432`.

Tables are created automatically on application startup.

## API Endpoints Examples

```bash
# health check
curl http://localhost:8000/health

# create property
curl -X POST http://localhost:8000/properties -H "Content-Type: application/json" \
    -d '{"type":"Residential","address":"123 Main St"}'

# list components
curl http://localhost:8000/components

# import excel file
curl -X POST http://localhost:8000/import/excel -F "file=@data.xlsx"

# dashboard
curl http://localhost:8000/dashboard/summary

# upcoming maintenance in next 30 days
curl http://localhost:8000/maintenance/upcoming/30
```

## Project Structure

```
backend/
    app.py                   # FastAPI application entrypoint
    database/
        base.py             # engine, session and init logic
        schema.sql          # initial SQL schema (optional)
    models/
        models.py           # SQLAlchemy ORM definitions
    services/
        maintenance_service.py
        financial_impact_service.py
        excel_service.py
    api/
        schemas.py         # Pydantic schemas
        routers/           # individual route modules
            properties.py
            components.py
            maintenance.py
            inspections.py
            import_router.py
            dashboard_router.py
```

## Notes

- Code is modular and ready for production extension; add authentication,
  pagination, etc., as needed.
- SQLAlchemy sessions are managed via a FastAPI dependency (`get_db`).
- Excel import expects sheets named exactly `properties`, `components`,
  and `maintenance_history`.

## License

MIT
