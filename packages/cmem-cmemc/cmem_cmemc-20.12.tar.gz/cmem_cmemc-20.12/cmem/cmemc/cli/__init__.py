"""The main command line interface."""

import json
import os
import sys
import traceback

import click

import requests.exceptions

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.commands import (
    admin,
    config,
    dataset,
    graph,
    project,
    query,
    vocabulary,
    workflow,
    workspace
)
from cmem.cmemc.cli.context import CONTEXT
from cmem.cmemc.cli.exceptions import (
    InvalidConfiguration
)

try:
    from cmem.cmemc.cli.version import VERSION
except ImportError:
    VERSION = "SNAPSHOT"

PYTHON_VERSION = "{}.{}.{}".format(
    sys.version_info.major,
    sys.version_info.minor,
    sys.version_info.micro
)
PYTHON_EXPECTED = "3.7"
PYTHON_GOT = "{}.{}".format(
    sys.version_info.major,
    sys.version_info.minor
)
if PYTHON_EXPECTED != PYTHON_GOT:
    # test for environment which indicates that we are in completion mode
    if os.getenv("COMP_WORDS", default=None):
        pass
    elif os.getenv("_CMEMC_COMPLETE", default=None):
        pass
    else:
        CONTEXT.echo_warning(
            "Warning: Your are running cmemc under a non-tested python "
            "environment (expected {}, got {})"
            .format(PYTHON_EXPECTED, PYTHON_GOT)
        )

# set the user-agent environment for the http request headers
os.environ["CMEM_USER_AGENT"] = "cmemc/{} (Python {})"\
                                .format(VERSION, PYTHON_VERSION)

# https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py
CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='CMEMC',
    help_option_names=['-h', '--help']
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--debug',
              is_flag=True,
              help='Output debug messages and stack traces after errors.')
@click.option('-q', '--quiet',
              is_flag=True,
              help='Suppress any non-error info messages.')
@click.option('--config-file',
              autocompletion=completion.ini_files,
              type=click.Path(
                  readable=True,
                  allow_dash=False,
                  dir_okay=False
              ),
              default=CONTEXT.config_file_default,
              show_default=True,
              help='Use this config file instead of the default one.')
@click.option('-c', '--connection',
              type=click.STRING,
              autocompletion=completion.connections,
              help='Use a specific connection from the config file.')
@click.version_option(
    version=VERSION,
    message="%(prog)s, version %(version)s, "
            "running under python {}".format(PYTHON_VERSION)
)
@click.pass_context
def cli(ctx, debug, quiet, config_file, connection):  # noqa: D403
    """eccenca Corporate Memory Control (cmemc).

    cmemc is the eccenca Corporate Memory Command Line Interface (CLI).

    Available commands are grouped by affecting resource type (such as graph,
    project and query). Each command / group has a separate --help
    screen to get command / group specific documentation.

    In order to see possible commands in a command group, simply
    execute the group command without further parameter (e.g. cmemc project).
    Some commands such as list, import and export can be executed in most
    command groups.
    \b
    Please have a look at the cmemc manual page for more information:

                        https://eccenca.com/go/cmemc
    """
    ctx.obj = CONTEXT
    ctx.obj.set_quiet(quiet)
    ctx.obj.set_debug(debug)
    ctx.obj.set_config_file(config_file)
    ctx.obj.set_connection(connection)


cli.add_command(config.config)
cli.add_command(workspace.workspace)
cli.add_command(graph.graph)
cli.add_command(query.query)
cli.add_command(project.project)
cli.add_command(vocabulary.vocabulary)
cli.add_command(workflow.workflow)
cli.add_command(dataset.dataset)
cli.add_command(admin.admin)


def main():
    """Start the command line interface."""
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            ValueError,
            IOError,
            InvalidConfiguration,
            NotImplementedError
    ) as error:
        CONTEXT.echo_error(str(error))
        CONTEXT.echo_debug(traceback.format_exc())
        # exceptions with response is HTTPError
        try:
            # try to load Problem Details for HTTP API JSON
            details = json.loads(error.response.text)
            error_message = ""
            if 'title' in details:
                error_message += details["title"] + ": "
            if 'detail' in details:
                error_message += details["detail"]
            CONTEXT.echo_error(error_message)
        except (AttributeError, ValueError):
            # is not json or any other issue, output plain response text
            pass
        sys.exit(1)
