import os
from configparser import ConfigParser, NoSectionError
import logging
from typing import Optional

from requests import PreparedRequest
from requests.auth import AuthBase
from appdirs import AppDirs

try:
    import google.colab  # noqa

    COLAB = True
except ImportError:
    COLAB = False

if COLAB:
    import colab_env  # noqa

logger = logging.getLogger(__name__)

dirs = AppDirs("edu.ucsd.cchdo", "cchdo")

CONFIG_FILE = os.path.join(dirs.user_config_dir, "config.cfg")

CCHDO_PREFIX = "https://cchdo.ucsd.edu"


def _create_config_dir() -> None:
    """Creates the user config dir using ``appdirs.user_config_dir``

    The actual location is system dependent and can be found by doing the following:

    >>> from cchdo.auth import dirs
    >>> dirs.user_config_dir
    '/home/vscode/.config/edu.ucsd.cchdo'

    The above being inside the devcontainer (linux) used for this project.
    """
    os.makedirs(dirs.user_config_dir, exist_ok=True)


def _check_apikey(apikey: str) -> bool:
    """check to see if the api key "looks" ok

    It cannot validate without the secrets but the
    payload can be checked to see if it at least decodes
    """
    import json
    from base64 import b64decode

    payload, *_ = apikey.split(".")

    try:
        logger.debug("Base64 decoding api key: %s...", apikey[:10])
        decoded = b64decode(payload.encode("ASCII"))
    except Exception as ex:
        logger.error("api key was either not valid ASCII or valid base64")
        raise ValueError("API could not be decoded") from ex

    try:
        logger.debug("JSON decoding api key: %s...", decoded[:10])
        json.loads(decoded)
    except Exception as ex:
        logger.error("api key payload could not be decoded as valid JSON")
        raise ValueError("API key payload not valid") from ex

    return True


def _migrate_uow_config() -> None:
    """Migrates the old uow config file to the new appdirs defined location.

    Will remove the old config file and attempt to removed the containing directory.
    """
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
    LEGACY_CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

    logger.debug("Checking to see if legacy config needs to me migrated")

    if not os.path.isfile(LEGACY_CONFIG_FILE):
        # file does not exist, so nothing to do
        return

    logger.info("A legacy hdo_uow config was found, migrating to standardized location")
    config = ConfigParser()
    config.read(LEGACY_CONFIG_FILE)

    apikey = config.get("api", "api_key")
    _check_apikey(apikey)

    write_apikey(apikey)

    os.remove(LEGACY_CONFIG_FILE)

    try:
        logger.debug("Removing legacy config dir")
        os.rmdir(CONFIG_DIR)
    except OSError:
        logger.info(
            "Legacy config dir had files other than the config file, leaving in place"
        )


def write_apikey(apikey: str) -> None:
    """Write the apikey to the config file

    This will create the config file and containing directories if needed.
    """
    config = _load_config()

    if not config.has_section("cchdo.auth"):
        config.add_section("cchdo.auth")

    config.set("cchdo.auth", "api_key", apikey)

    _write_config(config)


def _load_config() -> ConfigParser:
    """Loads the config file into a ConfigParser object"""
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config


def _write_config(config: ConfigParser) -> None:
    """Write the ConfigParser object to the config file.

    Will create the file and containing directories if needed.
    """
    _create_config_dir()
    logger.debug("Writing config to: %s", CONFIG_FILE)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)


def get_apikey() -> str:
    """Retrieves the apikey from the first source available

    Checks the following in order:

    * The environment variable ``CCHDO_AUTH_API_KEY``
    * The local config file, which has a platform dependent location
    """
    _migrate_uow_config()

    try:
        return os.environ["CCHDO_AUTH_API_KEY"]
    except KeyError:
        pass

    try:
        return _load_config().get("cchdo.auth", "api_key")
    except NoSectionError:
        pass

    logger.warn(
        "An API Key could not be loaded from any source, many (not all) CCHDO API calls will fail"
    )
    return ""


class CCHDOAuth(AuthBase):
    """AuthClass for use with the requests library

    If the request URI is detected to be for the CCHDO api endpoint, it will automatically set the correct headers.

    If the apikey is given as a string when initialized, it will use that as the key.
    When initialized with no arguments, will attempt to load the apikey with :meth:`cchdo.auth.get_apikey`.

    >>> import requests
    >>> from cchdo.auth import CCHDOAuth
    >>> cruises = requests.get("https://cchdo.ucsd.edu/api/v1/cruise", auth=CCHDOAuth()).json()

    It is highly recomended that the :obj:`cchdo.auth.session.session` object be used instead of manually including this auth class
    """

    def __init__(self, apikey: Optional[str] = None):
        if apikey is None:
            apikey = get_apikey()
        self._apikey = apikey

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        if r.url is not None and r.url.startswith(CCHDO_PREFIX):
            r.headers["X-Authentication-Token"] = self._apikey

        return r
