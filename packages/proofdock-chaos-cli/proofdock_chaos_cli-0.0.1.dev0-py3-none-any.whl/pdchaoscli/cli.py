# -*- coding: utf-8 -*-
import click
from chaoslib.control import load_global_controls
from chaoslib.exceptions import ChaosException
from chaoslib.experiment import (ensure_experiment_is_valid, run_experiment)
from chaoslib.settings import get_loaded_settings, load_settings
from chaoslib.types import Journal, Schedule, Strategy
from logzero import logger

from pdchaoscli.attack import build_experiment
from pdchaoscli.event import EventHandler
from pdchaoscli.loader import load_context, load_endpoint
from pdchaoscli.logging import configure_logger
from pdchaoscli.settings import PDCLI_CONFIG_PATH, set_context, set_endpoint


@click.group()
@click.option('--verbose', is_flag=True, help='Display debug level traces.')
@click.option('--no-log-file', is_flag=True,
              help='Disable logging to file entirely.')
@click.option('--log-file', default="pdchaoscli.log", show_default=True,
              help="File path where to write the command's log.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool = False,
        no_log_file: bool = False, log_file: str = "pdchaoscli.log"):

    if no_log_file:
        configure_logger(verbose=verbose)
    else:
        configure_logger(verbose=verbose, log_file=log_file)

    subcommand = ctx.invoked_subcommand

    # make it nicer for going through the log file
    logger.debug("#" * 79)
    logger.debug("Running command '{}'".format(subcommand))

    ctx.obj = {}
    ctx.obj["settings_path"] = click.format_filename(PDCLI_CONFIG_PATH)
    logger.debug("Using settings file '{}'".format(ctx.obj["settings_path"]))


@cli.command()
@click.option('--rollback-strategy', default="default", show_default=False,
              help="Rollback runtime strategy. Default is to never play them "
                   "on interruption or failed hypothesis.",
              type=click.Choice(['default', 'always', 'never', 'deviated']))
@click.option('--hypothesis-strategy', default="default",
              type=click.Choice([
                  "default", "before-method-only", "after-method-only",
                  "during-method-only", "continously"
              ], case_sensitive=True),
              help='Strategy to execute the hypothesis during the run.')
@click.option('--hypothesis-frequency', default=1.0, type=float,
              help='Pace at which running the hypothesis. '
                   'Only applies when strategy is either: '
                   'during-method-only or continously')
@click.option('--fail-fast', is_flag=True, default=False,
              help='When running in the during-method-only or continous '
                   'strategies, indicate the hypothesis can fail the '
                   'scenario as soon as it deviates once. Otherwise, keeps '
                   'running until the end of the scenario.')
@click.argument('definition')
@click.pass_context
def run(ctx: click.Context, definition: str,
        rollback_strategy: str = "default",
        hypothesis_strategy: str = "default",
        hypothesis_frequency: float = 1.0, fail_fast: bool = False) -> Journal:
    """Run an attack or scenario defined in the Chaos Platform."""

    settings = load_settings(PDCLI_CONFIG_PATH) or get_loaded_settings()
    try:
        set_endpoint(settings, load_endpoint())
        run_context = load_context(settings, definition)
        set_context(settings,  run_context)

        # build a CTK experiment based on the current context
        experiment = build_experiment(run_context)
    except Exception as x:
        logger.error(str(x))
        logger.debug(x)
        exit(1)

    has_deviated = False
    has_failed = False

    load_global_controls(settings)

    try:
        ensure_experiment_is_valid(experiment)
    except ChaosException as x:
        logger.error(str(x))
        logger.debug(x)
        exit(1)

    experiment["dry"] = False
    settings.setdefault(
        "runtime", {}).setdefault("rollbacks", {}).setdefault(
            "strategy", rollback_strategy)
    hypothesis_strategy = Strategy.from_string(hypothesis_strategy)
    schedule = Schedule(continous_hypothesis_frequency=hypothesis_frequency, fail_fast=fail_fast)
    event_handlers = [EventHandler(settings)]

    journal = run_experiment(experiment, settings=settings, event_handlers=event_handlers,
                             strategy=hypothesis_strategy, schedule=schedule)
    has_deviated = journal.get("deviated", False)
    has_failed = journal["status"] != "completed"

    if (has_failed or has_deviated):
        exit(1)

    return journal
