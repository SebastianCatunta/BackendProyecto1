#!/usr/bin/env python3
"""Compare redacted MCP snapshot files offline; never connect or modify report status.

Snapshot contract: references/bug-documentation-schema.json#/$defs/snapshot.
Exit 0 = eligible verification, 1 = failed/incomplete evidence, 2 = invalid input.
"""
import argparse
import json
from pathlib import Path
from validate_bug_report import validate


def check(before, after, report):
    reasons = []
    for label, snapshot in [('before', before), ('after', after)]:
        if not isinstance(snapshot, dict):
            return ['snapshot must be an object'], None
        for key in ['bug_id', 'environment', 'database', 'collection', 'scope', 'detection_query', 'source', 'evidence_reference', 'criteria']:
            if key not in snapshot or snapshot[key] in [None, '', [], {}]:
                reasons.append(label + ': missing ' + key)
        count = snapshot.get('affected_count')
        if type(count) is not int or count < 0:
            reasons.append(label + ': invalid affected_count')
        if snapshot.get('source') != 'read-only-mcp' or snapshot.get('complete') is not True:
            reasons.append(label + ': complete read-only MCP evidence required')
        criteria = snapshot.get('criteria')
        if not isinstance(criteria, dict) or not criteria or any(type(v) is not bool for v in criteria.values()):
            reasons.append(label + ': criteria must be a nonempty boolean map')
    for key, heading in [('bug_id', 'Bug ID'), ('environment', 'Environment'), ('database', 'Database'), ('collection', 'Collection')]:
        if before.get(key) != after.get(key) or after.get(key) != report.get(heading):
            reasons.append('target mismatch: ' + key)
    for key in ['scope', 'detection_query']:
        if before.get(key) != after.get(key):
            reasons.append('original detection scope/query changed: ' + key)
    if isinstance(before.get('criteria'), dict) and isinstance(after.get('criteria'), dict):
        if set(before['criteria']) != set(after['criteria']):
            reasons.append('verification criteria changed')
        if not all(v is True for v in after['criteria'].values()):
            reasons.append('post-correction criteria failed')
    if after.get('affected_count') != 0:
        reasons.append('remaining affected documents/objects are not zero')
    if after.get('new_inconsistencies') != 0 or type(after.get('new_inconsistencies')) is not int:
        reasons.append('new-inconsistency check missing or failed')
    execution = after.get('execution_evidence', {})
    if not isinstance(execution, dict):
        execution = {}
    for key in ['provided_by', 'reference', 'operation', 'exact_filter', 'matched_count', 'modified_count', 'changed_indexes', 'skipped_documents', 'errors']:
        if key not in execution:
            reasons.append('execution evidence missing: ' + key)
    if execution.get('provided_by') != 'user' or not execution.get('reference') or not execution.get('operation'):
        reasons.append('scoped user-provided execution provenance required')
    for key in ['environment', 'database', 'collection', 'scope']:
        if execution.get(key) != after.get(key):
            reasons.append('execution target/scope mismatch: ' + key)
    if execution.get('approved_plan_reference') != after.get('approved_plan_reference') or not after.get('approved_plan_reference'):
        reasons.append('approved repair plan reference missing/mismatched')
    if execution.get('approved') is not True:
        reasons.append('scoped approval evidence required')
    for key in ['matched_count', 'modified_count']:
        value = execution.get(key)
        if value is not None and (type(value) is not int or value < 0):
            reasons.append('invalid execution count: ' + key)
    if execution.get('matched_count') is None or execution.get('modified_count') is None:
        if not execution.get('counts_not_applicable_reason'):
            reasons.append('missing counts require explicit not-applicable reason')
    if not isinstance(execution.get('changed_indexes'), list):
        reasons.append('changed_indexes must be an explicit list')
    if execution.get('skipped_documents') != 0 or type(execution.get('skipped_documents')) is not int or execution.get('errors') != []:
        reasons.append('unresolved skips/errors or missing explicit execution results')
    return reasons, execution


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ['bug-report', 'before', 'after', 'output']:
        p.add_argument('--' + key, required=True)
    a = p.parse_args()
    try:
        report, errors, _ = validate(Path(a.bug_report).read_text(encoding='utf-8'))
        before = json.loads(Path(a.before).read_text(encoding='utf-8'))
        after = json.loads(Path(a.after).read_text(encoding='utf-8'))
        reasons, execution = check(before, after, report)
        reasons = errors + reasons
        result = {'bug_id': report.get('Bug ID'), 'verification_status': 'passed' if not reasons else 'failed-or-incomplete',
                  'eligible_for_verified': not reasons, 'before_count': before.get('affected_count'),
                  'after_count': after.get('affected_count'), 'remaining_affected_documents_or_objects': after.get('affected_count'),
                  'criteria': after.get('criteria'), 'execution_evidence': execution, 'limitations': after.get('limitations', []),
                  'reasons': reasons, 'report_status_changed': False,
                  'note': 'Offline evidence comparison only. No database write was executed; agent must confirm fresh MCP evidence before final status.'}
        target = Path(a.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
        print(result['verification_status'] + ': ' + str(target))
        for reason in reasons:
            print('CHECK:', reason)
        if reasons:
            p.exit(1)
    except (OSError, ValueError, AttributeError, TypeError) as e:
        p.exit(2, 'Invalid verification input/output: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
