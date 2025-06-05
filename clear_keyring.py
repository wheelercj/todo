"""Clears your Todoist API token and/or project ID from your device's keyring"""

import getpass

import keyring  # https://github.com/jaraco/keyring
import keyring.errors  # https://github.com/jaraco/keyring


def main():
    repo_url: str = "github.com/wheelercj/todo"
    user: str = getpass.getuser()

    try:
        keyring.delete_password(repo_url, user)
    except keyring.errors.PasswordDeleteError:
        print("You already did not have a Todoist API token saved")
    else:
        print("Todoist API token deleted")

    try:
        keyring.delete_password(repo_url, user + " project_id")
    except keyring.errors.PasswordDeleteError:
        print("You already did not have a Todoist project ID saved")
    else:
        print("Todoist project ID deleted")


if __name__ == "__main__":
    main()
