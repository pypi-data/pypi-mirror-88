import pytest
from _pytest.monkeypatch import MonkeyPatch

from fusegrader import __version__
from fusegrader.config import Config


@pytest.mark.parametrize("environment", ["development", "production"])
def test_env(monkeypatch: MonkeyPatch, environment: str) -> None:
    monkeypatch.setenv("ENV_FOR_DYNACONF", environment)
    settings = Config(environment=True)

    assert settings.env == environment
    assert settings.debug is False if environment == "production" else True
    assert settings.project_meta["version"] == __version__
