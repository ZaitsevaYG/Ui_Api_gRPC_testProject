import pytest
from config import Config

@pytest.fixture(scope="session")
def config():

    return Config