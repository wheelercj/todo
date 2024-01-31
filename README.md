# todo

A terminal command for creating tasks in [Todoist](https://todoist.com/).

For example, `todo buy oranges`.

This script uses [Todoist's Python SDK](https://developer.todoist.com/guides/#developing-with-todoist).

## setup

1. `git clone https://github.com/wheelercj/todo.git`
2. `pip install -r todo/requirements.txt`
3. Get your API token [here](https://app.todoist.com/app/settings/integrations/developer).
4. Create a .env file with variable `todoist_api_token`.
5. Add todo.py to your PATH environment variable.
6. Restart your terminal.
7. `todo see if this works`

You can also add to the .env file the variable `todoist_project_id` if you want to reduce this script's network requests. The script will tell you the project ID if you don't set the variable.

## done

There's also a `done` command for if you want to create a new task and immediately mark it as complete. The setup is the same but with done.py instead of todo.py.
