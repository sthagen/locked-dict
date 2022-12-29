import pathlib

__all__ = ['sbom_sha256']

BASE_URL = 'https://git.sr.ht/~sthagen/$REPO$/blob/default/sbom.json'
ENCODING = 'utf-8'
TARGET = """\
The [SBOM in CycloneDX v1.4 JSON format]($JSON_URL$) with SHA256 checksum ([$hash_8$ ...]($JSON_HASH_URL$ "sha256:$hash_full$")).\
"""

assumed = None
trigger, is_on = '[project]', False
with open('pyproject.toml', 'rt', encoding=ENCODING) as handle:
    for line in handle.readlines():
        text = line.strip()
        if text == trigger:
            is_on = True
            continue
        if is_on:
            stripped = text.replace(' ', '').replace('"', '').replace("'", '')
            if not stripped.startswith('name='):
                continue
            assumed = stripped.split('=', 1)[1]
            break

if assumed is None:
    assumed = str(pathlib.Path.cwd().parent)

def sbom_sha256():
    """Fill in the data."""
    with open(pathlib.Path('sbom.json.sha256'), 'rt', encoding=ENCODING) as handle:
        hash_full = handle.read().strip()
    hash_8 = hash_full[:8]
    base_path = BASE_URL.replace('$REPO$', assumed)
    j_p = base_path
    h_p = base_path + '.sha256'
    print(TARGET.replace('$hash_8$', hash_8).replace('$hash_full$', hash_full).replace('$JSON_URL$', j_p).replace('$JSON_HASH_URL$', h_p))
