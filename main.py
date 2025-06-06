import getpass
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Iterator
from urllib.error import HTTPError

import click  # https://palletsprojects.com/projects/click
import jsonpickle  # https://jsonpickle.readthedocs.io/en/latest/
import keyring  # https://github.com/jaraco/keyring
import keyring.errors  # https://github.com/jaraco/keyring
from todoist_api_python.api import TodoistAPI  # https://doist.github.io/todoist-api-python/
from todoist_api_python.models import Task  # https://doist.github.io/todoist-api-python/

from todoist_client import get_todoist_api_token
from todoist_client import get_todoist_project_id


prog_folder: Path = Path(__file__).parent
pyproject_toml: Path = prog_folder / "pyproject.toml"
toml_data: dict[str, Any] = tomllib.loads(pyproject_toml.read_text())
toml_project: dict[str, Any] = toml_data["project"]
prog_name: str = toml_project["name"]
prog_version: str = toml_project["version"]
prog_id: str = "github.com/wheelercj/todo"
user: str = getpass.getuser()
project_id_key: str = user + " project_id"


@click.group()
@click.version_option(prog_version, prog_name=prog_name)
def main() -> None:
    """Manage your Todoist tasks"""


@main.command()
@click.argument("task", nargs=-1)
def add(task: tuple[str]) -> None:
    """Create a new Todoist task"""
    task_s: str = " ".join(task).strip()
    if not task_s:
        raise click.BadArgumentUsage("task is required")
    if "System.Object[]" in task_s:
        raise click.BadArgumentUsage("Put quotes around the task when it has commas")

    api_token: str = get_todoist_api_token(prog_id, user)
    api = TodoistAPI(api_token)

    project_id: str = get_todoist_project_id(prog_id, project_id_key, api)

    try:
        _ = api.add_task(content=task_s, due_string="today", project_id=project_id)
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
        if isinstance(err, HTTPError):
            print("You may need to log out and try again")
        sys.exit(1)

    print("Task created")


@main.command()
@click.argument("destination", type=click.Path(exists=True, file_okay=False))
def export(destination: str) -> None:
    """Exports your tasks as a JSON file"""
    dest_path: Path = Path(destination).resolve()

    api_token: str = get_todoist_api_token(prog_id, user)
    api = TodoistAPI(api_token)

    tasks_pages: Iterator[list[Task]] = api.get_tasks()

    tasks: list[Task] = []
    for tasks_page in tasks_pages:
        tasks.extend(tasks_page)
    print(f"Found {len(tasks)} tasks")

    tasks_json = jsonpickle.encode(tasks)
    assert isinstance(tasks_json, str)

    now: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path: Path = dest_path / f"{now}_todoist_backup_v2.json"
    file_path.write_text(tasks_json, encoding="utf8")
    print(f"Backup saved to {file_path}")


@main.command()
def logout() -> None:
    """Removes your Todoist token & ID from your device's keyring"""
    try:
        keyring.delete_password(prog_id, user)
    except keyring.errors.PasswordDeleteError:
        print("You already did not have a Todoist API token saved")
    else:
        print("Todoist API token deleted")

    try:
        keyring.delete_password(prog_id, project_id_key)
    except keyring.errors.PasswordDeleteError:
        print("You already did not have a Todoist project ID saved")
    else:
        print("Todoist project ID deleted")


if __name__ == "__main__":
    main()
