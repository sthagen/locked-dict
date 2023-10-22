"""Derive the license information and publish in docs."""
import functools
import json
import pathlib
import pkg_resources
import string
import subprocess  # nosec
import sys
from typing import List, Tuple

import yaml

__all__ = ['dependency_tree_console_text', 'direct_dependencies_table', 'indirect_dependencies_table']

ENCODING = 'utf-8'
TP_PATH = pathlib.Path('docs', 'third-party')

TABLE_KEYS = (('Name', 'URL'), 'Version', 'License', 'Author', 'Description')
HEADER_LABELS = ('Name', 'Version', 'License', 'Author', 'Description (from packaging data)')

fallbacks, FALLBACK_URLS, FALLBACK_AUTHORS, FALLBACK_DESCRIPTIONS = {}, {}, {}, {}

THIRD_PARTY_FALLBACKS = 'third-party-fallbacks.yml'
TPF_PATH = pathlib.Path('etc', THIRD_PARTY_FALLBACKS)
if TPF_PATH.is_file():
    print(f'Reading fallback values from file ({TPF_PATH})', file=sys.stderr)
    with open(TPF_PATH, 'rt', encoding=ENCODING) as handle:
        fallbacks = yaml.safe_load(handle)

if fallbacks:
    if fallbacks.get('urls', {}):
        FALLBACK_URLS = {**FALLBACK_URLS, **fallbacks['urls']}
    if fallbacks.get('authors', {}):
        FALLBACK_AUTHORS = {**FALLBACK_AUTHORS, **fallbacks['authors']}
    if fallbacks.get('descriptions', {}):
        FALLBACK_DESCRIPTIONS = {**FALLBACK_DESCRIPTIONS, **fallbacks['descriptions']}

indirect_names, INDIRECT_NAMES = [], []

INDIRECT_PACKAGE_NAMES = 'indirect-package-names.yml'
IPN_PATH = pathlib.Path('etc', INDIRECT_PACKAGE_NAMES)
if IPN_PATH.is_file():
    print(f'Reading indirect names from file ({IPN_PATH})', file=sys.stderr)
    with open(IPN_PATH, 'rt', encoding=ENCODING) as handle:
        indirect_names = yaml.safe_load(handle)

if indirect_names:
    print(f'Indirect names from file gives map ({indirect_names})', file=sys.stderr)
    if (the_names := indirect_names.get('packages', [])):
        print(f'Extending indirect packages ({the_names}) from file', file=sys.stderr)
        INDIRECT_NAMES.extend(the_names)
        INDIRECT_NAMES = sorted(set(INDIRECT_NAMES))
else:
    print(f'No indirect names from file ({IPN_PATH})', file=sys.stderr)

TARGET = """\
__version__ = '$version$+parent.$revision$'\
"""


@functools.lru_cache()
def _fetch_direct_dependency_names():
    with pathlib.Path('requirements.txt').open() as requirements_txt:
        install_requires = [
            str(requirement)
            for requirement
            in pkg_resources.parse_requirements(requirements_txt)
        ]
    return install_requires


def _generate_dependency_information() -> None:
    """Use pip-licenses for creation of diverse databases and graphs."""
    install_requires = _fetch_direct_dependency_names()
    tokens = set(list(string.ascii_letters + '-_.'))
    direct_names = [''.join(c for c in term if c in tokens).strip('.') for term in install_requires]
    print('Direct dependencies identified as:', file=sys.stderr)
    for d_dep in direct_names:
        print(f'- {d_dep}', file=sys.stderr)
    direct_vector = [
        'pip-licenses', '--format', 'json', '-p', *direct_names,
        '--with-authors', '--with-description', '--with-urls', '--with-license-file', '--with-notice-file',
        '--with-system',  # HACK A DID ACK for setuptools
        '--output-file', str(TP_PATH / 'direct-dependency-licenses.json')]
    noise = subprocess.run(direct_vector, capture_output=True, encoding=ENCODING, text=True).stdout.strip()  # nosec
    if not noise.startswith('created path: ') or not noise.endswith('direct-dependency-licenses.json'):
        raise RuntimeError(noise)

    full_vector = [
        'pip-licenses', '--format', 'json', '-p', *direct_names, *INDIRECT_NAMES,
        '--with-authors', '--with-description', '--with-urls', '--with-license-file', '--with-notice-file',
        '--with-system',  # HACK A DID ACK for setuptools
        '--output-file', str(TP_PATH / 'all-dependency-licenses.json')]
    print('Licenses search per:', ' '.join(full_vector), file=sys.stderr)
    noise = subprocess.run(full_vector, capture_output=True, encoding=ENCODING, text=True).stdout.strip()  # nosec
    if not noise.startswith('created path: ') or not noise.endswith('all-dependency-licenses.json'):
        raise RuntimeError(noise)

    """
    direct_deps='jmespath,jsonschema,langcodes,lazr.uri,orjson,pydantic,scooby,setuptools,typer'
    pipdeptree --packages "${direct_deps}" --graph-output svg > docs/third-party/package-dependency-tree.svg
    pipdeptree --packages "${direct_deps}" --json-tree --warn silence > docs/third-party/package-dependency-tree.json
    """
    base_vector = ['pipdeptree', '--packages', ','.join(direct_names)]
    jobs = (
        (TP_PATH / 'package-dependency-tree.dot.txt', base_vector + ['--graph-output', 'dot']),
        (TP_PATH / 'package-dependency-tree.svg', base_vector + ['--graph-output', 'svg']),
        (TP_PATH / 'package-dependency-tree.json', base_vector + ['--json-tree', '--warn', 'silence']),
        (TP_PATH / 'package-dependency-tree.console.txt', base_vector + ['--warn', 'silence']),
    )
    for target, vector in jobs:
        plot = subprocess.run(vector, capture_output=True, encoding=ENCODING, text=True).stdout.strip()  # nosec
        target.write_text(plot, encoding=ENCODING)


