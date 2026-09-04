# Design Review

**Review scope:** `docs/architecture.md` before production coding begins.

**Decision:** Conditionally approved. The component boundaries are appropriate for the capstone, but implementation must satisfy the decisions and gates below before the system is called production-ready.

## Review Findings

| Area | Finding | Required control before implementation is complete |
| --- | --- | --- |
| Scalability | The design has no persistence, job boundary, retry policy, or concurrency strategy. A synchronous ingestion and RAG request path will not scale with larger imports or slow providers. | Persist normalized transactions behind a repository interface; make imports idempotent; process large imports asynchronously or in bounded batches; add provider timeouts, retries with backoff, rate-limit handling, and pagination. |
| Security | The architecture does not define authentication, authorization, tenant isolation, input limits, or audit events. Confluence page titles and base URLs are also external inputs. | Enforce authenticated access and per-user data isolation; validate file size, row count, fields, and URLs; use least-privilege integration credentials; redact sensitive values from logs; add dependency and secret scanning. |
| Cost | Embeddings, retrieval, and language-model calls have no budget, quota, or model-selection policy. | Set per-user and per-workflow quotas; use deterministic budget calculations without an LLM; chunk and deduplicate knowledge documents; cache stable retrieval results; record token and provider spend metrics. |
| Data Privacy | Transactions are financial data, but retention, deletion, consent, and provider processing boundaries are not defined. | Minimize stored fields; encrypt data in transit and at rest; define retention and deletion workflows; require explicit consent before external model calls; keep approved-source citations separate from private transaction data. |
| Maintainability | Contracts between components, versioning, observability, and failure semantics are unspecified. | Define typed interfaces and schema versions; use structured errors; add correlation IDs, health checks, metrics, and structured logs; keep provider adapters behind interfaces and document architecture decisions. |

## Decisions

- Keep budget arithmetic deterministic and independently testable; the advisor may summarize results but must not calculate authoritative totals.
- Use repository and provider interfaces so storage, embeddings, LLMs, and Confluence can be replaced without changing domain logic.
- Make ingestion idempotent using a stable transaction fingerprint composed from source, account, date, amount, and merchant fields where available.
- Use bounded batch sizes and explicit timeouts for imports and external calls. No external provider call may block indefinitely.
- Use a per-user authorization boundary for every transaction, budget, retrieval, and report operation.
- Use a small Python standard-library Confluence client to avoid adding a runtime dependency for publishing.
- Use Confluence storage-format HTML for reports and templates.
- Make publishing idempotent by looking up pages by space and title, then creating or updating them.
- Keep Confluence credentials in environment variables and exclude `.env` from Git.

## Pre-coding gates

1. Document transaction, budget, knowledge-document, and alert schemas with versioning rules.
2. Define authentication, authorization, consent, retention, deletion, and audit requirements.
3. Add tests for idempotent ingestion, provider timeout/failure, missing retrieval results, and tenant isolation.
4. Define model, token, storage, and Confluence rate-limit budgets with observable counters.
5. Require explicit titles and configured space keys when publishing; never place tokens in URLs, payloads, logs, or documentation.

## Residual risks

- Confluence Cloud availability and API rate limits remain an external dependency.
- Categorization quality may be imperfect and requires user correction or review flows.
- RAG output must remain informational and cite approved sources; it must not be presented as regulated financial advice.

## Scope Closure for This Capstone

The pre-coding gates above are closed for the local, deterministic capstone
demonstration as follows: the application uses in-process data, approved-source
contracts, environment-based Confluence credentials, bounded test fixtures,
and explicit offline verification. Authentication, tenant isolation, durable
storage, retention, deletion, provider quotas, and deployment observability
are accepted exclusions from this educational release. They remain mandatory
before production use and are tracked as follow-up work rather than silently
treated as implemented.
