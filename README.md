# todo

A terminal command for creating tasks in [Todoist](https://todoist.com/).

This script uses [Todoist's Python SDK](https://doist.github.io/todoist-api-python/).

## Setup

1. Install [uv](https://docs.astral.sh/uv/)
2. `git clone https://github.com/wheelercj/todo.git && cd todo`
3. Get your Todoist API token [here](https://app.todoist.com/app/settings/integrations/developer)
4. `uv run main.py add "Buy oranges"`

I recommend creating a custom terminal command to make running the script easier. You can use uv's `--project` option to specify the virtual environment's location. For example, here's the Bash command to create a `todo` command:

```bash
alias todo="uv run --project $HOME/todo $HOME/todo/main.py"
```
