import os

import requests

TOKEN_ENV_VAR = "SDV_AUTH_TOKEN"
BASE_URL_ENV_VAR = "SDV_URL"
API_PATH_ENV_VAR = "SDV_API_PATH"


def set_token(token):
    os.environ[TOKEN_ENV_VAR] = token


def _get_authorization_header():
    try:
        token =  os.environ[TOKEN_ENV_VAR]
        if token.lower().startswith("bearer"):
            return token
        else:
            return f"ApiToken {token}"
    except KeyError:
        raise ValueError(
            f"Env var {TOKEN_ENV_VAR} not set. Please set it by \`sdv.set_token(\"your token here\")`"
        )


def set_base_url(base_url):
    os.environ[BASE_URL_ENV_VAR] = base_url


def _get_base_url():
    try:
        return os.environ[BASE_URL_ENV_VAR]
    except KeyError:
        return "https://app.sportdatavalley.nl"


def set_api_path(api_path):
    os.environ[API_PATH_ENV_VAR] = api_path


def _get_api_path():
    try:
        return os.environ[API_PATH_ENV_VAR]
    except KeyError:
        return "/api/v1"


def _create_session():
    session = requests.Session()
    authorization_header = _get_authorization_header()
    session.headers.update({"Authorization": authorization_header})

    return session


def _create_url(resource):
    base_url = _get_base_url()
    api_path = _get_api_path()
    return f"{base_url}{api_path}{resource}"


def cast_if_not_none(value, to_type):
    if value is not None:
        return to_type(value)
    else:
        return value
