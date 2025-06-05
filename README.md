# todo

A terminal command for creating tasks in [Todoist](https://todoist.com/).

This script uses [Todoist's Python SDK](https://developer.todoist.com/guides/#developing-with-todoist).

## setup

1. `git clone https://github.com/wheelercj/todo.git && cd todo`
2. Get your Todoist API token [here](https://app.todoist.com/app/settings/integrations/developer).
3. `uv run todo.py Buy oranges`

I recommend creating a custom terminal command to make running the script easier. You can use uv's `--project` option to specify the virtual environment's location. For example, here's the Bash command to create a `todo` command:

```bash
alias todo="uv run --project $HOME/todo $HOME/todo/todo.py"
```

## done

There's also a `done` command for if you want to create a new task and immediately mark it as complete. The setup is the same but with done.py instead of todo.py.

## clear keyring

If you chose to save your Todoist API token and/or project ID into your device's keyring, you can delete them by running clear_keyring.py.
