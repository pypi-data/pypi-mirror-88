import json
from typing import Any, Dict, List

from pdchaoscli.api import endpoints, get_error_message
from requests import Session


def start_attack(app_id: str, actions: List[Dict[str, Any]], session: Session):
    data = json.dumps({
        'application_id': app_id,
        'name': '',
        'actions': actions
    })

    response = session.post(endpoints.application_attacks(), data=data, timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def cancel_attack(app_ids: List[str], session: Session):
    data = json.dumps({
        'application_ids': app_ids if app_ids else []
    })
    response = session.post("{}/cancel".format(endpoints.application_attacks()), data=data, timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