@functools.lru_cache()
def _fetch_dependencies(direct_only: bool = True):
    db = 'direct-dependency-licenses.json' if direct_only else 'all-dependency-licenses.json'
    dep_json_path = pathlib.Path('docs', 'third-party') / db
    with open(dep_json_path, 'rt', encoding=ENCODING) as handle:
        data = json.load(handle)
    return data


def _markdown_table(table: List[Tuple[str, str, str, str, str]], header_labels=HEADER_LABELS) -> str:
    """Create the gfm table as string."""
    columns = header_labels
    col_wid = {key: len(key) for key in columns}
    for slot, record in enumerate(table):
        for key, cell in zip(columns, record):
            col_wid[key] = max(len(cell), col_wid[key])

    header_cells = [key.ljust(col_wid[key]) for key in columns]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (col_wid[key] + 1) for key in columns]
    separator = f'|:{"|:".join(separator_cells)}|'

    rows = [f'| {" | ".join(str(v).ljust(col_wid[k]) for k, v in zip(columns, line))} |' for line in table]

    return '\n'.join([header] + [separator] + rows)


def _extract_rows(data):
    rows = []
    for record in data:
        nam = record['Name']
        url = record.get('URL', '')
        if url == 'UNKNOWN':
            url = FALLBACK_URLS.get(nam, '')
        nam_e = f'[{nam}]({url})' if url else nam

        ver = record['Version']
        ver_sion = f'[{ver}](https://pypi.org/project/{nam}/{ver}/)'
        lic = record['License']
        aut = record['Author']
        if aut == 'UNKNOWN' and nam in FALLBACK_AUTHORS:
            aut = FALLBACK_AUTHORS[nam]
        des = record['Description']
        if des in ('UNKNOWN', nam)  and nam in FALLBACK_DESCRIPTIONS:
            des = FALLBACK_DESCRIPTIONS[nam]
        rows.append((nam_e, ver_sion, lic, aut, des))
    rows.sort()
    return rows


def direct_dependencies_table() -> None:
    """Fill in the data from the direct dependencies."""
    _generate_dependency_information()
    data = _fetch_dependencies(direct_only=True)
    print('Direct dependencies at table generation:', file=sys.stderr)
    for d_dep in data:
        print(f'- {d_dep["Name"]}', file=sys.stderr)
    print(_markdown_table(_extract_rows(data)))


def indirect_dependencies_table() -> None:
    """Fill in the data from the indirect dependencies."""
    direct_data = _fetch_dependencies(direct_only=True)
    direct_names = tuple(record['Name'] for record in direct_data)
    indirect_only_data = [rec for rec in _fetch_dependencies(direct_only=False) if rec['Name'] not in direct_names]
    print('Indirect dependencies at table generation:', file=sys.stderr)
    for ind_dep in indirect_only_data:
        print(f'- {ind_dep["Name"]}', file=sys.stderr)

    print(_markdown_table(_extract_rows(indirect_only_data)))


def dependency_tree_console_text():
    """Fill in the pipdeptree console output minus any warnings."""
    console_tree = (TP_PATH / 'package-dependency-tree.console.txt').read_text(encoding=ENCODING).strip()
    fence = '````'
    print(f'{fence}console')
    print(console_tree)
    print(fence)
