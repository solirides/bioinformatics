# PGIP CLI

Typer-based command-line interface for interacting with the PGIP backend. The initial commands focus on plugin registry management; future iterations will add ingestion, workflow submission, and cohort operations.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .
```

Alternatively run in editable mode without a venv if you already have one active. The CLI expects the backend API to be reachable at `http://localhost:8000` by default; override with the environment variable `PGIP_BACKEND_URL`.

## Usage

```powershell
pgip plugins list
pgip plugins show frequency-aggregator
pgip plugins register path\to\manifest.json
```

Add `--api-url` to any command to target a different backend. The `register` command validates manifests using the same schema as the FastAPI service and reports rich error messages when fields are missing.

## Roadmap

- `pgip ingest` – Submit dataset ingestion jobs via Nextflow
- `pgip workflows` – Monitor pipeline status and logs
- `pgip cohort` – Manage cohort metadata and summary statistics exports
- Auth integration for multi-user mode
