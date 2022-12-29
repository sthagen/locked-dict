import functools
import pathlib
import subprocess  # nosec

__all__ = ['git_describe', 'version_sync']

ENCODING = 'utf-8'
TARGET = """\
__version__ = '$version$+parent.$revision$'\
"""


@functools.lru_cache()
def _fetch_version():
    with open(pathlib.Path('pyproject.toml'), 'rt', encoding=ENCODING) as handle:
        for line in handle:
            if line.strip().startswith('version'):
                version = line.strip().split('=')[1].strip().strip('"')
    return version


def git_describe(always: bool = True) -> None:
    """Fill in the version and revision data."""
    version = _fetch_version()
    vector = ['git', 'describe', '--abbrev=8', '--dirty=-dirty']
    if always:
        vector.append('--always')
    revision = subprocess.run(vector, capture_output=True, encoding=ENCODING, text=True, check=True).stdout  # nosec
    revision = 'abadcafe' if revision is None else revision.strip()
    print(TARGET.replace('$revision$', revision).replace('$version$', version))


def version_sync() -> None:
    """Fill in the version data only."""
    print(f'version = "{_fetch_version()}"')
