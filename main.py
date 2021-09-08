import os
import requests
import uuid
import json
from typing import Union, Optional
from dotenv import load_dotenv
from requests import api


# https://developer.todoist.com/rest/v1/
Projects = list[dict[str, Union[int, str, bool]]]
Tasks = list[dict[str, Union[int, str]]]


class Project:
    def __init__(self, id: int, name: str, api_token: str):
        self.id = id
        self.name = name
        self.api_token = api_token


def main():
    """Prints all active tasks in one project, or creates multiple tasks from markdown"""
    load_dotenv()
    api_token: str = get_api_token()
    projects: Projects = fetch_projects(api_token)
    print_project_names(projects)
    chosen_project_name: str = input('Enter a project name: ')

    try:
        project_id: int = get_project_id(chosen_project_name, projects)
    except ValueError as e:
        print(e)
    else:
        project = Project(project_id, chosen_project_name, api_token)

        chosen_action = input(
            '1. print tasks'
            '\n2. add tasks'
            '\n> ')
        if chosen_action == '1':
            print_project_tasks(project)
        elif chosen_action == '2':
            bulk_create_tasks(project)


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


def print_project_tasks(project: Project) -> None:
    """Prints a project's tasks to the terminal"""
    active_tasks: Tasks = fetch_active_tasks(project)
    print(f'Here are the active tasks in the {project.name} project:')
    for task in active_tasks:
        print(task['content'])


def bulk_create_tasks(project: Project) -> None:
    """Creates new Todoist tasks and sections from user input"""
    print('Enter the tasks with each task on its own line. Sections can be '
        'created by starting their lines with # (tag symbols). After entering '
        'all tasks and sections, enter DONE')
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
            if title.startswith('*'):
                title = title.lstrip('*').strip()
            elif title.startswith('- [ ]'):
                title = title.lstrip('- [ ]').strip()
            elif title.startswith('-'):
                title = title.lstrip('-').strip()

            post_task(title, project, section_id)

    print('Tasks created')


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


def post_task(task_title: str, project: Project, section_id: Optional[int]) -> None:
    """Makes an API request to add a new task to Todoist"""
    data = {
        'content': task_title,
        'due_lang': 'en',
        'project_id': project.id }
    if section_id:
        data['section_id'] = section_id

    requests.post(
        'https://api.todoist.com/rest/v1/tasks',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {project.api_token}'
        }).json()


def fetch_active_tasks(project: Project) -> Tasks:
    """Fetches all active tasks in a project"""
    return requests.get(
        'https://api.todoist.com/rest/v1/tasks',
        params={
            'project_id': project.id
        },
        headers={
            'Authorization': f'Bearer {project.api_token}'
        }).json()


if __name__ == '__main__':
    main()
