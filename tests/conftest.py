import pyclip
import pytest

@pytest.fixture
def mock_video() -> pyclip.Video:
    """Fixture to generate a mock video for testing."""
    return pyclip.Video.rand()
