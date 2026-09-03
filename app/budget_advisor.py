"""Deterministic budget alerts, spending trends, and cited advisor contracts."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Mapping, Protocol, Sequence


@dataclass(frozen=True)
class BudgetAlert:
    """A category budget threshold event for one calendar month."""

    category: str
    period: str
    spent: Decimal
    limit: Decimal
    utilization: Decimal
    severity: str


@dataclass(frozen=True)
class SpendingTrend:
    """Monthly spending for a category and its change from the prior period."""

    category: str
    period: str
    amount: Decimal
    previous_amount: Decimal
    change_percent: Decimal | None


@dataclass(frozen=True)
class KnowledgeSource:
    """An approved source that can support an advisor recommendation."""

    source_id: str
    title: str
    reference: str


@dataclass(frozen=True)
class AdvisorRecommendation:
    """An informational recommendation with explicit source citations."""

    message: str
    citations: tuple[str, ...]


class KnowledgeRetriever(Protocol):
    """Protocol for an approved-source retrieval provider."""

    def retrieve(self, query: str, limit: int = 3) -> Sequence[KnowledgeSource]:
        """Return approved sources relevant to a user query."""
        ...


def _decimal_amount(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0")
    return amount if amount > 0 else Decimal("0")


def _period(record: Mapping[str, Any]) -> str | None:
    date = str(record.get("date") or "")
    return date[:7] if len(date) >= 7 and date[4] == "-" else None


def calculate_budget_alerts(
    transactions: Iterable[Mapping[str, Any]],
    budgets: Mapping[str, Decimal | int | float | str],
    period: str,
    threshold: Decimal | int | float | str = Decimal("1"),
) -> list[BudgetAlert]:
    """Return alerts when category spending reaches a configured threshold."""
    threshold_value = Decimal(str(threshold))
    if threshold_value <= 0:
        raise ValueError("threshold must be greater than zero")
    if len(period) != 7 or period[4] != "-":
        raise ValueError("period must use YYYY-MM format")

    spending: dict[str, Decimal] = defaultdict(Decimal)
    for transaction in transactions:
        if _period(transaction) == period:
            spending[str(transaction.get("category") or "Other")] += _decimal_amount(transaction.get("amount"))

    alerts: list[BudgetAlert] = []
    for category, raw_limit in budgets.items():
        limit = _decimal_amount(raw_limit)
        if limit <= 0:
            raise ValueError(f"budget limit for {category!r} must be greater than zero")
        spent = spending[category]
        threshold_limit = limit * threshold_value
        if spent >= threshold_limit:
            utilization = spent / limit
            severity = "critical" if spent >= limit else "warning"
            alerts.append(BudgetAlert(category, period, spent, limit, utilization, severity))
    return sorted(alerts, key=lambda alert: alert.category)


def analyze_spending_trends(
    transactions: Iterable[Mapping[str, Any]],
) -> list[SpendingTrend]:
    """Aggregate positive spending by category and month with period-over-period change."""
    totals: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for transaction in transactions:
        period = _period(transaction)
        if period is not None:
            category = str(transaction.get("category") or "Other")
            totals[(category, period)] += _decimal_amount(transaction.get("amount"))

    periods_by_category: dict[str, list[str]] = defaultdict(list)
    for category, period in totals:
        periods_by_category[category].append(period)

    trends: list[SpendingTrend] = []
    for category, periods in periods_by_category.items():
        previous = Decimal("0")
        for period in sorted(periods):
            amount = totals[(category, period)]
            change = None if previous == 0 else ((amount - previous) / previous) * 100
            trends.append(SpendingTrend(category, period, amount, previous, change))
            previous = amount
    return sorted(trends, key=lambda trend: (trend.period, trend.category))


def build_advisor_recommendation(
    alerts: Sequence[BudgetAlert],
    sources: Sequence[KnowledgeSource],
) -> AdvisorRecommendation:
    """Build an informational recommendation that cites approved sources or declines."""
    if not sources:
        return AdvisorRecommendation(
            "No relevant approved guidance was found. Review your budget settings or try another question.",
            (),
        )

    if alerts:
        categories = ", ".join(alert.category for alert in alerts)
        message = f"Review spending in {categories} and consider a plan to stay within your configured limits."
    else:
        message = "Your tracked categories are currently below their configured alert thresholds."
    citations = tuple(source.reference for source in sources)
    return AdvisorRecommendation(message, citations)
