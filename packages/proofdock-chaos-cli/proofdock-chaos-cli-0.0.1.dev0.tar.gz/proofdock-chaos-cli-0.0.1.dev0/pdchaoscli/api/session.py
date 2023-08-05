from contextlib import contextmanager
from typing import Generator

from chaoslib.types import Settings
from pdchaoscli.settings import get_api_token, get_api_url
from requests import Session


@contextmanager
def client_session(verify_tls: bool = True, settings: Settings = None) -> Generator[Session, None, None]:

    # prepare auth token
    headers = {
        "Authorization": "Bearer {}".format(get_api_token(settings)),
    }

    with Session() as s:
        s.base_url = get_api_url(settings)
        s.headers.update(headers)
        s.verify = verify_tls
        yield s
