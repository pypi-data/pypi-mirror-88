from requests import Session

from . import CCHDOAuth

session = Session()
session.auth = CCHDOAuth()
