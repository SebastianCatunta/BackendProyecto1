# Bug: Fictional orphan orders excluded from fulfillment

## Bug ID
BUG-001

## Status
verified

## Environment
testing

## Severity
medium

## Category
orphan-reference

## Database
ecommerce

## Collection
orders

## Relevant fields
- userId
- status

## Related collections
- users

## 1. Bug location and reproduction
### Location
Fictional ecommerce testing dataset: orders.userId references users._id.
Illustrative application files: src/orders/order.schema.ts and orders.service.ts;
illustrative endpoint GET /orders. These are scenario locations, not this project's files.

### Reproduction steps
1. Confirm testing/ecommerce target and inspect userId BSON types and users indexes.
2. Run the detection aggregation and a separate bounded sample query through read-only MCP.
3. Compare against the rule: every non-quarantined order must reference an existing user.

### Detection query or aggregation
```javascript
db.orders.aggregate([
  {$match: {userId: {$type: 'objectId'}, status: {$ne: 'quarantined'}}},
  {$lookup: {from: 'users', localField: 'userId', foreignField: '_id', as: 'parent'}},
  {$match: {parent: {$size: 0}}},
  {$count: 'affected_count'}
])
```

### Expected result
Zero non-quarantined orphan orders; missing/wrong-type references checked separately.

### Actual result
Before manual repair: 3 non-quarantined orphan orders. After repair: zero.

## 2. Problem description
Three fictional order records reference absent users, violating the fulfillment
contract. This can break customer lookup. Original cause was incomplete fixture
import; fixture source was reviewed separately. No real project bug is asserted.

## Evidence
Fictional read-only MCP evidence: aggregation count 3; projected bounded samples
labelled order-A, order-B, order-C with synthetic absent parent labels. Type checks
found zero missing/wrong-type IDs. Index inspection found users._id indexed.
Confidence high in this fictional scenario; production and concurrent writers
are not covered. These illustrative results are not live tool results.

## 3. Proposed solution
Retain all three records and mark them quarantined for owner review rather than
delete orders or fabricate users. Set status=quarantined with an explicit reviewed
_id list and original-status predicate. Requires manual execution. Backup original
status values per ID; rollback restores those values from the scoped backup.
Prerequisite: fulfillment explicitly excludes quarantined records. Risk: hiding
orders from active workflows; owner must reconcile later. Verification repeats
original aggregation and checks retained records and quarantine count.

## Repair plan
Illustrative reference: repair-plans/BUG-001-v1.json. Proposal execution_status:
not_executed_read_only_mcp. The MongoDB MCP server is read-only. This repair plan has not modified the database.

## Approval
- Approval status: approved
- Approved scope: exact three fictional IDs, original status=open
- Approved environment: testing
- Approved operation: updateMany setting status=quarantined

## Executed correction
Not executed through the read-only MongoDB MCP server.

Fictional user-provided execution evidence: administrator command output confirmed
testing/ecommerce/orders and the exact three-ID filter plus status=open; updateMany
with {$set: {status: 'quarantined'}}. Matched count: 3; modified count: 3; created or
changed indexes: none; skipped documents: 0; errors: none. Evidence reference:
fictional-user-output-001. This is an example of acceptable evidence, not an actual execution.

## Verification
Fictional fresh read-only MCP verification repeated the exact original pipeline:
before 3, after 0, remaining affected active orders 0. Separate reads confirmed
all three originals retained and quarantined, collection count unchanged, zero
new type/reference inconsistencies, and all criteria passed. Final verification
status: passed. Quarantined references still need owner reconciliation; they are
not claimed to have been restored. Illustrative result: verification-results/BUG-001-v1.json.

## Final solution
In this fictional scenario only, the user manually quarantined the three scoped
orders. Read-only verification confirmed no active orphan orders and no deletion.
The completed correction is quarantine, not reconstruction of missing users.

## History
- detected: fictional missing-parent symptom reported.
- investigated: read-only count and contract established.
- solution-proposed: retain/quarantine approach selected.
- repair-plan-generated: version 1 proposed; not executed through MCP.
- awaiting-manual-execution: scoped plan approved.
- manually-corrected: fictional administrator output received.
- verified: fictional fresh MCP postconditions passed.
