# Pulled from emulation_system/tests/test_configuration.json
import os
from typing import Generator

import pytest
from emulation_system.settings import CONFIGURATION_FILE_LOCATION_VAR_NAME
from emulation_system.settings_models import ConfigurationSettings, DefaultFolderPaths

from emulation_system.settings import ROOT_DIR


def get_test_conf() -> ConfigurationSettings:
    conf_path = os.path.normpath(
        os.path.join(ROOT_DIR, "emulation_system", "tests", "test_configuration.json")
    )
    return ConfigurationSettings.from_file_path(conf_path)


def get_default_folder_path(name: str) -> str:
    return get_test_conf().global_settings.default_folder_paths.__getattribute__(
        name.replace("-", "_")
    )


def get_source_download_locations():
    return get_test_conf().emulation_settings.source_download_locations


def get_head(name: str) -> str:
    return get_source_download_locations().heads.__getattribute__(
        name.replace("-", "_")
    )


def get_commit(name: str) -> str:
    return get_source_download_locations().commits.__getattribute__(
        name.replace("-", "_")
    )


TEST_CONF_OPENTRONS_PATH = get_default_folder_path("opentrons")
TEST_CONF_FIRMWARE_PATH = get_default_folder_path("ot3-firmware")
TEST_CONF_MODULES_PATH = get_default_folder_path("modules")

TEST_CONF_OPENTRONS_HEAD = get_head("opentrons")
TEST_CONF_FIRMWARE_HEAD = get_head("ot3-firmware")
TEST_CONF_MODULES_HEAD = get_head("modules")

TEST_CONF_OPENTRONS_EXPECTED_COMMIT = get_commit("opentrons")
TEST_CONF_FIRMWARE_EXPECTED_COMMIT = get_commit("ot3-firmware")
TEST_CONF_MODULES_EXPECTED_COMMIT = get_commit("modules")


@pytest.fixture
def test_json_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
    )


@pytest.fixture
def test_configuration_settings(test_json_path) -> ConfigurationSettings:
    return ConfigurationSettings.from_file_path(test_json_path)


@pytest.fixture
def default_folder_paths(test_configuration_settings) -> DefaultFolderPaths:
    return test_configuration_settings.global_settings.default_folder_paths


@pytest.fixture
def set_config_file_env_var(test_json_path) -> Generator:
    os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME] = test_json_path
    yield
    del os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]