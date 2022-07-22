import json
import os
import sys
import uuid
from datetime import datetime

import requests
from dotenv import load_dotenv

from project import Project
from project import Projects


def main():
    load_dotenv()
    api_token: str = get_api_token()
    task_content = " ".join(sys.argv[1:])
    assert task_content
    projects: Projects = fetch_projects(api_token)
    inbox_project_id: int = get_project_id("Inbox", projects)
    inbox_project = Project("Inbox", inbox_project_id, api_token)
    now = datetime.now()
    todays_date = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}"
    post_task(task_content, inbox_project, None, todays_date)


def get_api_token() -> str:
    """Gets the API token from a .env file or directly from the user

    If a .env file is not found, the user is asked for the token. If the user
    provides the token, a .env file with the token is created.
    """
    try:
        api_token = os.environ["my_todoist_api_token"]
    except KeyError:
        print("Find your Todoist API token in settings > integrations")
        api_token = input("and enter it here: ")
        with open(".env", "a") as file:
            file.write(f"my_todoist_api_token={api_token}")
    return api_token


def fetch_projects(api_token: str) -> Projects:
    """Fetches all projects"""
    return requests.get(
        "https://api.todoist.com/rest/v1/projects",
        headers={"Authorization": f"Bearer {api_token}"},
    ).json()


def get_project_id(chosen_project_name: str, projects: Projects) -> int:
    """Gets a Todoist project's ID by its name

    Raises ValueError if the project does not exist.
    """
    for project in projects:
        if project["name"] == chosen_project_name:
            return project["id"]
    raise ValueError("Project not found")


def post_task(
    task_title: str,
    project: Project,
    section_id: int = None,
    due_date: str = None,
) -> None:
    """Makes an API request to add a new task to Todoist

    Due dates must be in the YYYY-MM-DD format.
    """
    data = {"content": task_title, "due_lang": "en", "project_id": project.id}
    if section_id:
        data["section_id"] = section_id
    if due_date:
        data["due_date"] = due_date

    requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps(data),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": f"Bearer {project.api_token}",
        },
    ).json()


if __name__ == "__main__":
    main()
