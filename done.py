"""Creates a new task in Todoist and immediately marks it as complete"""
import os
import sys
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

load_dotenv()

due_string: str = "today"
api_token: str = os.environ["todoist_api_token"]
project_id: str = os.environ["todoist_project_id"]
if not api_token:
    print("Error: could not find env var `todoist_api_token`")
    sys.exit(1)
if not project_id:
    print("Error: could not find env var `todoist_project_id`")
    sys.exit(1)

content: str = " ".join(sys.argv[1:])
if not content:
    print("Error: task content not given")
    sys.exit(1)
if "System.Object[]" in content:
    print("Error: put quotes around the input when it has commas")
    sys.exit(1)

api = TodoistAPI(api_token)

try:
    task = api.add_task(content=content, due_string=due_string, project_id=project_id)
except Exception as err:
    print(f"Error: {err}")
    sys.exit(1)

try:
    api.close_task(task.id)
except Exception as err:
    print(f"Error: {err}")
    sys.exit(1)

print("Task complete")
