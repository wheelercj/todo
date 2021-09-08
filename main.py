import os
import requests
import uuid
import json
from typing import Union
from dotenv import load_dotenv


# https://developer.todoist.com/rest/v1/
Projects = list[dict[str, Union[int, str, bool]]]
Tasks = list[dict[str, Union[int, str]]]


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
        chosen_action = input(
            '1. print tasks'
            '\n2. add tasks'
            '\n> ')
        if chosen_action == '1':
            print_project_tasks(chosen_project_name, project_id, api_token)
        elif chosen_action == '2':
            bulk_create_tasks(project_id, api_token)


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


def print_project_tasks(chosen_project_name: str, project_id: int, api_token: str) -> None:
    """Prints a project's tasks to the terminal"""
    active_tasks: Tasks = fetch_active_tasks(project_id, api_token)
    print(f'Here are the active tasks in the {chosen_project_name} project:')
    for task in active_tasks:
        print(task['content'])


def bulk_create_tasks(project_id: int, api_token: str) -> None:
    """Creates new Todoist tasks from text where each task is on its own line"""
    print('Enter the tasks, with each task on its own line. Then enter "DONE".')
    task_text = ''
    while task_text != 'DONE':
        task_text = input()
        if task_text == 'DONE':
            break
        post_new_task(task_text.strip(), project_id, api_token)
    print('Tasks created')


def post_new_task(task_text: str, project_id: int, api_token: str) -> None:
    """Makes an API request to add new tasks to Todoist"""
    requests.post(
        'https://api.todoist.com/rest/v1/tasks',
        data=json.dumps({
            'content': task_text,
            'due_lang': 'en',
            # 'priority': 4,
            'project_id': project_id
        }),
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {api_token}'
        }).json()


def fetch_active_tasks(project_id: int, api_token: str) -> Tasks:
    """Fetches all active tasks in a project"""
    return requests.get(
        'https://api.todoist.com/rest/v1/tasks',
        params={
            'project_id': project_id
        },
        headers={
            'Authorization': f'Bearer {api_token}'
        }).json()


if __name__ == '__main__':
    main()
