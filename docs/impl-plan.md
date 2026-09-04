# Implementation Plan

Tasks are dependency-ordered. No production implementation should proceed past the foundation stage until the design-review gates are accepted by the human reviewer.

1. **Confirm domain contracts and schema versions.** Define transaction, budget, knowledge-document, alert, user, and audit-event schemas. **Status:** closed for local capstone scope.
2. **Confirm security and privacy controls.** Define authentication, per-user authorization, consent, retention, deletion, encryption, input limits, and redaction rules. **Status:** production follow-up explicitly accepted; local credentials remain environment-based.
3. **Define provider and repository interfaces.** Specify storage, embedding, language-model, and Confluence adapter contracts. **Status:** local contracts closed; production adapters remain follow-up work.
4. **Implement transaction ingestion.** Normalize CSV, JSON, and Plaid-style inputs; safely handle malformed records and invalid amounts. **Status:** complete for local capstone scope.
5. **Test ingestion behavior.** Cover empty input, missing fields, malformed records, source preservation, and cross-format normalized contracts. **Status:** complete.
6. **Implement deterministic budget alerts.** Aggregate category spending by period and emit warning/critical alerts at configured thresholds without using an LLM for arithmetic. **Status:** complete.
7. **Implement approved-source retrieval and advisor responses.** Define the citation-required advisor contract and no-result behavior. **Status:** complete locally; external provider integration is excluded.
8. **Add operational safeguards.** Add dependency and secret scanning plus local verification. Production telemetry and deployment controls remain follow-up work. **Status:** complete for local capstone scope.
9. **Run verification and review.** Execute unit/integration tests, confirm at least 90% coverage for core financial calculations, run the secret check, and complete review. **Status:** complete.
10. **Publish SDLC artifacts to Confluence.** Publish approved artifacts using the optional idempotent publisher. **Status:** dry-run verified; live publication remains optional.

## Blocked Work

Production transaction storage, authorization, consent, retention, provider contracts, and cost budgets remain follow-up work. The local capstone path is unblocked and verified without Confluence credentials; live synchronization is optional.
