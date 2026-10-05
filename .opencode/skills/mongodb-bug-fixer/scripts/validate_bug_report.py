#!/usr/bin/env python3
"""Validate Markdown structure and lifecycle gates offline; pending is not completed."""
import argparse
import re
from pathlib import Path
from create_bug_report import ENVIRONMENTS, CATEGORIES

STATUSES = ['detected', 'investigated', 'solution-proposed', 'repair-plan-generated', 'awaiting-manual-execution', 'manually-corrected', 'verified', 'blocked', 'unresolved']
SECTIONS = ['Bug ID', 'Status', 'Environment', 'Severity', 'Category', 'Database', 'Collection', 'Relevant fields', 'Related collections', '1. Bug location and reproduction', '2. Problem description', 'Evidence', '3. Proposed solution', 'Repair plan', 'Approval', 'Executed correction', 'Verification', 'Final solution']


def parse_report(text):
    # Ignore headings appearing inside fenced query/code examples.
    clean = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    matches = list(re.finditer(r'^## (.+?)\s*$', clean, re.M))
    return {m[1]: clean[m.end():matches[i+1].start() if i+1 < len(matches) else len(clean)].strip() for i, m in enumerate(matches)}


def validate(text):
    sections = parse_report(text)
    errors, pending = [], []
    if not re.search(r'^# Bug: \S.+$', text, re.M):
        errors.append('missing/nonempty bug title')
    for key in SECTIONS:
        body = sections.get(key, '')
        if not body:
            errors.append('missing/empty section: ' + key)
        elif re.search(r'\bPending\b|<[^>]+>|\{\{', body, re.I):
            pending.append(key)
    for key, allowed in [('Status', STATUSES), ('Environment', ENVIRONMENTS), ('Severity', ['low', 'medium', 'high', 'critical'])]:
        if sections.get(key) not in allowed:
            errors.append('invalid ' + key)
    if not re.fullmatch(r'BUG-\d{3,}', sections.get('Bug ID', '')):
        errors.append('invalid Bug ID')
    if any(x.strip() not in CATEGORIES for x in sections.get('Category', '').split(',')):
        errors.append('invalid Category')
    approval = sections.get('Approval', '')
    if not re.search(r'Approval status:\s*(not-approved|approved|rejected)\b', approval):
        errors.append('missing/invalid approval status')
    if 'Not executed through the read-only MongoDB MCP server.' not in sections.get('Executed correction', ''):
        errors.append('missing permanent read-only execution statement')
    status = sections.get('Status')
    for heading in ['Location', 'Reproduction steps', 'Detection query or aggregation', 'Expected result', 'Actual result']:
        if not re.search(r'^### ' + re.escape(heading) + r'\s*$', sections.get('1. Bug location and reproduction', ''), re.M):
            errors.append('missing reproduction subsection: ' + heading)
    gates = []
    if status in ['investigated', 'solution-proposed', 'repair-plan-generated', 'awaiting-manual-execution', 'manually-corrected', 'verified']:
        gates += ['1. Bug location and reproduction', '2. Problem description', 'Evidence']
    if status in ['solution-proposed', 'repair-plan-generated', 'awaiting-manual-execution', 'manually-corrected', 'verified']:
        gates += ['3. Proposed solution']
    if status in ['repair-plan-generated', 'awaiting-manual-execution', 'manually-corrected', 'verified']:
        gates += ['Repair plan']
    if status in ['manually-corrected', 'verified']:
        gates += ['Executed correction', 'Approval']
        if not re.search(r'user[- ]provided.*evidence', sections.get('Executed correction', ''), re.I):
            errors.append('execution evidence provenance missing')
    if status == 'verified':
        gates += ['Verification', 'Final solution']
    for key in set(gates):
        if key in pending:
            errors.append('status requires completed section: ' + key)
    return sections, errors, pending


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bug-report', required=True)
    p.add_argument('--require-complete', action='store_true', help='Fail on any pending section')
    a = p.parse_args()
    try:
        _, errors, pending = validate(Path(a.bug_report).read_text(encoding='utf-8'))
    except OSError as e:
        p.exit(1, str(e) + '\n')
    for key in pending:
        print('PENDING:', key)
    if a.require_complete and pending:
        errors.append('report contains pending sections')
    for error in errors:
        print('ERROR:', error)
    if errors:
        p.exit(1, 'Report validation failed\n')
    print('Structure/lifecycle validation passed; pending sections are not evidence of completion.')


if __name__ == '__main__':
    main()
