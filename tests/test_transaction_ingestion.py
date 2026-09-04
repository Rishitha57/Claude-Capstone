import json
from pathlib import Path

from app.transaction_ingestion import parse_transactions, normalize_transaction


def test_parse_transactions_from_csv():
    csv_text = """date,description,amount,currency
2024-01-05,Whole Foods,42.35,USD
2024-01-07,Netflix,15.99,USD
"""

    rows = parse_transactions(csv_text, source="csv")

    assert rows == [
        {
            "date": "2024-01-05",
            "description": "Whole Foods",
            "amount": 42.35,
            "currency": "USD",
            "merchant": "Whole Foods",
            "category": "Groceries",
            "source": "csv",
        },
        {
            "date": "2024-01-07",
            "description": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "merchant": "Netflix",
            "category": "Entertainment",
            "source": "csv",
        },
    ]


def test_normalize_transaction_handles_missing_optional_fields():
    tx = {
        "date": "2024-02-01",
        "description": "Starbucks",
        "amount": "9.50",
        "currency": "USD",
    }

    normalized = normalize_transaction(tx)

    assert normalized["amount"] == 9.5
    assert normalized["merchant"] == "Starbucks"
    assert normalized["category"] == "Food & Drink"
    assert normalized["source"] == "unknown"


def test_parse_transactions_skips_invalid_json_records_and_defaults_bad_amount():
    json_text = json.dumps(
        {
            "transactions": [
                {"description": "Unknown charge", "amount": "not-a-number"},
                "not a transaction",
            ]
        }
    )

    rows = parse_transactions(json_text, source="json")

    assert rows == [
        {
            "date": None,
            "description": "Unknown charge",
            "amount": 0.0,
            "currency": "USD",
            "merchant": "Unknown charge",
            "category": "Other",
            "source": "json",
        }
    ]


def test_parse_transactions_returns_empty_list_for_invalid_json():
    assert parse_transactions("{invalid", source="json") == []
