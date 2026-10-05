# Read-only diagnostic patterns

Adapt collection names, field names, BSON types and business rules to the project.
Examples are read-only mongosh-style notation to translate into available MCP
find/count/aggregate/explain parameters. Never run mutations or `$out`/`$merge`.
Collect exact count separately from bounded representative results, inspect code
contracts and record limitations (sampling, concurrency, partial permissions).

## Missing fields and invalid data
```javascript
db.orders.countDocuments({requiredField: {$exists: false}})
db.orders.find({requiredField: {$exists: false}}, {_id: 1}).limit(5)
db.orders.countDocuments({status: {$nin: ['open', 'closed', 'quarantined']}})
```
Missing, null and empty values are distinct; `$nin` also matches missing fields.
Use explicit predicates for business-valid exceptions, lifecycle and soft deletes.

## Invalid types
```javascript
db.orders.aggregate([
  {$match: {$expr: {$ne: [{$type: '$userId'}, 'objectId']}}},
  {$count: 'affected_count'}
])
```
Aggregation `$type` distinguishes arrays/missing; query `$type` can match array
elements. Do not convert before diagnosing: string/ObjectId mismatch can explain
apparently orphaned references. Separate numeric subtypes if contract permits.

## Duplicate values
```javascript
db.users.aggregate([
  {$match: {businessKey: {$type: 'string'}}},
  {$group: {_id: '$businessKey', n: {$sum: 1}}},
  {$match: {n: {$gt: 1}}},
  {$group: {_id: null, duplicate_groups: {$sum: 1}, affected_documents: {$sum: '$n'}}}
])
```
Specify collation/normalization, tenant key and null rules. Distinguish duplicate
groups, all participating documents and excess records. Index absence alone is
not evidence of duplicates; inspect unique/partial/sparse index definitions.

## Orphan and broken references
```javascript
db.orders.aggregate([
  {$match: {userId: {$type: 'objectId'}, status: {$ne: 'quarantined'}}},
  {$lookup: {from: 'users', localField: 'userId', foreignField: '_id', as: 'parent'}},
  {$match: {parent: {$size: 0}}},
  {$count: 'affected_count'}
])
```
For samples replace final count with project `_id,userId` and limit 5. Record
wrong-type/missing references in separate checks. A parent present but inactive,
wrong tenant, or wrong lifecycle state is a broken business reference; apply
that explicit contract in a lookup pipeline. Lookups here assume same database.

## Schema-validation violations
Read validator/options if exposed. Compare required fields, allowed types/ranges
and validationLevel/action to models and DTOs. Translate each rule to a read-only
predicate; an adaptable top-level query is `{$nor: [{$jsonSchema: REVIEWED_SCHEMA}]}`
where supported. Historical records may predate validators. Missing metadata
must not be replaced by an inferred sampled schema without qualification.

## Missing/inefficient indexes and slow queries
Inspect index keys, order, uniqueness, collation, partial predicates and workload.
Explain the exact application filter/sort/projection with representative parameters.
Compare winning plan, blocking sort, keys/documents examined versus returned,
latency and dataset size. Use executionStats only within an agreed read budget.
COLLSCAN on a tiny collection is not automatically a bug; establish latency and
resource requirements. Verify candidate plans manually later; never create indexes.

## Inconsistent denormalized data
```javascript
db.orders.aggregate([
  {$match: {items: {$type: 'array'}}},
  {$set: {computedTotal: {$sum: '$items.lineTotal'}}},
  {$match: {$expr: {$ne: ['$total', '$computedTotal']}}},
  {$count: 'affected_count'}
])
```
Pipeline `$set` transforms returned documents only, not stored data; never append
a write stage. Confirm tax, currency, rounding, refunds and types before comparing.
Report malformed arrays separately. Use the project's actual total calculation.

## Migration errors
Read migration source and provided execution logs. Compare version markers,
expected field/type distributions and invariants by cohort using group/count.
Check partially converted records and old/new field coexistence. Do not rerun
migrations or infer completion from a version marker alone.

## Application-database contract violations
Trace DTO validation → model casting → service filters → Mongo document/index
contract → response serialization. Inspect string/ObjectId use, tenant scope,
required/default fields, soft deletes, projections and uniqueness assumptions.
Describe endpoint reproduction without calling a mutating endpoint. Combine
code evidence and actual read-only database results; missing tests are not proof
of a data bug. If no safe/confirmed explanation emerges, mark unresolved.
