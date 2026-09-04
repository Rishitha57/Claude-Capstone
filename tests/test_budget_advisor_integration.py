from app.budget_advisor import (
    KnowledgeSource,
    build_advisor_recommendation,
    calculate_budget_alerts,
    analyze_spending_trends,
)
from app.transaction_ingestion import parse_transactions


def test_ingestion_to_budget_alert_and_advisor_flow():
    csv_text = "date,description,amount\n2026-02-01,Restaurant,120\n2026-02-15,Restaurant,80\n"
    transactions = parse_transactions(csv_text, source="csv")

    alerts = calculate_budget_alerts(transactions, {"Food & Drink": 150}, "2026-02")
    trends = analyze_spending_trends(transactions)
    recommendation = build_advisor_recommendation(
        alerts,
        [KnowledgeSource("guide-1", "Budget guide", "https://example.test/guide")],
    )

    assert len(alerts) == 1
    assert alerts[0].category == "Food & Drink"
    assert alerts[0].spent == 200
    assert trends[0].amount == 200
    assert recommendation.citations == ("https://example.test/guide",)
    assert "Food & Drink" in recommendation.message
