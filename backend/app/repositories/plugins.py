"""Data access helpers for plugins."""

from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Plugin
from app.models.plugin import PluginManifest


async def list_plugins(session: AsyncSession) -> list[Plugin]:
    """Return plugins ordered by most recent update."""

    stmt: Select[tuple[Plugin]] = select(Plugin).order_by(Plugin.updated_at.desc())
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_plugin(
    session: AsyncSession, *, name: str, version: Optional[str] = None
) -> Optional[Plugin]:
    """Fetch a plugin by name and optional version."""

    stmt: Select[tuple[Plugin]] = select(Plugin).where(Plugin.name == name)
    if version:
        stmt = stmt.where(Plugin.version == version)
    else:
        stmt = stmt.order_by(Plugin.updated_at.desc()).limit(1)

    result = await session.execute(stmt)
    return result.scalars().first()


async def upsert_plugin(session: AsyncSession, manifest: PluginManifest) -> Plugin:
    """Insert or update a plugin manifest."""

    plugin = await get_plugin(session, name=manifest.name, version=manifest.version)

    manifest_payload = manifest.model_dump(mode="json")

    if plugin:
        plugin.description = manifest.description
        plugin.entrypoint = manifest.entrypoint
        plugin.authors = manifest.authors
        plugin.tags = manifest.tags
        plugin.manifest = manifest_payload
        plugin.created_at = manifest.created_at
        plugin.updated_at = manifest.updated_at
        plugin.latest_run_at = manifest.updated_at
    else:
        plugin = Plugin(
            name=manifest.name,
            version=manifest.version,
            description=manifest.description,
            entrypoint=manifest.entrypoint,
            authors=list(manifest.authors),
            tags=list(manifest.tags),
            manifest=manifest_payload,
            created_at=manifest.created_at,
            updated_at=manifest.updated_at,
            latest_run_at=manifest.updated_at,
        )
        session.add(plugin)

    await session.commit()
    await session.refresh(plugin)
    return plugin


async def delete_plugin(session: AsyncSession, *, name: str, version: str) -> bool:
    """Delete a plugin by name/version pair."""

    plugin = await get_plugin(session, name=name, version=version)
    if plugin is None:
        return False

    await session.delete(plugin)
    await session.commit()
    return True
