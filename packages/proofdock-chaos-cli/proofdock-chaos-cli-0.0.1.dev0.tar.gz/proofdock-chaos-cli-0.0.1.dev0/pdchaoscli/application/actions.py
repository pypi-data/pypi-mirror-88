# -*- coding: utf-8 -*-
from typing import Any, Dict, List

import pdchaoscli.api.applications as app_api
from chaoslib.settings import get_loaded_settings
from chaoslib.types import Configuration, Secrets
from logzero import logger
from pdchaoscli.api.session import client_session

__all__ = ["start_attack", "cancel_attack"]


def start_attack(targets: List[Dict[str, Any]], actions: List[Dict[str, Any]],
                 path: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """Start the attack actions on the applications.

    **Be aware**: It may take up to 30s to propagate new attack configuration to all your applications.

    Parameters
    ----------
    targets : List[Target], required
        List of application you want to attack
    actions : List[Action], required
        number of seconds of delay - for a 'delay' attack
        fully qualified name of the exception - for a 'fault' attack
    path: str, optional
        path to attack
    """
    logger.debug(
        "Starting {}: configuration='{}', actions='{}', targets='{}'"
        .format(start_attack.__name__, configuration, actions, targets))

    settings = get_loaded_settings()
    for target in targets:
        application_id = target.get('application_id')
        logger.info("Starting attack on application: {}".format(application_id))
        with client_session(verify_tls=False, settings=settings) as session:
            app_api.start_attack(application_id, actions, session)

    return targets


def cancel_attack(targets: List[Dict[str, Any]] = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """Cancel running attacks.

    **Be aware**: If no 'target' is provided all attacks will be stopped.

    Parameters
    ----------
    target : List[Target], optional
        Applications for which an attack is to be canceled.
    """
    logger.debug(
        "Starting {}: configuration='{}', target='{}'"
        .format(cancel_attack.__name__, configuration, targets))

    settings = get_loaded_settings()
    with client_session(verify_tls=False, settings=settings) as session:
        app_api.cancel_attack([target.get('application_id') for target in targets], session)

    return targets
