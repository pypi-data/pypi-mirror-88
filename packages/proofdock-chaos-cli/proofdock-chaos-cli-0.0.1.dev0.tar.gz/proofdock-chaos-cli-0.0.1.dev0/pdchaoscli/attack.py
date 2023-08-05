from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict

from chaoslib.types import Experiment


def build_experiment(context: Dict) -> Experiment:
    attack = context.get('attack')
    definition = attack.get('definition')
    title = attack.get('title') or 'Attack'
    description = attack.get('title') or 'Attack'

    experiment = _get_experiment_template()
    if len(definition.get('method')) > 0:
        # set meta data of experiment
        _set_experiment_meta(experiment, title, description)
        # set method section
        for item in definition.get('method'):
            _set_experiment_method(Activity.get(item), experiment)

    return experiment


def _get_experiment_template():
    return {
        "version": "1.0.0",
        "title": "",
        "description": "",
        "method": [],
        "rollbacks": []
    }


def _set_experiment_meta(experiment: Experiment, title: str, description: str):
    experiment['title'] = title
    experiment['description'] = description


def _set_experiment_method(activity: ApplicationAttackActivity, experiment: Experiment):
    activity.add_to_experiment(experiment)


class Activity(object):
    DOMAIN_APPLICATION = 'application'
    DOMAIN_AZURE = 'azure'

    def __init__(self, activity: Dict[str, Any]):
        self._activity = activity

    @staticmethod
    def get(activity: Dict[str, Any]):
        activity_type: str = activity.get('type')
        activity_type_split = activity_type.split(".")
        domain_provided = activity_type_split[0]

        if len(activity_type_split) == 1:
            # Invalid activity value
            raise Exception("Unsupported activity type")
        elif domain_provided.lower() == Activity.DOMAIN_APPLICATION:
            # Applications
            if activity_type_split[1].lower() == 'attack_request':
                return ApplicationAttackActivity(activity)
            else:
                raise Exception("Unsupported activity type")
        elif domain_provided.lower() == Activity.DOMAIN_AZURE:
            # Azure
            return AzureAttackActivity(activity)
        else:
            # Nothing matches
            raise Exception("Unsupported activity type")

    @property
    def type(self) -> str:
        return self._activity.get('type')

    @abstractmethod
    def add_to_experiment(self, experiment: Experiment):
        raise NotImplementedError()

    @property
    def arguments(self) -> str:
        return self._activity.get('arguments')


class ApplicationAttackActivity(Activity):

    def __init__(self, activity: Dict[str, Any]):
        Activity.__init__(self, activity)

    def add_to_experiment(self, experiment: Dict[str, Any]):
        # start attack and pause for a request attack duration
        method = experiment.get('method')
        method.append({
            "type": "action",
            "name": "Inject application attack",
            "provider": {
                "type": "python",
                "module": "pdchaoscli.application.actions",
                "func": "start_attack",
                "arguments": {
                    "actions": self.arguments.get('actions'),
                    "path": self.arguments.get('path'),
                    "targets": self.arguments.get('targets')
                }
            },
            "pauses": {
                "after": self.arguments.get('duration')
            }
        })
        rollbacks = experiment.get('rollbacks')
        rollbacks.append({
            "type": "action",
            "name": "Cancel application attack",
            "provider": {
                "type": "python",
                "module": "pdchaoscli.application.actions",
                "func": "cancel_attack",
                "arguments": {
                    "targets": self.arguments.get("targets")
                }
            }
        })


class AzureAttackActivity(Activity):

    def __init__(self, activity: Dict[str, Any]):
        Activity.__init__(self, activity)

    def add_to_experiment(self, experiment: Dict[str, Any]):
        activity_type_split = self._activity.get('type').split(".")
        resource = activity_type_split[1]
        func = activity_type_split[2]
        # start attack and pause for a request attack duration
        method = experiment.get('method')
        method.append({
            "type": "action",
            "name": "Inject Azure attack",
            "provider": {
                "type": "python",
                "module": "pdchaosazure.%s.actions" % resource,
                "func": func,
                "arguments": self.arguments
            }
        })
