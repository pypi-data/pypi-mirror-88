from urllib import parse

from chaoslib.settings import get_loaded_settings
from pdchaoscli.settings import get_api_url


def base() -> str:
    return get_api_url(get_loaded_settings())


# attacks
def attack_events(execution_id: str) -> str:
    return _get_url(base(), 'v1/attacks/executions/{}/events'.format(execution_id))


def attack_definition(definition_id: str) -> str:
    return _get_url(base(), 'v1/attacks/{}'.format(definition_id))


# scenarios
def scenario_events(execution_id: str) -> str:
    return _get_url(base(), 'v1/scenarios/executions/{}/events'.format(execution_id))


def scenario_definition(definition_id: str) -> str:
    return _get_url(base(), 'v1/scenarios/{}'.format(definition_id))


# application
def applications() -> str:
    return _get_url(base(), 'v1/applications')


def application_attacks() -> str:
    return _get_url(base(), 'v1/applications/attacks')


def _get_url(base: str, address: str):
    base = base if base.endswith("/") else base + "/"
    return parse.urljoin(base, address)
