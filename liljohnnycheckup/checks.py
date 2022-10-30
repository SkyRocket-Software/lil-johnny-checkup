from datetime import datetime
import socket
import ssl
import httpx


from . import settings
from .logger import logger


def do_check(url, method='head', timeout=15, user_agent=None):
    logger.debug(f'Attempting to perform {method} request to {url}')
    action = getattr(httpx, method)
    start = datetime.utcnow()
    try:
        r = action(
            url,
            timeout=timeout,
            follow_redirects=True,
            headers={
                'User-Agent': (
                    user_agent
                    if user_agent
                    else settings.HTTP_USER_AGENT
                ),
            }
        )
        r.raise_for_status()
    except httpx.ConnectTimeout as e:
        success = False
        status_code = -1
        message = f'Failed to establish connection. {e}'
    except httpx.TimeoutException as e:
        success = False
        status_code = -1
        message = f'The server did not respond before the timeout ({timeout}(s)). {e}'
    except httpx.TooManyRedirects as e:
        success = False
        status_code = -1
        message = f'Too many redirects. {e}'
    except httpx.ConnectError as e:
        success = False
        status_code = -1
        message = f'Invalid SSL/TLS Certificate. {e}'
    except httpx.HTTPStatusError as e:
        success = False
        status_code = r.status_code
        message = f'Invalid response code {e}'
    except Exception as e:
        success = False
        status_code = -1
        message = f'An unknown error occurred. Please contact support. {e}'
        if settings.DEBUG:
            raise e
    else:
        success = True
        status_code = r.status_code
        message = None
        url = str(r.url)

    end = datetime.utcnow()
    duration = (end - start).microseconds / 1000

    return success, status_code, url, message, duration


# SSL/TLS Cert Checks


def get_cert_expires_at(hostname, timeout, port):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    conn.settimeout(timeout)

    try:
        conn.connect((hostname, port))
        ssl_info = conn.getpeercert()
    except ssl.SSLCertVerificationError:
        return datetime.now()

    return datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def get_cert_is_valid(hostname, days=7, timeout=5.0, port=443):
    try:
        expires = get_cert_expires_at(hostname, timeout, port)
    except Exception as e:
        logger.error(f'Encountered error while verifying hostname: {hostname}')
        return False, 0
        is_valid = False
    else:
        remaining = expires - datetime.utcnow()
        is_valid = remaining.days > 0
        return is_valid, remaining.days
