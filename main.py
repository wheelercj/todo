# external imports
import os
import re
import requests
import uuid
import json
from typing import Optional
from dotenv import load_dotenv

# internal import
from project import Project, Projects


def main():
    """Prints all active tasks in one project, or creates multiple tasks from markdown"""
    load_dotenv()
    api_token: str = get_api_token()
    projects: Projects = fetch_projects(api_token)
    print_project_names(projects)
    project_name: str = input('Enter a project name: ')

    try:
        project_id: int = get_project_id(project_name, projects)
    except ValueError as e:
        print(e)
    else:
        project = Project(project_name, project_id, api_token)

        chosen_action = input(
            '1. view tasks'
            '\n2. add tasks'
            '\n> ')
        if chosen_action == '1':
            project.print()
        elif chosen_action == '2':
            add_tasks(project)


def get_api_token() -> str:
    """Gets the API token from a .env file or directly from the user
    
    If a .env file is not found, the user is asked for the token. If the user
    provides the token, a .env file with the token is created.
    """
    try:
        api_token = os.environ['my_todoist_api_token']
    except KeyError:
        print('Find your Todoist API token in settings > integrations')
        api_token = input('and enter it here: ')
        with open('.env', 'a') as file:
            file.write(f'my_todoist_api_token={api_token}')
    return api_token


def fetch_projects(api_token: str) -> Projects:
    """Fetches all projects"""
    return requests.get(
        'https://api.todoist.com/rest/v1/projects',
        headers={
            'Authorization': f'Bearer {api_token}'}
    ).json()


def print_project_names(projects: Projects) -> None:
    """Prints the names of Todoist projects"""
    print('Here are all of your current Todoist projects:')
    for project in projects:
        print(project['name'])


def get_project_id(chosen_project_name: str, projects: Projects) -> int:
    """Gets a Todoist project's ID by its name
    
    Raises ValueError if the project does not exist.
    """
    for project in projects:
        if project['name'] == chosen_project_name:
            return project['id']
    raise ValueError('Project not found')


def add_tasks(project: Project) -> None:
    """Creates tasks & sections from input, and adds them to Todoist"""
    print('Enter the tasks with each task on its own line. To add a date to a '
        '\ntask, use [YYMMDD] (including the square brackets) at the end of '
        '\nthe line, e.g. [210908] to set the due date to 2021-9-8. Sections '
        '\ncan be created by starting their lines with # (tag symbols). After '
        '\nentering all tasks and sections, enter DONE')
    title = ''
    section_id = None
    while title != 'DONE':
        title = input().strip()
        if title == 'DONE':
            break
        elif not title:
            continue
        elif title.startswith('#'):
            title = title.lstrip('#').strip()
            section_id: int = post_section(title, project)
        else:
            title, due_date = parse_task(title)
            post_task(title, project, section_id, due_date)

    print('Tasks created')


def parse_task(content: str) -> tuple[str, Optional[str]]:
    """Removes unneeded markdown and finds a due date, if present
    
    If a due date is returned, it is in the format YYYY-MM-DD.
    """
    if content.startswith('*'):
        content = content.lstrip('*').strip()
    elif content.startswith('- [ ]'):
        content = content.lstrip('- [ ]').strip()
    elif content.startswith('-'):
        content = content.lstrip('-').strip()

    due_date = None
    match = re.search(r'\[\d{6}\]$', content)
    if match:
        due_date = match[0].lstrip('[').rstrip(']')
        due_date = f'20{due_date[:2]}-{due_date[2:4]}-{due_date[4:]}'
        content = content.removesuffix(match[0]).strip()
    
    return content, due_date


def post_section(section_title: str, project: Project) -> int:
    """Makes an API request to add a new Todoist task section
    
    Returns the new section's ID.
    """
    response: str = requests.post(
        'https://api.todoist.com/rest/v1/sections',
        data=json.dumps({
            'project_id': project.id,
            'name': section_title
        }),
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {project.api_token}'
        }).json()

    return response['id']


def post_task(task_title: str, project: Project, section_id: Optional[int], due_date: Optional[str]) -> None:
    """Makes an API request to add a new task to Todoist
    
    Due dates must be in the YYYY-MM-DD format.
    """
    data = {
        'content': task_title,
        'due_lang': 'en',
        'project_id': project.id }
    if section_id:
        data['section_id'] = section_id
    if due_date:
        data['due_date'] = due_date

    requests.post(
        'https://api.todoist.com/rest/v1/tasks',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {project.api_token}'
        }).json()


if __name__ == '__main__':
    main()
