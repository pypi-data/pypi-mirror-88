"""Configuration for :mod:`pytest`."""
import pytest


@pytest.fixture(scope="function", autouse=True)
def test():
    pass
