import os
import logging


DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = getattr(logging, os.environ.get('LOG_LEVEL', 'info').upper())
LOG_LOCATION = os.environ.get('LOG_LOCATION', '-')
HTTP_USER_AGENT = os.environ.get(
    'HTTP_USER_AGENT',
    'lil johnny checkup/v1.0'
)


# Authentication Settings


if os.environ.get('HTTP_USERS', False):
    HTTP_USERS = [
        entry for entry in os.environ.get('HTTP_USERS').split(',')
    ]
else:
    HTTP_USERS = []
