# todo

A terminal command for creating tasks in [Todoist](https://todoist.com/).

This script uses [Todoist's Python SDK](https://developer.todoist.com/guides/#developing-with-todoist).

## setup

1. `git clone https://github.com/wheelercj/todo.git`
2. Get your API token [here](https://app.todoist.com/app/settings/integrations/developer).
3. Create files named `~/.config/todo-saver/todoist-token` and `~/.config/todo-saver/todoist-project-id` with your Todoist token and the ID of the Todoist project you want to create new tasks in.
4. `uv run todo.py see if this works`

I recommend creating a custom terminal command to make using the script easier.

## done

There's also a `done` command for if you want to create a new task and immediately mark it as complete. The setup is the same but with done.py instead of todo.py.
