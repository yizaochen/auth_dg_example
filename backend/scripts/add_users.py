import requests
import json


def add_user(user_profile: dict):
    url = "http://localhost:3500/register/"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(user_profile))

    if response.status_code in [201, 200]:
        print("User created successfully:", response.json())
    elif response.status_code == 400:
        print("Bad request:", response.json())
    elif response.status_code == 409:
        print("Conflict: Username already exists.")
    else:
        print("Failed to create user:", response.status_code, response.text)


def main():
    """
    ROLES
    -----
    User: 2001
    Editor: 1984
    Admin: 5150
    -----
    """
    new_users = [
        {"user": "dave1", "pwd": "password1", "roles": "2001"},
        {"user": "walt2", "pwd": "password2", "roles": "2001,1984"},
        {"user": "walt1", "pwd": "password3", "roles": "2001,1984,5150"},
    ]

    for user in new_users:
        add_user(user)


if __name__ == "__main__":
    main()
