"""Publish AI-Expense-Advisor SDLC documents to Confluence Cloud."""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ConfluenceConfigurationError(ValueError):
    """Raised when required Confluence configuration is missing."""


class ConfluencePublishError(RuntimeError):
    """Raised when Confluence rejects a publish request."""


def _load_dotenv() -> None:
    """Load simple KEY=VALUE entries from the project .env without overriding the process environment."""
    dotenv_path = Path(__file__).parents[1] / ".env"
    if not dotenv_path.is_file():
        return

    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#") or "=" not in entry:
            continue
        name, value = entry.split("=", 1)
        name = name.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(name, value)


@dataclass(frozen=True)
class ConfluenceConfig:
    """Connection settings for a Confluence Cloud site."""

    base_url: str
    space_key: str
    email: str
    api_token: str
    parent_page_id: str | None = None

    @classmethod
    def from_environment(cls) -> "ConfluenceConfig":
        """Build configuration from CONFLUENCE_* environment variables."""
        _load_dotenv()
        values = {
            "base_url": os.getenv("CONFLUENCE_BASE_URL", "").rstrip("/"),
            "space_key": os.getenv("CONFLUENCE_SPACE_KEY", ""),
            "email": os.getenv("CONFLUENCE_EMAIL", ""),
            "api_token": os.getenv("CONFLUENCE_API_TOKEN", ""),
            "parent_page_id": os.getenv("CONFLUENCE_PARENT_PAGE_ID") or None,
        }
        missing = [name for name in ("base_url", "space_key", "email", "api_token") if not values[name]]
        if missing:
            raise ConfluenceConfigurationError(
                "Missing Confluence configuration: " + ", ".join(missing)
            )
        return cls(**values)


class ConfluenceClient:
    """Small Confluence Server REST API client for document publishing."""

    def __init__(self, config: ConfluenceConfig) -> None:
        self.config = config
        self._api_root = f"{config.base_url}/wiki/rest/api"

    def publish_page(
        self,
        title: str,
        html: str,
        parent_page_id: str | None = None,
    ) -> dict[str, Any]:
        """Create or update a page identified by title in the configured space."""
        if not title.strip():
            raise ValueError("Confluence page title cannot be empty")

        existing = self._find_page(title)
        if existing is None:
            payload: dict[str, Any] = {
                "type": "page",
                "title": title,
                "space": {"key": self.config.space_key},
                "body": {"storage": {"value": html, "representation": "storage"}},
            }
            parent_id = parent_page_id or self.config.parent_page_id
            if parent_id:
                payload["ancestors"] = [{"id": parent_id}]
            return self._request("POST", "/content", payload)

        page_id = str(existing["id"])
        version = int(existing["version"]["number"]) + 1
        payload = {
            "version": {"number": version},
            "title": title,
            "type": "page",
            "body": {"storage": {"value": html, "representation": "storage"}},
        }
        return self._request("PUT", f"/content/{page_id}", payload)

    def _find_page(self, title: str) -> dict[str, Any] | None:
        query = urlencode({"spaceKey": self.config.space_key, "title": title, "expand": "version"})
        response = self._request("GET", f"/content?{query}")
        results = response.get("results", [])
        return results[0] if results else None

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        token = base64.b64encode(f"{self.config.email}:{self.config.api_token}".encode()).decode()
        data = json.dumps(payload).encode() if payload is not None else None
        request = Request(
            f"{self._api_root}{path}",
            data=data,
            headers={
                "Authorization": f"Basic {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode())
        except HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise ConfluencePublishError(
                f"Confluence request failed with HTTP {error.code}: {detail[:500]}"
            ) from error


def publish_file(path: str, title: str, config: ConfluenceConfig | None = None) -> dict[str, Any]:
    """Publish an HTML file to Confluence and return the API response."""
    with open(path, encoding="utf-8") as document:
        html = document.read()
    return ConfluenceClient(config or ConfluenceConfig.from_environment()).publish_page(title, html)
