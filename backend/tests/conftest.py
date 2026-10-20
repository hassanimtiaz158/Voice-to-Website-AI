import pytest


@pytest.fixture
def anyio_backend():
    """Specify that AnyIO async tests should run on asyncio only (not trio)."""
    return "asyncio"
