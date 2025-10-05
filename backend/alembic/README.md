# PGIP Alembic Migrations

This directory contains the Alembic configuration for managing database schema changes. Run commands from `backend/`:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

The default database URL is sourced from `PGIP_DATABASE_URL`. During development you can point Alembic at PostgreSQL by exporting:

```bash
set PGIP_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pgip
```

> Alembic operates synchronously under the hood; when using async URLs Alembic wraps them automatically via `async_engine_from_config` in `alembic/env.py`.
