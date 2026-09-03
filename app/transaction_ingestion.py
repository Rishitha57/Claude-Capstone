from __future__ import annotations

import csv
import io
import json
from typing import Any


def _categorize(description: str) -> str:
    text = (description or "").lower()
    if any(keyword in text for keyword in ["whole foods", "grocery", "market", "farmers", "supermarket", "organic"]):
        return "Groceries"
    if any(keyword in text for keyword in ["netflix", "spotify", "hulu", "youtube", "movie", "cinema", "stream"]):
        return "Entertainment"
    if any(keyword in text for keyword in ["coffee", "starbucks", "cafe", "tea", "bakery", "restaurant", "food"]):
        return "Food & Drink"
    if any(keyword in text for keyword in ["uber", "lyft", "gas", "fuel", "transit", "metro", "train", "bus"]):
        return "Transportation"
    if any(keyword in text for keyword in ["rent", "mortgage", "apartment", "landlord"]):
        return "Housing"
    if any(keyword in text for keyword in ["pharmacy", "clinic", "doctor", "hospital", "insurance"]):
        return "Health"
    return "Other"


def normalize_transaction(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize a raw transaction record into a consistent structure."""
    amount_raw = record.get("amount")
    try:
        amount = float(amount_raw) if amount_raw not in (None, "") else 0.0
    except (TypeError, ValueError):
        amount = 0.0

    description = str(record.get("description") or record.get("merchant") or "Unknown")
    merchant = str(record.get("merchant") or description or "Unknown")
    category = str(record.get("category") or _categorize(description))
    currency = str(record.get("currency") or "USD").upper()
    source = str(record.get("source") or "unknown")

    return {
        "date": record.get("date"),
        "description": description,
        "amount": amount,
        "currency": currency,
        "merchant": merchant,
        "category": category,
        "source": source,
    }


def _parse_csv_rows(text: str, source: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(text))
    return [normalize_transaction({**row, "source": source}) for row in reader]


def _parse_json_rows(text: str, source: str) -> list[dict[str, Any]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return []

    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("transactions", [])
    else:
        records = []

    return [
        normalize_transaction({**record, "source": source})
        for record in records
        if isinstance(record, dict)
    ]


def parse_transactions(text: str, source: str = "csv") -> list[dict[str, Any]]:
    """Parse transaction input from CSV, JSON, or a Plaid-style mock stream."""
    if not text or not text.strip():
        return []

    if source.lower() == "json":
        return _parse_json_rows(text, "json")

    if source.lower() == "csv":
        return _parse_csv_rows(text, "csv")

    if source.lower() == "plaid":
        return _parse_json_rows(text, "plaid")

    raise ValueError(f"Unsupported transaction source: {source}")
