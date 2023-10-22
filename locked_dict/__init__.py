# [[[fill git_describe()]]]
__version__ = '2023.10.22+parent.5401b2a1'
# [[[end]]] (checksum: e6486a7406df5721dff8e4d6c3be9f88)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
