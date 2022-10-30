from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlparse

from fastapi import FastAPI, Depends

from . import auth, checks, logger


logger = logger.logger
app = FastAPI(swagger_ui_parameters={"deepLinking": False})


@dataclass
class CheckRequest:
    url: str
    method: Literal['head', 'get'] = 'head'
    request_timeout: int = 15
    check_certificate: bool = False
    certificate_expiry_days: int = 7
    certificate_check_timeout: float = 5.0
    certificate_check_port: int = 443
    user_agent: str = None


@dataclass
class CheckResult:
    success: bool
    status_code: str
    url: str
    message: str
    duration: float
    has_valid_cert: bool
    cert_expires_in: int


@app.get('/')
def greet():
    return 'Hello from Lil\' Johnny Checkup!'


@app.post('/')
def checkup(
    check: CheckRequest,
    user=Depends(auth.authenticate)
):
    logger.info(f'Attempting to check {check.url}')
    success, status_code, url, message, duration = checks.do_check(
        check.url,
        check.method,
        check.request_timeout,
    )
    if check.check_certificate:
        logger.debug(f'Attempting to verify certificate for {url}')
        url_parts = urlparse(url)
        has_valid_cert, cert_expires_in = checks.get_cert_is_valid(
            url_parts.hostname,
            days=check.certificate_expiry_days,
            timeout=check.certificate_check_timeout,
            port=check.certificate_check_port,
        )
    else:
        logger.debug('Skipping certificate checks')
        has_valid_cert = cert_expires_in = None

    return CheckResult(
        success,
        status_code,
        url,
        message,
        duration,
        has_valid_cert,
        cert_expires_in
    )
