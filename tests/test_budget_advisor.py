from decimal import Decimal

import pytest

from app.budget_advisor import (
    KnowledgeSource,
    BudgetAlert,
    build_advisor_recommendation,
    calculate_budget_alerts,
    analyze_spending_trends,
)


TRANSACTIONS = [
    {"date": "2026-01-05", "category": "Food & Drink", "amount": "60.00"},
    {"date": "2026-01-20", "category": "Food & Drink", "amount": "40.00"},
    {"date": "2026-02-05", "category": "Food & Drink", "amount": "150.00"},
    {"date": "2026-02-07", "category": "Transport", "amount": "25.00"},
]


def test_calculate_budget_alerts_generates_warning_and_critical_alerts():
    alerts = calculate_budget_alerts(
        TRANSACTIONS,
        {"Food & Drink": "100", "Transport": "100"},
        "2026-02",
        threshold="0.8",
    )

    assert alerts == [
        BudgetAlert(
            "Food & Drink", "2026-02", Decimal("150.00"), Decimal("100"), Decimal("1.5"), "critical"
        )
    ]


def test_calculate_budget_alerts_rejects_invalid_configuration():
    with pytest.raises(ValueError, match="YYYY-MM"):
        calculate_budget_alerts([], {"Food": 100}, "2026")

    with pytest.raises(ValueError, match="greater than zero"):
        calculate_budget_alerts([], {"Food": 0}, "2026-02")


def test_analyze_spending_trends_reports_period_change():
    trends = analyze_spending_trends(TRANSACTIONS)

    food_trends = [trend for trend in trends if trend.category == "Food & Drink"]
    assert food_trends[0].amount == Decimal("100.00")
    assert food_trends[1].amount == Decimal("150.00")
    assert food_trends[1].previous_amount == Decimal("100.00")
    assert food_trends[1].change_percent == Decimal("50.0")


def test_build_advisor_recommendation_requires_citations():
    no_sources = build_advisor_recommendation([], [])
    assert no_sources.citations == ()
    assert "No relevant approved guidance" in no_sources.message

    sources = [KnowledgeSource("budget-1", "Budgeting guide", "https://example.test/budgeting")]
    recommendation = build_advisor_recommendation([], sources)
    assert recommendation.citations == ("https://example.test/budgeting",)
    assert "below" in recommendation.message
