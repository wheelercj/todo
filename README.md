# refactor todo list

For creating or copying Todoist tasks in bulk. Requires Python 3.9+.

Here's what it's like creating new tasks in bulk. I started off creating a new project in Todoist, but you don't need to.
![empty Todoist project](images\empty_Todoist_project.png)

Start this program. The first time it runs, it will ask for your API token and tell you where to find it.

Enter a project and choose whether you want to:
1. view all the tasks in a list that's easy to copy and paste somewhere else
2. or create new tasks in bulk
![example project name list](images\example_project_name_list.png)

Below is an example of a format that works when creating new tasks in bulk. Each task is on its own line, and tasks can optionally be given a due date by ending the line with a date in [YYMMDD] format. Any markdown bullet points or empty checkboxes at the start of the line will be removed. Lines that start with at least one # (tag symbol) will create a Todoist section.
![example tasks input](images\example_tasks_input.png)

Then the new tasks and sections appear in Todoist!
![example tasks now in Todoist](images\example_tasks_now_in_Todoist.png)
