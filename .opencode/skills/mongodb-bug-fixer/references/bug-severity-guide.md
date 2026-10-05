# Severity guide

| Severity | Practical criteria and examples |
|---|---|
| low | Small, contained correctness issue without user-visible failure; optional display field missing in test fixtures; minor index inefficiency within latency budget. |
| medium | Limited user-visible correctness/performance degradation with workaround; stale denormalized totals or a bounded group of orphan orders; no demonstrated loss or outage. |
| high | Material production correctness or availability impact; widespread broken references, checkout timeouts, unique constraint absent with confirmed duplicates, recoverable loss affecting workflows. |
| critical | Active major outage, irreversible substantial data loss, or confirmed serious privacy/security exposure; corrupted balances across production or unrestricted sensitive data disclosure. Escalate to owner immediately while remaining read-only. |

Evaluate data correctness, actual/potential loss, availability, privacy/security,
query latency/resource contention, affected count and proportion, environment,
business importance, recurrence and recovery options. A single financial record
can be high severity; millions of optional missing values can be low. Production
impact matters more than fixture count. Separate observed impact from plausible
risk. Explain severity, confidence and unknowns; do not inflate critical solely
because a database is production or a query uses COLLSCAN.
