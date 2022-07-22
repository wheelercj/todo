import json
import re
import uuid
from typing import Optional

import requests
from dotenv import load_dotenv

from create_task import fetch_projects
from create_task import get_api_token
from create_task import get_project_id
from create_task import post_task
from project import Project
from project import Projects


def main():
    """Prints all active tasks in one project, or creates multiple tasks from markdown"""
    load_dotenv()
    api_token: str = get_api_token()
    projects: Projects = fetch_projects(api_token)
    print_project_names(projects)
    project_name: str = input("Enter a project name: ")

    try:
        project_id: int = get_project_id(project_name, projects)
    except ValueError as e:
        print(e)
    else:
        project = Project(project_name, project_id, api_token)

        chosen_action = input("1. view tasks\n2. add tasks\n> ")
        if chosen_action == "1":
            project.print()
        elif chosen_action == "2":
            add_tasks(project)


def print_project_names(projects: Projects) -> None:
    """Prints the names of Todoist projects"""
    print("Here are all of your current Todoist projects:")
    for project in projects:
        print(project["name"])


def add_tasks(project: Project) -> None:
    """Creates tasks & sections from input, and adds them to Todoist"""
    print(
        "Enter the tasks with each task on its own line. To add a date to a "
        "\ntask, use [YYMMDD] (including the square brackets) at the end of "
        "\nthe line, e.g. [210908] to set the due date to 2021-9-8. Sections "
        "\ncan be created by starting their lines with # (tag symbols). After "
        "\nentering all tasks and sections, enter DONE"
    )
    title = ""
    section_id = None
    while title != "DONE":
        title = input().strip()
        if title == "DONE":
            break
        elif not title:
            continue
        elif title.startswith("#"):
            title = title.lstrip("#").strip()
            section_id: int = post_section(title, project)
        else:
            title, due_date = parse_task(title)
            post_task(title, project, section_id, due_date)

    print("Tasks created")


def parse_task(content: str) -> tuple[str, Optional[str]]:
    """Removes unneeded markdown and finds a due date, if present

    If a due date is returned, it is in the format YYYY-MM-DD.
    """
    if content.startswith("*"):
        content = content.lstrip("*").strip()
    elif content.startswith("- [ ]"):
        content = content.lstrip("- [ ]").strip()
    elif content.startswith("-"):
        content = content.lstrip("-").strip()

    due_date = None
    match = re.search(r"\[\d{6}\]$", content)
    if match:
        due_date = match[0].lstrip("[").rstrip("]")
        due_date = f"20{due_date[:2]}-{due_date[2:4]}-{due_date[4:]}"
        content = content.removesuffix(match[0]).strip()

    return content, due_date


def post_section(section_title: str, project: Project) -> int:
    """Makes an API request to add a new Todoist task section

    Returns the new section's ID.
    """
    response: str = requests.post(
        "https://api.todoist.com/rest/v1/sections",
        data=json.dumps({"project_id": project.id, "name": section_title}),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": f"Bearer {project.api_token}",
        },
    ).json()

    return response["id"]


if __name__ == "__main__":
    main()
