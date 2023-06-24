#! /usr/bin/env python
"""Derive tag changes from markdown change log."""
import pathlib

ENCODING = 'utf-8'
CHG_PATH = pathlib.Path('docs/changes.md')
changes = [line.strip() for line in CHG_PATH.open('rt', encoding=ENCODING).readlines()]

out = []
found = False
for line in changes:
    if line.startswith('#') or not line:
        continue
    if not found:
        if line.startswith('20'):
            found = True
            continue
    if found:
        if line.startswith(':'):
            line = line.lstrip(': ')
        if line.startswith('*'):
            out.append('-' + line[1:])
            continue
        if not line or line.startswith('20'):
            break

print('\n'.join(out))
