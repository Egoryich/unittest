import logging
import time
import warnings


logger = logging.getLogger(__name__)


def normalize_username(raw: str) -> str:
    username = raw.strip().lower()
    if len(username) < 3:
        warnings.warn("short usernames are deprecated", DeprecationWarning, stacklevel=2)
    return username


def build_profile(payload: dict) -> dict:
    logger.info("building profile for %s", payload.get("username"))
    return {
        "username": normalize_username(payload["username"]),
        "role": payload["role"].lower(),
    }


def wait_until_ready(check_status, *, timeout, interval):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check_status():
            logger.info("status is ready")
            return True
        time.sleep(interval)
    logger.error("timed out waiting for ready status")
    return False

