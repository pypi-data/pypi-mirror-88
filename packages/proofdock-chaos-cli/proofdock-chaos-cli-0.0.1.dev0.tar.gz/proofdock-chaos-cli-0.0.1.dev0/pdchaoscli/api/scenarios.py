import json
from datetime import datetime
from typing import Dict

from pdchaoscli.api import get_error_message
from pdchaoscli.api.endpoints import scenario_definition, scenario_events
from requests import Session


def get_definition(definition_id: str, session: Session):
    response = session.get(scenario_definition(definition_id), timeout=30)
    if not response.ok:
        raise Exception(get_error_message(response))


def send_execution_event(execution_id: str, name: str, context: Dict, state, session: Session):
    data = json.dumps({
        'name': name,
        'state': state,
        'context': context,
        'timestamp': datetime.utcnow().isoformat()
    })
    response = session.post(scenario_events(execution_id), data=data, timeout=30)
    if not response.ok:
        raise Exception(get_error_message(response))
