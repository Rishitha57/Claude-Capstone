import json

from app.transaction_ingestion import parse_transactions


def test_supported_sources_produce_the_same_normalized_contract():
    csv_input = "date,description,amount\n2026-01-05,Metro,3.50\n"
    json_input = json.dumps([{"date": "2026-01-05", "description": "Metro", "amount": 3.5}])
    plaid_input = json.dumps({"transactions": [{"date": "2026-01-05", "description": "Metro", "amount": 3.5}]})

    csv_rows = parse_transactions(csv_input, source="csv")
    json_rows = parse_transactions(json_input, source="json")
    plaid_rows = parse_transactions(plaid_input, source="plaid")

    assert [row | {"source": "normalized"} for row in csv_rows] == [
        row | {"source": "normalized"} for row in json_rows
    ] == [
        row | {"source": "normalized"} for row in plaid_rows
    ]
    assert {row["source"] for row in csv_rows + json_rows + plaid_rows} == {"csv", "json", "plaid"}
