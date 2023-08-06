import os

import pytest

from .. import (
    _migrate_uow_config,
    _create_config_dir,
    dirs,
    _check_apikey,
    CONFIG_FILE,
    get_apikey,
)

TEST_KEY = "WyIyIiwiJDUkcm91bmRzPTUzNTAwMCRmYWtlX2RhdGEiLCJfZmFrZV9kYXRhXyJd.fake.fake"

LEGACY_CREDS = f"""
[api]
api_end_point = https://cchdo.ucsd.edu/api/v1
api_key = {TEST_KEY}
"""


def testCreateConfigDir(fs):
    _create_config_dir()

    assert os.path.exists(dirs.user_config_dir)


def testLegacyAuth(fs):
    LEGACY_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
    LEGACY_CONFIG_FILE = os.path.join(LEGACY_CONFIG_DIR, "config")
    fs.create_file(LEGACY_CONFIG_FILE, contents=LEGACY_CREDS)

    _migrate_uow_config()

    assert not os.path.exists(LEGACY_CONFIG_FILE)
    assert not os.path.exists(LEGACY_CONFIG_DIR)
    assert os.path.exists(dirs.user_config_dir)
    assert os.path.exists(os.path.join(dirs.user_config_dir, CONFIG_FILE))

    # Check that something "valid looking" was written
    assert _check_apikey(get_apikey())


def testCheckAPIKey():
    assert _check_apikey(TEST_KEY)

    with pytest.raises(ValueError):
        _check_apikey("bad")
