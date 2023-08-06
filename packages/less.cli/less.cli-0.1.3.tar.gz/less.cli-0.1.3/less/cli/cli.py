import json
from os import environ, path

import click
import requests
from urllib import parse

TOKEN_FILE = "access_token.json"
LESS_ENDPOINT = environ.get("LESS_ENDPOINT", "https://pzl4olv9y9.execute-api.us-west-2.amazonaws.com/Prod/")


class LoginRequiredException(Exception):
    def __init__(self, message):
        self.message = "Must be authorized to call API"


def get_access_token(user, password):
    return requests.get(f"{LESS_ENDPOINT}/GetCLIToken?user={parse.quote(user)}&password={parse.quote(password)}")


def _access_token_headers():
    if not path.isfile(TOKEN_FILE):
        print("Please login first")
        raise LoginRequiredException()

    with open(TOKEN_FILE, "r") as f:
        access_token = json.load(f)

    return {
        "Authorization": f"Bearer {access_token['access_token']}"
    }


@click.group()
def main():
    pass


@main.command()
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(user, password):
    response = get_access_token(user, password)
    if response.status_code == 200:
        with open(TOKEN_FILE, "w") as f:
            json.dump(response.json(), f)
        print("Login success")
    else:
        print("Incorrect credentials")


@main.group("api")
def api():
    pass


@api.command("list")
def list_apis():
    try:
        access_token_headers = _access_token_headers()
    except LoginRequiredException:
        return

    res = requests.get(f"{LESS_ENDPOINT}/Api", headers=access_token_headers)
    if res.status_code == 200:
        print(res.json())
    else:
        print(res.text)


@api.command("set-custom-code")
@click.option("--filename", required=True)
@click.option("--name", required=True)
def api_set_custom_code(filename, name):
    if not path.isfile(filename):
        print(f"File {filename} not found")
        return
    with open(filename, "r") as f:
        custom_code = f.read()

    try:
        access_token_headers = _access_token_headers()
    except LoginRequiredException:
        return

    res = requests.post(f"{LESS_ENDPOINT}/Api", headers=access_token_headers, json={
        "name": name,
        "custom_code": custom_code
    })
    print(res.status_code)
    print(res.text)


if __name__ == "__main__":
    main()
