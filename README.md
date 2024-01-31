# todo

A terminal command for creating tasks in [Todoist](https://todoist.com/).

For example, `todo buy oranges`

This script uses [Todoist's Python SDK](https://developer.todoist.com/guides/#developing-with-todoist).

## setup

1. `git clone https://github.com/wheelercj/todo.git`
2. `cd todo`
3. `pip install -r requirements.txt`
4. Create a .env file with variables `todoist_api_token` and `todoist_project_id`
5. Add todo.py to your PATH environment variable
6. Restart your terminal
7. `todo see if this works`

## done

There's also a `done` command for if you want to create a new task and immediately mark it as complete. The setup is the same but with done.py instead of todo.py.
