from typing import Optional
from pathlib import Path
import json
import requests
import pkg_resources

import typer
from tabulate import tabulate
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import FailedHookException, OutputDirExistsException
import mvi.cliutils as cliutils
import mvi.config as config

THIS_DIR = Path(__file__).parent
AUTH_TOKEN_EXPIRE_IN_DAYS = 7

# This wrapper prevent exceptions because the server is offline or the IP is wrong
post = cliutils.check_connection(requests.post)
get = cliutils.check_connection(requests.get)
delete = cliutils.check_connection(requests.delete)
put = cliutils.check_connection(requests.put)

app = typer.Typer()
state = dict()


def _get_services_for_autocompletion():
    # Autocompletion runs before callback so state is empty
    try:
        with config.CONFIG_FILE.open("r") as file_handle:
            conf = json.load(file_handle)
    except FileNotFoundError:
        return []
    response = get(
        f"{conf['active_host']}/services/",
        headers=cliutils.get_request_auth_header(conf),
    )
    if response.status_code == 200:
        return response.json()
    return []


def _autocomplete_service_name(incomplete: str):
    services = _get_services_for_autocompletion()
    valid_completion_items = [service["name"] for service in services]
    for name in valid_completion_items:
        if name.startswith(incomplete):
            yield name


def _autocomplete_service_version(ctx: typer.Context, incomplete: str):
    services = _get_services_for_autocompletion()
    # Take the service name into consideration to show relevant versions
    name = ctx.params.get("name", "")
    valid_completion_items = [
        service["version"] for service in services if service["name"] == name
    ]
    for ver in valid_completion_items:
        if ver.startswith(incomplete):
            yield ver


@app.callback()
def _callback(context: typer.Context):
    """Command-line tool for MultiViz Integrator. Initialize a new project,
    deploy services, list them and kill them in a convenient package.

    \f
    Arguments:
        context (Context): Callback context.

    Returns:
        None

    """
    # Create a configuration file if missing
    if not config.CONFIG_FILE.exists():
        config.initialize_cli_configuration()

    # Update the state from the configuration file
    with config.CONFIG_FILE.open("r") as file_handle:
        state.update(json.load(file_handle))

    # Skip host and token checks if running login function
    if context.invoked_subcommand in ["login", "init"]:
        return

    # Check if the user has an active host
    if state["active_host"] is None:
        typer.echo(
            "You must log in to a MVI host with `mvi login`"
            " before using this function."
        )
        context.abort()

    # Check that the token for the active host is valid
    valid_token = config.check_token_validity(
        state["active_host"], state["access_tokens"][state["active_host"]]
    )
    if not valid_token:
        typer.echo(
            f"You have been logged out from {state['active_host']}."
            " Please log in to the host again."
        )
        context.abort()

    typer.echo(f"Active host: {state['active_host']}")


