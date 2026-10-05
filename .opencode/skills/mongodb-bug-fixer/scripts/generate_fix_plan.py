#!/usr/bin/env python3
"""Generate a proposed JSON repair plan offline. --dry-run prints without writing a file."""
import argparse
import json
import re
from pathlib import Path
from create_bug_report import ENVIRONMENTS

OPERATIONS = ['updateOne', 'updateMany', 'replaceOne', 'deleteOne', 'deleteMany', 'insertOne', 'createIndex', 'dropIndex', 'validator-change', 'migration', 'quarantine', 'manual-review', 'unknown']


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ['bug-id', 'database', 'collection', 'filter', 'risk', 'verification-query', 'rollback-plan', 'output']:
        p.add_argument('--' + key, required=True)
    p.add_argument('--environment', required=True, choices=ENVIRONMENTS[:-1])
    p.add_argument('--operation', required=True, choices=OPERATIONS)
    p.add_argument('--estimated-count', required=True, type=int)
    p.add_argument('--update', help='JSON object containing complete proposed payload/specification')
    p.add_argument('--backup-recommendation', default='Take a scoped consistent backup/snapshot; validate restoration before manual execution.')
    p.add_argument('--manual-instructions', default='Review and approve target/scope; take backup; rerun dry-run; stop on count drift; execute reviewed proposal outside MCP in controlled batches; supply output and verify with read-only MCP.')
    p.add_argument('--destructive', action='store_true', help='Flag destructive effects including destructive updates/migrations')
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    if not re.fullmatch(r'BUG-\d{3,}', a.bug_id):
        p.error('invalid bug-id')
    if a.estimated_count < 0:
        p.error('estimated-count cannot be negative')
    for key in ['database', 'collection', 'risk', 'verification_query', 'rollback_plan', 'backup_recommendation', 'manual_instructions']:
        if not getattr(a, key).strip():
            p.error(key + ' safety/target information must not be empty')
    try:
        filt = json.loads(a.filter)
        payload = json.loads(a.update) if a.update else None
    except ValueError as e:
        p.error('invalid JSON: ' + str(e))
    if not isinstance(filt, dict) or (payload is not None and (not isinstance(payload, dict) or not payload)):
        p.error('filter and proposal payload must be JSON objects; payload must not be empty')
    if a.operation not in ['deleteOne', 'deleteMany', 'manual-review', 'unknown'] and payload is None:
        p.error('--update requires the complete proposed operation specification')
    if a.operation in ['updateOne', 'updateMany', 'replaceOne', 'deleteOne', 'deleteMany', 'quarantine', 'migration'] and not filt:
        p.error('unbounded data mutation filter rejected')
    if a.operation in ['updateOne', 'deleteOne', 'replaceOne'] and a.estimated_count > 1:
        p.error('single-document operation estimated-count cannot exceed one')
    destructive = a.destructive or a.operation in ['deleteOne', 'deleteMany', 'dropIndex', 'replaceOne', 'migration', 'quarantine', 'validator-change']
    metadata = a.operation in ['createIndex', 'dropIndex', 'validator-change']
    plan = {
        'bug_id': a.bug_id, 'environment': a.environment, 'database': a.database,
        'collection': a.collection, 'operation_type': a.operation,
        'exact_filter': filt, 'proposed_operation': {'label': 'PROPOSED — NOT EXECUTED', 'type': a.operation, 'payload': payload},
        'estimated_affected_count': a.estimated_count,
        'dry_run_query': {'capability': 'inspect indexes/validators and compare proposed definition' if metadata else 'count and projected find', 'filter': filt, 'expected_count': a.estimated_count},
        'risk': a.risk, 'backup_recommendation': a.backup_recommendation,
        'rollback_strategy': a.rollback_plan, 'verification_query': a.verification_query,
        'manual_execution_instructions': a.manual_instructions,
        'execution_status': 'not_executed_read_only_mcp',
        'warning': 'The MongoDB MCP server is read-only. This repair plan has not modified the database.',
        'destructive': destructive, 'manual_confirmation_required': True,
        'destructive_warning': 'Destructive operation: explicit manual confirmation, consistent backup/snapshot and tested rollback/recovery required.' if destructive else None
    }
    text = json.dumps(plan, indent=2, ensure_ascii=False) + '\n'
    if a.dry_run:
        print(text, end='')
        return
    try:
        target = Path(a.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x', encoding='utf-8') as f:
            f.write(text)
        print('Saved proposed plan; no database operation executed:', target)
    except OSError as e:
        p.exit(1, 'Cannot save plan: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
