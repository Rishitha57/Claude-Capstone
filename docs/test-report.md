# Test Report

**Verification date:** 2026-09-03

**Result:** PASS

## Environment

Python 3.13.7

## Unit Tests

| Test | Result |
|--------|--------|
| test_transaction_ingestion | PASS |
| test_budget_advisor | PASS |
| test_confluence_publisher | PASS |

## Integration Tests

| Test | Result |
|--------|--------|
| test_budget_advisor_integration | PASS |
| test_transaction_ingestion_integration | PASS |
| test_e2e_publish_confluence | PASS |

## Edge Cases

- Empty CSV
- Missing fields
- Invalid category
- Empty knowledge source
- Confluence API failure

All listed tests passed. The complete suite contains 21 tests.

## Execution

```text
python scripts/verify_workflow.py
21 passed in 0.80s
Core coverage: app/budget_advisor.py 97% (90 statements, 3 missed)
pip-audit: No known vulnerabilities found
Confluence dry run: 7 artifact pages listed successfully
```

The 90% core financial calculation coverage gate passed. Live Confluence
publication was not attempted because it requires opt-in credentials.