@app.command()
def deploy(
    name: str = typer.Argument(
        ...,
        help="Name of the new service.",
        autocompletion=_autocomplete_service_name,
    ),
    version: str = typer.Argument(
        ...,
        help="Version of the new service.",
        autocompletion=_autocomplete_service_version,
    ),
    source: str = typer.Argument(
        ...,
        help=(
            "Path to the source of the service. "
            "Depending on [OPTIONS], (default): [Local directory or tar.gz archive]"
            ", (--image): [name of docker image], (--git): [URL to git repository]"
        ),
    ),
    port: Optional[int] = typer.Option(
        8000, "--port", "-p", help="Internal port for the service."
    ),
    image_flag: Optional[bool] = typer.Option(
        False, "--image", "-i", help="Deploy service from an docker image."
    ),
    git_flag: Optional[bool] = typer.Option(
        False, "--git", "-g", help="Deploy service from a git repository URL."
    ),
):
    """
    Deploy a new service.

    \f
    Args:
        name (str): Name of the new service.
        version (str): Version of the new service.
        source (str): Path to the source of the service.
        port (int, optional): Internal port for the service.
        image_flag (bool, optional): Indicate that an image is
            being used for creating the service. Default False.
        git_flag (bool, optional): Indicate that a git repository
            is being used for creating the service. Default False.

    Raises:
        Exit: If the user specifies both the -i and the -g option.
    """
    host = state["active_host"]

    if git_flag and image_flag:
        typer.echo("Error: Cannot use both -i and -g, choose one.")
        raise typer.Exit(1)

    request = {}
    request["name"] = name
    request["version"] = version
    request["port"] = port

    typer.echo("Deploying service...")
    response = None
    if image_flag:
        request["image"] = source
        response = post(
            f"{host}/services/~image",
            json=request,
            headers=cliutils.get_request_auth_header(state),
        )
    elif git_flag:
        request["git_url"] = source
        response = post(
            f"{host}/services/~git",
            json=request,
            headers=cliutils.get_request_auth_header(state),
        )
    # If neither image or git flag is active we default to a tar request.
    else:
        source = Path(source).resolve()
        if not source.exists():
            typer.echo(f"Could not find anything on the path {str(source)}")
            raise typer.Exit(1)

        if source.is_dir():
            source = cliutils.make_tarball(source)

        if source.suffixes != [".tar", ".gz"]:
            typer.echo(
                "Error: Source must be a .tar.gz file or a "
                "directory when deploying with --tar."
            )
            raise typer.Exit(1)

        response = post(
            f"{host}/services/~tar",
            data=request,
            files={"file": ("filename", open(str(source), "rb"), "application/x-gzip")},
            headers=cliutils.get_request_auth_header(state),
        )

    if response.status_code == 202:
        typer.echo("Service deployed successfully")
        # Show the started service
        ls(request["name"], request["version"])
    else:
        cliutils.echo_failed_request(response)


# pylint: disable=invalid-name
@app.command()
def ls(
    name: Optional[str] = typer.Argument(
        None,
        help="List services with this name.",
        autocompletion=_autocomplete_service_name,
    ),
    version: Optional[str] = typer.Argument(
        None,
        help="List service with this version.",
        autocompletion=_autocomplete_service_version,
    ),
):
    """List running services, filtered by name and version.

    \f
    Args:
        name (str, optional): List services with this name. Defaults to None.
        version (str, optional): List services of a certain name with this
            version. Defaults to None.
    """
    response = get(
        f"{state['active_host']}/services/",
        headers=cliutils.get_request_auth_header(state),
    )

    if response.status_code == 200:
        services = response.json()
        services = cliutils.get_services_by_name_version(services, name, version)

        # Get the info to print
        keys = ["MAIN", "NAME", "VERSION", "STATUS", "RUNNING"]
        output = []
        for service in services:
            inspection = get(
                f"{state['active_host']}/services/~inspection",
                params={"name": service["name"], "version": service["version"]},
                headers=cliutils.get_request_auth_header(state),
            ).json()

            values = cliutils.get_list_values_from_inspection(service, inspection)
            output.append(dict(zip(keys, values)))

        # Fill with empty row to print
        if len(output) == 0:
            output.append(dict(zip(keys, len(keys) * [None])))

        table = tabulate(output, headers="keys")
        typer.echo(f"{table}\n")
    else:
        cliutils.echo_failed_request(response)


@app.command()
def logs(
    name: str = typer.Argument(
        ...,
        help="Name of the service to read logs from",
        autocompletion=_autocomplete_service_name,
    ),
    version: Optional[str] = typer.Argument(
        None,
        help="Version of the service to read logs from."
        " Defaults to the main version of the service",
        autocompletion=_autocomplete_service_version,
    ),
):
    """Shows the logs for a service

    \f
    Args:
        name (str): Name of the service. Defaults to None.
        version (str, optional): Version of the service. Defaults to None.

    Raises:
        Exit: If the service name is not provided or the service cannot be found.
    """

    # Check if server exists
    response = get(
        f"{state['active_host']}/services/",
        headers=cliutils.get_request_auth_header(state),
    )
    services = []
    if response.status_code == 200:
        services = response.json()
        services = cliutils.get_services_by_name_version(services, name, version)
        if len(services) == 0:
            typer.echo("No services match the given name and version.")
            raise typer.Exit(1)
    else:
        cliutils.echo_failed_request(response)

    # If no version is specified, read logs from main version.
    if not version:
        service = cliutils.get_service(services, True, "main")
        version = service[0]["version"]

    # Get the logs
    response = get(
        f"{state['active_host']}/services/~logs/",
        params={"name": name, "version": version},
        headers=cliutils.get_request_auth_header(state),
    )
    if response.status_code == 200:
        typer.echo(response.text)
    elif response.status_code == 404:
        typer.echo(f"Failed to read logs, service {name} {version} not found.")
    else:
        cliutils.echo_failed_request(response)


