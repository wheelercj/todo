"""Creates a new task in Todoist"""

import sys

from common import get_inputs


def main():
    due_string, content, api, project_id = get_inputs()

    try:
        _ = api.add_task(content=content, due_string=due_string, project_id=project_id)
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)

    print("Task created")


if __name__ == "__main__":
    main()
