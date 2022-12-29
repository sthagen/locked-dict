# [[[fill git_describe()]]]
__version__ = '2022.12.13+parent.ff7049ef'
# [[[end]]] (checksum: 853a9f21e62834d23aa0601ad62a61ce)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