@app.command()
def kill(
    name: Optional[str] = typer.Argument(
        None,
        help="Name of the service(s) to kill.",
        autocompletion=_autocomplete_service_name,
    ),
    version: Optional[str] = typer.Argument(
        None,
        help="Version of the service to kill.",
        autocompletion=_autocomplete_service_version,
    ),
    all_: Optional[bool] = typer.Option(False, "--all", "-a", help="Kill all services"),
):
    """Kill one or multiple services by name and version.

    \f
    Args:
        name (str, optional): Name of the service(s) to kill. Defaults to None.
        version (str, optional): Version of the service to kill. Defaults to None.
        all_ (bool, optional): Kill all services. Defaults to False.

    Raises:
        Exit: If there are no services to kill matching the given description.
    """
    response = get(
        f"{state['active_host']}/services/",
        headers=cliutils.get_request_auth_header(state),
    )
    if response.status_code != 200:
        cliutils.echo_failed_request(response)

    services = response.json()

    if len(services) == 0:
        typer.echo("No running services to kill.")
        raise typer.Exit(1)

    if not all_ and not name and not version:
        ls(name, version)  # List all services
        typer.echo(
            "Include the name or name and version of the service(s)"
            " to kill or -a/--all to kill all."
        )
        raise typer.Exit(1)

    services = cliutils.get_services_by_name_version(services, name, version)

    if len(services) == 0:
        typer.echo("No services match the given name and version.")
        raise typer.Exit(1)

    ls(name, version)  # List the services matching name and version

    # Get user validation
    validation = typer.confirm("Are you sure you want to kill the above service(s)?")
    if not validation:
        typer.echo("Service(s) not killed")
        raise typer.Exit()

    for service in cliutils.sort_main_service_last(services):
        response = delete(
            f"{state['active_host']}/services/",
            json={"name": service["name"], "version": service["version"]},
            headers=cliutils.get_request_auth_header(state),
        )

        if response.status_code == 200:
            typer.echo(f"Service {service['name']} {service['version']} killed.")
        elif response.status_code == 403:
            typer.echo(
                f"Cannot kill main service {service['name']} {service['version']}"
                " while it has shadows."
            )
        elif response.status_code == 404:
            typer.echo(f"Service {service['name']} {service['version']} not found.")
        else:
            typer.echo(
                f"Function failed {response.status_code} "
                f"for {service['name']} {service['version']}."
            )


@app.command()
def assign(
    name: str = typer.Argument(
        ...,
        help="Name of version to change main",
        autocompletion=_autocomplete_service_name,
    ),
    version: str = typer.Argument(
        ...,
        help="Version of service to set as main",
        autocompletion=_autocomplete_service_version,
    ),
):
    """Changes main service to the service specified.

    \f
    Args:
        name (str): Name of the service to change to primary.
        version (str): Version of the service to change to primary.

    Raises:
        Exit: If the user does not validate the assign.
    """
    validation = typer.confirm(f"Change {name} {version} to main?", default=False)
    if not validation:
        typer.echo("Assign cancelled.")
        raise typer.Exit()

    response = put(
        f"{state['active_host']}/services/~assign",
        json={"name": name, "version": version},
        headers=cliutils.get_request_auth_header(state),
    )

    if response.status_code == 200:
        typer.echo(f"Changed main version to {name} {version}")
        ls(name=name, version=None)
    else:
        cliutils.echo_failed_request(response)


