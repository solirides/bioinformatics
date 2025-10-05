"""Compatibility shim exposing backend app package at repository root."""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType
from typing import Iterable, List

from pkgutil import extend_path

# Ensure this package behaves as a namespace package that points to
# the actual backend implementation living under ``backend/app``.
_package_root = Path(__file__).resolve().parent
_backend_path = _package_root.parent / "backend" / "app"

# Start with any existing namespace entries (for compatibility with
# editable installs or other tooling) then append the backend path if missing.
__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]
if str(_backend_path) not in __path__:  # type: ignore[operator]
    __path__.append(str(_backend_path))  # type: ignore[operator]


def __getattr__(name: str) -> ModuleType | object:
    """Lazily proxy top-level attributes to the backend package.

    This mirrors the behaviour of ``backend.app`` so consumers importing from
    ``app`` continue to work whether they execute commands from the backend
    directory or the repository root.
    """

    backend_pkg = importlib.import_module("backend.app")
    try:
        return getattr(backend_pkg, name)
    except AttributeError as exc:  # pragma: no cover - mirrors default behaviour
        raise AttributeError(f"module 'app' has no attribute {name!r}") from exc


def __dir__() -> Iterable[str]:  # pragma: no cover - introspection only
    backend_pkg = importlib.import_module("backend.app")
    names: List[str] = sorted(set(dir(backend_pkg)))
    return names
