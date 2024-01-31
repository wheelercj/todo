import os
import sys
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI


def get_inputs():
    load_dotenv()

    due_string: str = "today"

    api_token: str = os.environ["todoist_api_token"]
    if not api_token:
        print("Error: could not find env var `todoist_api_token`")
        sys.exit(1)

    content: str = " ".join(sys.argv[1:])
    if not content:
        print("Error: task content not given")
        sys.exit(1)
    if "System.Object[]" in content:
        print("Error: put quotes around the input when it has commas")
        sys.exit(1)

    api = TodoistAPI(api_token)

    project_id: str | None = os.environ.get("todoist_project_id")
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
