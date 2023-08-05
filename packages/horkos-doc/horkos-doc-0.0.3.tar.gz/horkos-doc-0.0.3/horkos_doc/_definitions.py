import typing


class Context(typing.NamedTuple):
    """The configuration to use while rendering the catalog."""

    build_dir: str = 'build'
    home_page: str = 'Horkos Docs'
    author: str = None
