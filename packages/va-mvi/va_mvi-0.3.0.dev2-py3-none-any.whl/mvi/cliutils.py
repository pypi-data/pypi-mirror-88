import tarfile
import re
from datetime import datetime
from requests.exceptions import ConnectionError as ReqConnectionError
import typer


def get_service(service_list, value, key):
    matches = [info for info in service_list if info[key] == value]
    return matches


def get_services_by_name_version(response_data, name, version):
    if name:
        response_data = get_service(response_data, name, "name")
    if version:
        response_data = get_service(response_data, version, "version")
    return response_data


def get_list_values_from_inspection(service, inspection):
    main = "*" if service["main"] else ""
    name = service["name"]
    version = service["version"]
    status = inspection["State"]["Status"]
    running = inspection["State"]["Running"]
    if running:
        timestamp = inspection["State"]["StartedAt"]
        running_msg = "Running"
    else:
        timestamp = inspection["State"]["FinishedAt"]
        running_msg = "Stopped"

    timestamp = datetime.strptime(timestamp.split(".")[0], "%Y-%m-%dT%H:%M:%S")
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    running_msg += f" (since {timestamp})"

    values = [main, name, version, status, running_msg]
    return values


def check_connection(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReqConnectionError as exc:
            # Pick out the most interesting parts of the error message
            error_pattern = re.compile(
                r"\[Errno [-0-9]+\] [A-Za-z0-9_ ]+"
            )  # Finds "[Errno #] Message"
            host_pattern = re.compile(
                r"(?<=host=')[A-Za-z0-9.\/_-]+(?=')"
            )  # Finds host='"address"'
            port_pattern = re.compile(r"(?<=port=)\d+")  # Finds port="#"
            exc_message = str(exc)
            typer.echo("Encountered a connection error!")
            typer.echo(
                f"{error_pattern.findall(exc_message)[0]} "
                f"for {host_pattern.findall(exc_message)[0]}:"
                f"{port_pattern.findall(exc_message)[0]}"
            )
            # This results in a message like:
            # [Errno 111] Connection refused for localhost:8000

            raise typer.Abort()

    return wrapper


def echo_failed_request(response):
    typer.echo(f"Function failed: {response.status_code} - {response.reason}:")
    try:
        typer.echo(f"{str(response.json()['detail'])}")
    except ValueError:
        typer.echo(f"{response.content}")
    finally:
        raise typer.Exit(1)


def sort_main_service_last(services):
    main_services = []
    sorted_services = []
    for service in services:
        if not service["main"]:
            sorted_services.append(service)
        else:
            main_services.append(service)
    sorted_services.extend(main_services)
    return sorted_services


def make_tarball(source_dir):
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Could not find the directory {source_dir}")
    with tarfile.open(source_dir.with_suffix(".tar.gz"), "w:gz") as tar:
        # By setting arcname to empty string, the root in the tarball will
        # be the same as the root of the 'source_dir'.
        tar.add(source_dir, arcname="")
    return source_dir.with_suffix(".tar.gz")


def get_request_auth_header(state):
    return {"Authorization": (f"Bearer {state['access_tokens'][state['active_host']]}")}
