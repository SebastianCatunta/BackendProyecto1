#!/usr/bin/env python3
"""Create an offline report skeleton; no database access. Lists are comma-separated."""
import argparse
import re
from pathlib import Path

ENVIRONMENTS = ['local', 'development', 'testing', 'staging', 'production', 'unknown']
CATEGORIES = ['invalid-data', 'missing-field', 'invalid-type', 'duplicate-data', 'orphan-reference', 'broken-reference', 'schema-validation', 'missing-index', 'inefficient-index', 'slow-query', 'inconsistent-denormalized-data', 'migration-error', 'application-database-contract', 'unknown']


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ['bug-id', 'title', 'database', 'collection', 'output']:
        p.add_argument('--' + key, required=True)
    p.add_argument('--environment', required=True, choices=ENVIRONMENTS)
    p.add_argument('--severity', required=True, choices=['low', 'medium', 'high', 'critical'])
    p.add_argument('--category', required=True, help='Comma-separated supported categories')
    p.add_argument('--fields', default='')
    p.add_argument('--related-collections', default='')
    p.add_argument('--force', action='store_true', help='Explicitly replace an existing report')
    a = p.parse_args()
    if not re.fullmatch(r'BUG-\d{3,}', a.bug_id):
        p.error('bug-id must be BUG- followed by at least three digits')
    categories = [x.strip() for x in a.category.split(',')]
    if any(x not in CATEGORIES for x in categories):
        p.error('unsupported category; supported: ' + ', '.join(CATEGORIES))
    for key in ['title', 'database', 'collection']:
        value = getattr(a, key)
        if not value.strip() or '\n' in value or '\r' in value:
            p.error(key + ' must be a nonempty single line')
    values = vars(a).copy()
    values['category'] = ', '.join(categories)
    for key in ['fields', 'related_collections']:
        entries = [x.strip() for x in values[key].split(',') if x.strip()]
        if any('\n' in x or '\r' in x for x in entries):
            p.error(key + ' entries must be single lines')
        values[key] = '\n'.join('- ' + x for x in entries) or 'Pending: identify values or explicitly record none.'
    try:
        template = (Path(__file__).resolve().parents[1] / 'assets/bug-report-template.md').read_text(encoding='utf-8')
        text = re.sub(r'\{\{(\w+)\}\}', lambda m: values[m[1]], template)
        target = Path(a.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w' if a.force else 'x', encoding='utf-8') as f:
            f.write(text)
        print('Created detected report:', target)
    except (OSError, KeyError) as e:
        p.exit(1, 'Cannot create report: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
