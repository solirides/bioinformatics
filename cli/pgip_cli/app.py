"""PGIP Typer application."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import httpx
import typer
from pydantic import BaseModel, ValidationError
from rich.console import Console
from rich.table import Table

DEFAULT_API_URL = "http://localhost:8000"
console = Console()


class PluginSummary(BaseModel):
    name: str
    version: str
    description: str
    tags: list[str] = []
    latest_run_at: Optional[str] = None


class PluginManifest(BaseModel):
    name: str
    version: str
    description: str
    authors: list[str]
    entrypoint: str
    created_at: str
    updated_at: str
    inputs: list[dict]
    outputs: list[dict]
    tags: list[str] = []
    provenance: dict
    resources: Optional[dict] = None


def _client(base_url: str) -> httpx.Client:
    return httpx.Client(base_url=base_url, timeout=10.0)


def _get_base_url(api_url: Optional[str]) -> str:
    return api_url or os.getenv("PGIP_BACKEND_URL", DEFAULT_API_URL)


app = typer.Typer(help="Interact with the PanGenome Insight Platform backend.")
plugins_app = typer.Typer(help="Manage annotation plugins.")
app.add_typer(plugins_app, name="plugins")


@plugins_app.command("list")
def list_plugins(api_url: Optional[str] = typer.Option(None, help="Override backend API URL")) -> None:
    """List available plugins."""

    base_url = _get_base_url(api_url)
    with _client(base_url) as client:
        response = client.get("/api/v1/plugins/")
    if response.status_code != 200:
        console.print(f"[red]Error:[/] {response.text}")
        raise typer.Exit(code=1)

    try:
        payload = [PluginSummary.model_validate(item) for item in response.json()]
    except ValidationError as exc:
        console.print(f"[red]Failed to parse response:[/] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="PGIP Plugins")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Description")
    table.add_column("Tags", style="green")

    for plugin in payload:
        tags = ", ".join(plugin.tags) if plugin.tags else "-"
        table.add_row(plugin.name, plugin.version, plugin.description, tags)

    console.print(table)


@plugins_app.command("show")
def show_plugin(
    name: str = typer.Argument(..., help="Plugin name"),
    version: Optional[str] = typer.Option(None, help="Optional plugin version"),
    api_url: Optional[str] = typer.Option(None, help="Override backend API URL"),
    output: Optional[Path] = typer.Option(None, help="Write manifest JSON to file"),
) -> None:
    """Show manifest details for a plugin."""

    base_url = _get_base_url(api_url)
    params = {"version": version} if version else None

    with _client(base_url) as client:
        response = client.get(f"/api/v1/plugins/{name}", params=params)

    if response.status_code != 200:
        console.print(f"[red]Error:[/] {response.text}")
        raise typer.Exit(code=1)

    try:
        manifest = PluginManifest.model_validate(response.json())
    except ValidationError as exc:
        console.print(f"[red]Failed to parse manifest:[/] {exc}")
        raise typer.Exit(code=1) from exc

    if output:
        output.write_text(json.dumps(manifest.model_dump(mode="json"), indent=2))
        console.print(f"Manifest written to {output}")
        return

    console.print_json(data=manifest.model_dump(mode="json"))


@plugins_app.command("register")
def register_plugin(
    manifest_path: Path = typer.Argument(..., exists=True, readable=True, help="Path to manifest JSON"),
    api_url: Optional[str] = typer.Option(None, help="Override backend API URL"),
) -> None:
    """Register or update a plugin manifest from a JSON file."""

    base_url = _get_base_url(api_url)

    try:
        manifest_data = json.loads(manifest_path.read_text())
        manifest = PluginManifest.model_validate(manifest_data)
    except (json.JSONDecodeError, ValidationError) as exc:
        console.print(f"[red]Invalid manifest:[/] {exc}")
        raise typer.Exit(code=1) from exc

    with _client(base_url) as client:
        response = client.post("/api/v1/plugins/", json=manifest.model_dump(mode="json"))

    if response.status_code not in (200, 201):
        console.print(f"[red]Error:[/] {response.text}")
        raise typer.Exit(code=1)

    console.print(f"[green]Registered plugin {manifest.name} v{manifest.version}[/]")
