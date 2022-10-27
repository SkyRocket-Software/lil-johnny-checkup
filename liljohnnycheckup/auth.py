import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from . import settings


security = HTTPBasic()


def get_account(username):
    """This function is called to check if a username /
    password combination is valid.
    """
    return next((
        entry.split(':')[1]
        for entry in settings.HTTP_USERS
        if entry.split(':')[0] == username
    ), None)


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if password := get_account(credentials.username):
        current_password_bytes = credentials.password.encode('utf-8')
        is_correct_password = secrets.compare_digest(
            current_password_bytes, password.encode('utf-8')
        )
        if is_correct_password:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={"WWW-Authenticate": "Basic"},
    )
