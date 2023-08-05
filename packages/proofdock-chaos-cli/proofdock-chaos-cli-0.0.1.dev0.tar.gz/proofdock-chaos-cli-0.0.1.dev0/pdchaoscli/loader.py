import os

from chaoslib.exceptions import ChaosException
from logzero import logger

import pdchaoscli.api.attacks as attacks
import pdchaoscli.api.scenarios as scenarios
from pdchaoscli.api.session import client_session


def load_context(settings, definition_id):
    # check if definition id belongs to the attack
    attack = None
    with client_session(verify_tls=False, settings=settings) as session:
        try:
            attack = attacks.get_definition(definition_id, session)
        except Exception:
            logger.debug('No attack definition found.', exc_info=1)
            # fallback to scenario definition
            try:
                attack = scenarios.get_definition(definition_id, session)
            except Exception:
                logger.debug('No scenario definition found.', exc_info=1)
                raise ChaosException('Unable to get the attack/scenario definition.')
    context = {
        'attack': attack
    }
    return context


def load_endpoint():
    return {
        'url': _get_variable_or_default('PROOFDOCK_API_URL', None),
        'token': _get_variable_or_default('PROOFDOCK_API_TOKEN', None)
    }


def _get_variable_or_default(var: str, default: str):
    if var in os.environ and os.environ[var]:
        return os.environ[var]
    else:
        return default
