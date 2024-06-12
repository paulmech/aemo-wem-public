from support.settingscli import Settings
import pytest


def test_settings_no_script():
    with pytest.raises(Exception) as e:
        Settings(["list-files", "-max-depth", "1"])
    assert e.value.args[0] == "Expected python script name"


def test_settings_bad_command():
    with pytest.raises(Exception) as e:
        Settings(
            ["aemowem.py", "https://hello.world", "list-flies", "--max-depth", "1"]
        )
    assert e.value.args[0].startswith("Unknown command: expected one from")


def test_settings_good_options():
    settings = Settings(
        [
            "aemowem.py",
            "https://hello.world",
            "list-files",
            "--max-depth",
            "1",
            "--min-older-days",
            "30",
        ]
    )
    assert settings.options is not None
    assert "min-older-days" in settings.options
    assert "max-depth" in settings.options
    assert ["1"] == settings.options["max-depth"]
    assert ["30"] == settings.options["min-older-days"]


def test_settings_no_arguments():
    with pytest.raises(Exception) as e:
        Settings([])
    assert e.value.args[0] == "No arguments provided"


def test_settings_bad_romance_params():
    with pytest.raises(Exception) as e:
        Settings("strings")
    assert e.value.args[0] == "Expected a list of string parameters"


def test_settings_no_url():
    with pytest.raises(Exception) as e:
        Settings(["script.py"])
    assert e.value.args[0] == "URL expected"


def test_settings_bad_url():
    with pytest.raises(Exception) as e:
        Settings(["script.py", "https:/websait.com"])
    assert e.value.args[0] == "URL does not meet expectations: https:/websait.com"
