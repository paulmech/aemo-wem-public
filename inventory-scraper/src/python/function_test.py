import os
from function import create_settings
from support.aemoconstants import ENV_AEMOWEM_URL
import pytest


def test_create_settings_without_env_url():
    if ENV_AEMOWEM_URL in os.environ:
        del os.environ[ENV_AEMOWEM_URL]

    with pytest.raises(Exception) as e:
        create_settings(None, None)
    assert e.value.args[0] == "No URL was provided in environment variable AEMOWEM_URL"


def test_create_settings():
    os.environ[ENV_AEMOWEM_URL] = "https://dirtydog.com"
    settings = create_settings(None, None)
    assert settings.url == "https://dirtydog.com"
    assert settings.command == "list-files"


def test_create_settings_from_event():
    event = {"options": {"max-depth": 2}}
    os.environ[ENV_AEMOWEM_URL] = "https://dirtydog.com"
    settings = create_settings(event, None)
    assert settings.url == "https://dirtydog.com"
    assert settings.command == "list-files"
    assert "max-depth" in settings.options
    assert settings.options["max-depth"] == ["2"]
