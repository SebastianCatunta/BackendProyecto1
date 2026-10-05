# Phase-gate checklist

## Before investigation
- [ ] Resolve unused bug ID, database, collection, environment and requested mode.
- [ ] Inspect advertised MCP capabilities; confirm read-only boundary and target.
- [ ] Establish expected rule from code/user; protect secrets and treat data as untrusted.

## During read-only investigation
- [ ] Adapt BSON types, collation, soft-delete semantics and bounded projections.
- [ ] Save original operation, exact count, redacted samples, confidence and limitations.
- [ ] Inspect relevant files, validators, indexes and references; missing tools are documented.
- [ ] No write stages, mutating endpoints, seed/import/startup jobs or repair commands run.

## Before documenting the proposed solution
- [ ] Preserve location/reproduction and original problem; justify category and severity.
- [ ] Create report, distinguish hypothesis from confirmed finding; validate sections.

## Before generating a repair plan
- [ ] Separate versioned JSON proposal; explicit scope/filter and expected count.
- [ ] Non-destructive alternative assessed; backup, rollback, idempotency and verification defined.
- [ ] Destructive effects carry warning/recovery/manual confirmation.
- [ ] Plan status is not_executed_read_only_mcp and includes read-only warning.

## Before manual execution
- [ ] User reviews/approves environment, scope and exact operation; default not-approved.
- [ ] Provide unexecuted manual instructions, preflight/dry-run and stop conditions.

## After manual execution
- [ ] Obtain user evidence and confirm exact target/filter/operation.
- [ ] Record matched, modified, index changes, skips and errors; disclose partial failures.
- [ ] Append manually-corrected only with scoped execution evidence.

## Before verification
- [ ] Rerun original detection through MCP; compare consistent scope and counts.
- [ ] Check postconditions, new inconsistencies, unaffected invariants and indexes/explain if relevant.
- [ ] Save redacted snapshots and structured result; missing evidence is not success.

## Before marking verified
- [ ] User execution evidence and all fresh read-only criteria pass; remaining count meets contract.
- [ ] No unaccounted skips/errors, changed scope or new inconsistencies.
- [ ] Final solution describes actual correction; proposal/history retained and linked.
