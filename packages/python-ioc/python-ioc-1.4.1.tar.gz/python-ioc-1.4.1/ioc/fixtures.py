"""Declares fixtures for integration with :mod:`pytest`."""
import ioc


def pytest_runtest_teardown(item, nextitem):
    """Tear down the inversion-of-control container after each test."""
    ioc.teardown()
