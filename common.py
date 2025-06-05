import getpass
import sys

import click  # https://palletsprojects.com/projects/click
import keyring  # https://github.com/jaraco/keyring
from todoist_api_python.api import TodoistAPI


def get_inputs():
    due_string: str = "today"

    repo_url: str = "github.com/wheelercj/todo"
    user: str = getpass.getuser()
    api_token: str = get_todoist_api_token(repo_url, user)

    content: str = " ".join(sys.argv[1:])
    if not content:
        print("Error: task content not given")
        sys.exit(1)
    if "System.Object[]" in content:
        print("Error: put quotes around the input when it has commas")
        sys.exit(1)

    api = TodoistAPI(api_token)

    project_id: str = get_todoist_project_id(repo_url, user, api)

    return due_string, content, api, project_id


def get_todoist_api_token(repo_url: str, user: str) -> str:
    api_token: str | None = keyring.get_password(repo_url, user)
    if not api_token:
        api_token = getpass.getpass("Enter your Todoist API token: ").strip()
        if not api_token:
            print("No API token received")
            sys.exit(1)

        chose_to_save: bool = click.confirm(
            "Would you like to save the Todoist API token into your device's keyring?"
        )
        if chose_to_save:
            keyring.set_password(repo_url, user, api_token)
            print("Todoist API token saved")

    return api_token


def get_todoist_project_id(repo_url: str, user: str, api: TodoistAPI) -> str:
    user += " project_id"

    project_id: str | None = keyring.get_password(repo_url, user)
    if not project_id:
        try:
            projects = api.get_projects()
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)

        for project in projects:
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
            keyring.set_password(repo_url, user, project_id)
            print("Todoist project ID saved")

    return project_id
