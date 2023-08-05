from typing import Any, Dict

from chaoslib.run import RunEventHandler
from chaoslib.types import Experiment, Journal, Settings
from logzero import logger

from pdchaoscli.api.attacks import send_execution_event
from pdchaoscli.api.session import client_session
from pdchaoscli.settings import get_context


class EventHandler(RunEventHandler):
    def __init__(self, settings: Settings):
        self._execution_id = get_context(settings).get('attack').get('latest_execution').get('id')
        self._settings = settings

    def _handle_event(self, event: str, context: dict, state: dict):
        try:
            with client_session(verify_tls=False, settings=self._settings) as session:
                send_execution_event(self._execution_id, event, context, state, session)
        except Exception as ex:
            logger.error("Could not update experiment state in the Proofdock "
                         "cloud. %s", str(ex))
            logger.debug(ex)

    def started(self, experiment: Experiment, journal: Journal) -> None:
        self._handle_event('experiment-started', experiment, journal)

    def finish(self, journal: Journal) -> None:
        self._handle_event('experiment-completed', None, journal)

    def interrupted(self, experiment: Experiment,
                    journal: Journal) -> None:
        self._handle_event('experiment-interrupted', experiment, journal)

    def signal_exit(self) -> None:
        logger.error("Experiment execution caught a system signal")

    def start_continous_hypothesis(self, frequency: int) -> None:
        logger.debug("Steady state will run continously now")

    def continous_hypothesis_iteration(self, iteration_index: int,
                                       state: Any) -> None:
        logger.debug("Steady state iteration {}".format(iteration_index))

    def continous_hypothesis_completed(self, experiment: Experiment,
                                       journal: Journal,
                                       exception: Exception = None) -> None:
        logger.debug("Continous steady state is now complete")

    def start_hypothesis_before(self, experiment: Experiment) -> None:
        self._handle_event('ssh-before-started', experiment, None)

    def hypothesis_before_completed(self, experiment: Experiment,
                                    state: Dict[str, Any],
                                    journal: Journal) -> None:
        self._handle_event('ssh-before-completed', experiment, None)

    def start_hypothesis_after(self, experiment: Experiment) -> None:
        self._handle_event('ssh-after-started', experiment, None)

    def hypothesis_after_completed(self, experiment: Experiment,
                                   state: Dict[str, Any],
                                   journal: Journal) -> None:
        self._handle_event('ssh-after-completed', experiment, None)

    def start_method(self, experiment: Experiment) -> None:
        logger.debug("Method has now started")

    def method_completed(self, experiment: Experiment, state: Any) -> None:
        logger.debug("Method has now completed")

    def start_rollbacks(self, experiment: Experiment) -> None:
        logger.debug("Rollbacks have now started")

    def rollbacks_completed(self, experiment: Experiment,
                            journal: Journal) -> None:
        logger.debug("Rollbacks have now completed")

    def start_cooldown(self, duration: int) -> None:
        logger.debug("Cooldown period has now started")

    def cooldown_completed(self) -> None:
        logger.debug("Cooldown period has now completed")
