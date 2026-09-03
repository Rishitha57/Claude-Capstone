# Implementation Plan

Tasks are dependency-ordered. No production implementation should proceed past the foundation stage until the design-review gates are accepted by the human reviewer.

1. **Confirm domain contracts and schema versions.** Define transaction, budget, knowledge-document, alert, user, and audit-event schemas. **Status:** pending. **Blocks:** 2-8.
2. **Confirm security and privacy controls.** Define authentication, per-user authorization, consent, retention, deletion, encryption, input limits, and redaction rules. **Status:** pending. **Blocks:** 3-8.
3. **Define provider and repository interfaces.** Specify storage, embedding, language-model, and Confluence adapter contracts, including timeout, retry, pagination, and structured-error behavior. **Status:** pending. **Blocks:** 4-8.
4. **Implement transaction ingestion.** Normalize CSV, JSON, and Plaid-style inputs; safely handle malformed records and invalid amounts. Storage, fingerprints, and bounded batches remain pending the approved repository contract. **Status:** in progress. **Depends on:** 1-3.
5. **Test ingestion behavior.** Cover empty input, missing fields, malformed records, source preservation, and cross-format normalized contracts. Duplicate imports, size limits, and provider failures remain pending their respective interfaces. **Status:** in progress. **Depends on:** 4.
6. **Implement deterministic budget alerts.** Aggregate category spending by period and emit warning/critical alerts at configured thresholds without using an LLM for arithmetic. **Status:** in progress. **Depends on:** 1-3.
7. **Implement approved-source retrieval and advisor responses.** Define the citation-required advisor contract and no-result behavior. Provider retrieval, consent checks, quotas, caching, and token-cost metrics remain pending. **Status:** in progress. **Depends on:** 1-3 and 6.
8. **Add operational safeguards.** Add correlation IDs, structured logs, health checks, metrics, rate-limit handling, dependency scanning, and secret scanning. **Status:** pending. **Depends on:** 2-7.
9. **Run verification and review.** Execute unit/integration tests, confirm at least 90% coverage for core financial calculations, run the secret check, and complete the Lens review checklist. **Status:** pending. **Depends on:** 4-8.
10. **Publish SDLC artifacts to Confluence.** Publish approved HTML requirements, technical design, and workflow report pages using the optional idempotent publisher. **Status:** framework ready. **Depends on:** 9 and configured Confluence credentials.

## Blocked Work

Transaction storage, budget alerts, and RAG implementation are blocked until schemas, authorization boundaries, consent and retention rules, provider contracts, and cost budgets are approved. Confluence synchronization is blocked only by missing credentials or an unavailable Confluence tenant; local development does not require it.
