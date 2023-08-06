from pathlib import Path
import json
import requests
from mvi.cliutils import check_connection


CONFIG_DIR = Path.home() / ".config" / "mvi"
CONFIG_FILE = CONFIG_DIR / "mviconfig.json"


def read_cli_configuration():
    with CONFIG_FILE.open("r") as file_handle:
        config = json.load(file_handle)
    return config


def save_cli_configuration(config):
    with CONFIG_FILE.open("w+") as file_handle:
        json.dump(config, file_handle)


def initialize_cli_configuration():
    CONFIG_DIR.mkdir(exist_ok=True, parents=True)
    config = {"active_host": None, "access_tokens": dict()}
    save_cli_configuration(config)


def check_token_validity(host, token):
    if not token:
        return False

    get = check_connection(requests.get)
    response = get(
        f"{host}/auth/verify",
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )
    return response.status_code == 200
