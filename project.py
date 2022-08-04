from __future__ import annotations

from typing import Optional
from typing import Union

import requests


# https://developer.todoist.com/rest/v1/
Projects = list[dict[str, Union[int, str, bool]]]  # Same as API.
Task = dict[str, Union[int, str]]
Tasks = list[Task]  # Same as API.
Sections = list[dict[str, Union[int, str]]]  # Same as API.
MySections = dict[int, dict[str, Union[str, Tasks]]]  # Customized.
"""
    self.my_sections = {
        int(section_id): {
            'name': f'{section_name}',
            'tasks': Tasks()
        }
    }
"""


class Project:
    """A Todoist project with sections and tasks"""

    def __init__(self, name: str, id: int, api_token: str):
        self.name = name
        self.id = id
        self.api_token = api_token

    def fetch_tasks_and_sections(self):
        """Fetches and organizes tasks and sections."""
        self.active_tasks: Tasks = self.fetch_active_tasks()
        self.sections: Sections = self.fetch_sections()
        self.my_sections: MySections = self.get_my_sections()

    def fetch_active_tasks(self) -> Tasks:
        """Fetches all of this project's active tasks"""
        return requests.get(
            "https://api.todoist.com/rest/v1/tasks",
            params={"project_id": self.id},
            headers={"Authorization": f"Bearer {self.api_token}"},
        ).json()

    def fetch_sections(self) -> Sections:
        """Fetches all of this project's sections"""
        return requests.get(
            "https://api.todoist.com/rest/v1/sections",
            params={"project_id": self.id},
            headers={"Authorization": f"Bearer {self.api_token}"},
        ).json()

    def get_my_sections(self) -> MySections:
        """Divides this project's active tasks into sections

        Tasks without a section have a section name of None.
        """
        my_sections: MySections = {}
        for task in self.active_tasks:
            section_id = task["section_id"]
            if section_id in my_sections:
                my_sections[section_id]["tasks"].append(task)
            else:
                section_name = self.get_section_name(section_id)
                my_sections[section_id] = {"name": section_name, "tasks": [task]}

        return my_sections

    def get_section_name(self, section_id: int) -> str:
        """Gets a section's name by its ID

        Assumes the section exists.
        """
        for section in self.sections:
            if section["id"] == section_id:
                return section["name"]

    def print(self) -> None:
        """Prints this project's tasks to the terminal"""
        self.fetch_tasks_and_sections()
        print(f"\nHere are the active tasks in the {self.name} project:")
        for section in self.my_sections.values():
            section_name: str = section["name"]
            if section_name:
                print(f"## {section_name}")
            for task in section["tasks"]:
                due_date = self.get_task_due_date(task)
                if due_date:
                    print(f'  {task["content"]} [{due_date}]')
                else:
                    print(f'  {task["content"]}')

    def get_task_due_date(self, task: Task) -> Optional[str]:
        """Gets a task's due date in YYMMDD format

        Returns None if the task has no due date.
        """
        try:
            due_date: str = task["due"]["date"]  # In the form YYYY-MM-DD.
            due_date = (
                due_date[2:4] + due_date[5:7] + due_date[8:10]
            )  # In the form YYMMDD.
            return due_date
        except KeyError:
            return None