@app.command()
def init(
    path: Optional[Path] = typer.Argument(
        Path.cwd(), help="Project generation output directory."
    )
):
    """
    Generates skeleton code for a new MVI project

    \f
    Args:
        path (Path, optional): Project generation output directory.

    Raises:
        Exit: If the output directory could not be found
    """
    path = path.resolve()

    if not path.is_dir():
        typer.echo(f"Could not find the directory: {str(path)}")
        raise typer.Exit(1)
    # Find out which mvi version that should be used by the service
    try:
        dist = pkg_resources.get_distribution("va-mvi")
        mvi_specifier = (
            str(dist.as_requirement())
            if dist.version != "0.0.0.dev0"
            else dist.project_name
        )  # Use full specificer unless in dev environment, then just go for the latest
    except pkg_resources.DistributionNotFound:
        typer.echo(
            "`va-mvi` package not found, assuming latest version "
            "should be used for the generated project."
        )
        mvi_specifier = "va-mvi"

    try:
        cookiecutter(
            str(THIS_DIR / "mvi_template"),
            output_dir=str(path),
            extra_context={"_mvi_specifier": mvi_specifier},
        )
    except FailedHookException:
        pass
    except OutputDirExistsException as exc:
        typer.echo(f"{str(exc)}. Could not create a new project.")


@app.command()
def token(
    lifetime: Optional[int] = typer.Argument(
        None,
        help=(
            "Number of days the token should be valid."
            " If not specified, the token will never expire."
        ),
    )
):
    """Generate a new authentication token

    \f
    Args:
        lifetime (Optional[int], optional): Number of days the token should be valid.mvi
            Default to None which correpsonds to a long-lived token.
    """
    response = post(
        f"{state['active_host']}/auth/token",
        headers=cliutils.get_request_auth_header(state),
        json={"expire_in_days": lifetime},
    )
    if response.status_code != 200:
        cliutils.echo_failed_request(response)
    token_value = response.json()["Token"]
    typer.echo(
        "Use the token in a Authorization: Bearer token,"
        " for further details see the docs"
    )
    typer.echo(token_value)


@app.command()
def login():
    """Login to the specified host

    \f
    Raises:
        Exit: If there are no services to kill matching the given description.
    """
    # Print any existing hosts and let the user choose with a number
    current_hosts = state["access_tokens"].keys()
    if len(current_hosts) > 0:
        typer.echo("Current hosts:")
        for i, key in enumerate(current_hosts):
            typer.echo(f"{i} - {key}")

    # Select host
    host = typer.prompt("Enter MVI host")

    # If user chooses a number from the current hosts
    if host.isdigit():
        try:
            host = list(current_hosts)[int(host)]
        except IndexError:
            typer.echo(f"Index {host} out of range")
            raise typer.Exit(1)

    if not (host.startswith("http://") or host.startswith("https://")):
        typer.echo("Host URL must start with http:// or https://")
        raise typer.Exit(1)

    # If the user already has a valid token we just change the active host
    valid_token = config.check_token_validity(
        host, state.get("access_tokens").get(host)
    )
    if valid_token:
        state["active_host"] = host
        config.save_cli_configuration(state)
        typer.echo(f"Changed host to {host}")
        raise typer.Exit()

    typer.echo(f"Logging in to MVI instance at {host}")
    username = typer.prompt("Username", type=str)
    password = typer.prompt("Password", type=str, hide_input=True)

    # A session scope is needed in order to keep the cookies alive
    with requests.Session() as session:
        session_post = cliutils.check_connection(session.post)
        session_get = cliutils.check_connection(session.get)

        # Login using provided credentials
        response = session_post(
            f"{host}/auth/login",
            data={"username": username, "password": password},
        )

        # Verify that we have received a cookie
        response = session_get(f"{host}/auth/verify", allow_redirects=False)
        if response.status_code != 200:
            typer.echo("Login failed!")
            raise typer.Exit(1)

        # Ask for a longlived token
        response = session_post(
            f"{host}/auth/token", params={"expire_in_days": AUTH_TOKEN_EXPIRE_IN_DAYS}
        )

        state["active_host"] = host
        state["access_tokens"][host] = response.json()["Token"]
        config.save_cli_configuration(state)
        typer.echo(f"Changed host to {host}")
