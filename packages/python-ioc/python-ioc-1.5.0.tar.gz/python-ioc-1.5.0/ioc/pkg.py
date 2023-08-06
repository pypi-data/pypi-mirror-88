"""Setup inversion-of-control through entrypoints."""
import pkg_resources


IOC_ENTRYPOINT_NAME = 'ioc.providers'


def get_providers():
    """Return the mapping of inversion-of-control providers and their
    entrypoints.
    """
    return [
        (entry_point.name, entry_point.load())
        for entry_point
        in pkg_resources.iter_entry_points('ioc.providers')
    ]


def setup():
    """Load all :term:`Dependency Providers` and start setting up the
    dependencies container.
    """
    for name, module in get_providers():
        if not hasattr(module, 'setup_ioc'):
            continue
        module.setup_ioc()
