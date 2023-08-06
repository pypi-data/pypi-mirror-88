"""configuration commands for cmem command line interface."""
import click

from cmem.cmemc.cli import completion
from cmem.cmempy.health import (
    di_is_healthy, dp_is_healthy, get_di_version, get_dp_version
)


@click.command(name="list")
@click.pass_obj
def list_command(app):
    """List configured CMEM connections."""
    for section_string in app.config:
        if section_string != "DEFAULT":
            app.echo_result(section_string)


@click.command(name="edit")
@click.pass_obj
def edit_command(app):
    """Edit the user-scope configuration file."""
    app.echo_info("Open editor for config file " + app.config_file)
    click.edit(filename=app.config_file)


@click.command(name="check")
@click.argument(
    "configs",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.connections
)
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Check all configured connections."
)
@click.pass_obj
def check_command(app, configs, all_):
    """Check the status of deployment."""
    app.echo_warning(
        "This command is deprecated and will be removed with the next "
        "major release. Please use the 'admin status' command."
    )
    if all_:
        # in case --all is given,
        # list of configs is filled with all available configs
        configs = ([_ for _ in app.config if _ != "DEFAULT"])
    for config_string in configs:
        app.echo_debug("Now health check for " + config_string)
        app.set_connection(config_string)
        app.echo_success("[{}] ".format(config_string))
        # check DP
        app.echo_result("DataPlatform ", nl=False)
        if dp_is_healthy():
            app.echo_result(get_dp_version() + " ... ", nl=False)
            app.echo_success("UP")
        else:
            app.echo_result(get_dp_version() + " ... ", nl=False)
            app.echo_error("DOWN")
        # check DI
        app.echo_result("DataIntegration ", nl=False)
        if di_is_healthy():
            app.echo_result(get_di_version() + " ... ", nl=False)
            app.echo_success("UP")
        else:
            app.echo_result(get_di_version() + " ... ", nl=False)
            app.echo_error("DOWN")


@click.group()
def config():
    u"""List, edit and check configurations.

    Configurations are identified by the section identifier in the
    config file. Each configuration represent a Corporate Memory deployment
    with its specific access method as well as credentials.

    A minimal configuration which uses client credentials has the following
    entries:

    \b
    [example.org]
    CMEM_BASE_URI=https://cmem.example.org/
    OAUTH_GRANT_TYPE=client_credentials
    OAUTH_CLIENT_ID=cmem-service-account
    OAUTH_CLIENT_SECRET=my-secret-account-pass

    In addition to that, the following config parameters can be used as well:

    \b
    SSL_VERIFY=False    - for ignoring certificate issues (not recommended)
    DP_API_ENDPOINT=URL - to point to a non-standard DataPlatform location
    DI_API_ENDPOINT=URL - to point to a non-standard DataIntegration location
    OAUTH_TOKEN_URI=URL - to point to an external IdentityProvider location
    OAUTH_USER=username - username (only if OAUTH_GRANT_TYPE=password)
    OAUTH_PASSWORD=pass - password (only if OAUTH_GRANT_TYPE=password)

    In order to request passwords on start, you can use the following
    parameter instead the PASSWORD parameter: OAUTH_PASSWORD_ENTRY=True
    OAUTH_CLIENT_SECRET_ENTRY=True.
    """


config.add_command(list_command)
config.add_command(check_command)
config.add_command(edit_command)
