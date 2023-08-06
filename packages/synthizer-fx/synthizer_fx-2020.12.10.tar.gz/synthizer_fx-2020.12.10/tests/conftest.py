"""Setup tests."""

from typing import Generator

from pytest import fixture
from synthizer import Context, GlobalFdnReverb, initialize, shutdown


@fixture(scope='session', autouse=True)
def setup() -> Generator[None, None, None]:
    """Initialize and shutdown synthizer."""
    initialize()
    yield
    shutdown()


@fixture(name='context', scope='session')
def get_context() -> Context:
    """Return a synthizer context."""
    return Context()


@fixture(name='reverb')
def get_reverb(context: Context) -> GlobalFdnReverb:
    """Get a reverb object."""
    return GlobalFdnReverb(context)
