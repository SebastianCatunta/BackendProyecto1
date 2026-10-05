# Safe manual repair planning

1. Diagnose with least-privilege read-only MCP. Bound queries and redact outputs.
2. Establish business rules, exact scope, BSON types and baseline affected count.
3. Preserve original report before plans. Separate proposal, approval, reported
   execution and independently verified result in an append-only audit history.
4. Prefer normalization, flags, rebuilding derived fields or retaining/quarantining
   invalid records over deletion. A move to quarantine with source deletion still
   requires destructive safeguards. Never invent missing reference targets.
5. Provide a read-only dry run selecting exactly the intended scope. Explain race
   conditions: the user must recheck counts immediately before execution and stop
   on unexpected drift. A dry-run file preview is not a live database preflight.
6. Recommend a consistent scoped backup/export or snapshot and tested restore
   procedure, without exporting secrets through this skill. Note retention and
   access controls. For updates preserve per-record original values for rollback;
   unsetting a field is not rollback if values existed before the repair.
7. Require explicit user approval for target environment, exact operation and
   scope. Destructive plans require explicit manual confirmation, snapshot and
   recovery instructions. Approval never grants this skill permission to execute.
8. Give manual instructions outside MCP with no credentials/URIs. Describe
   preconditions, batch size, checkpoints, retry/idempotency predicates and stop
   conditions. Index/validator changes need metadata preflight and rollback too.
9. For production consider maintenance windows, resource budgets, concurrent
   writers, replication lag, index build overhead and rollback ownership. Avoid
   automatically running even supposedly harmless application startup scripts.
10. Accept scoped user output/DBA confirmation. Record exact filter and operation,
    matched/modified counts, changed indexes, skips, errors and evidence provenance.
    Unexpected counts or partial failures need investigation, not silent success.
11. Verify using fresh MCP reads, original detection and business invariants.
    Reinspect indexes/explain when relevant. Retain failed attempts and limitations.
12. Save completed solution only when all criteria and scoped evidence pass.
    Read-only observation alone cannot prove who performed a correction.
