import getpass
import sys
from typing import Iterator

import click  # https://palletsprojects.com/projects/click
import keyring  # https://github.com/jaraco/keyring
from todoist_api_python.api import TodoistAPI  # https://doist.github.io/todoist-api-python/
from todoist_api_python.models import Project  # https://doist.github.io/todoist-api-python/


def get_todoist_api_token(prog_id: str, user: str) -> str:
    api_token: str | None = keyring.get_password(prog_id, user)
    if not api_token:
        api_token = getpass.getpass("Enter your Todoist API token: ").strip()
        if not api_token:
            print("No API token received")
            sys.exit(1)

        chose_to_save: bool = click.confirm(
            "Would you like to save the Todoist API token into your device's keyring?"
        )
        if chose_to_save:
            keyring.set_password(prog_id, user, api_token)
            print("Todoist API token saved")

    return api_token


def get_todoist_project_id(prog_id: str, project_id_key: str, api: TodoistAPI) -> str:
    project_id: str | None = keyring.get_password(prog_id, project_id_key)
    if not project_id:
        try:
            projects_pages: Iterator[list[Project]] = api.get_projects()
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            sys.exit(1)

        for projects_page in projects_pages:
            for project in projects_page:
                if project.name == "Inbox":
                    project_id = project.id
                    print(f"Using project {project.name} with ID {project_id}")
                    break
        if not project_id:
            print("Error: no project ID found")
            sys.exit(1)

        chose_to_save: bool = click.confirm(
            "Would you like to save the Todoist project ID into your device's keyring?"
        )
        if chose_to_save:
            keyring.set_password(prog_id, project_id_key, project_id)
            print("Todoist project ID saved")

    return project_id
