import os
import sys

from todoist_api_python.api import TodoistAPI


def get_inputs():
    due_string: str = "today"

    with open(os.path.expanduser("~/.config/todo-saver/todoist-token"), encoding="utf8") as file:
        api_token: str = file.read().strip()
    if not api_token:
        print("Error: the Todoist API token file is empty?")
        sys.exit(1)

    content: str = " ".join(sys.argv[1:])
    if not content:
        print("Error: task content not given")
        sys.exit(1)
    if "System.Object[]" in content:
        print("Error: put quotes around the input when it has commas")
        sys.exit(1)

    api = TodoistAPI(api_token)

    with open(
        os.path.expanduser("~/.config/todo-saver/todoist-project-id"), encoding="utf8"
    ) as file:
        project_id: str = file.read().strip()
    if not project_id:
        try:
            projects = api.get_projects()
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)
        for p in projects:
            if p.name == "Inbox":
                project_id = p.id
                print(f"Using project {p.name} with id {project_id}")
                break

    return due_string, content, api, project_id
