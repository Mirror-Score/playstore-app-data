#  Inspired from:
#  https://github.com/CCExtractor/sample-platform/blob/master/mod_deploy/controllers.py
import hashlib
import hmac
from datetime import datetime, timedelta
from functools import wraps
from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network
from typing import Callable, List, Union

import requests
from flask import abort, current_app, g, request

IPAddress = Union[IPv4Address, IPv6Address]
cached_web_hook_blocks: List[str] = []
cached_load_time: datetime = datetime(1970, 1, 1)


def cache_has_expired() -> bool:
    """Check if the cache expired.

    Returns:
        bool: True if the cache was last updated more than one hour ago
    """
    global cached_load_time
    return cached_load_time + timedelta(hours=1) < datetime.now()


def get_cached_web_hook_blocks() -> List[str]:
    """Fetch the cached web hook blocks

    Returns:
        List[str]: A list of ip blocks
    """
    global cached_web_hook_blocks

    if len(cached_web_hook_blocks) == 0 or cache_has_expired():
        client_id = current_app.config.get("GITHUB_CLIENT_ID", "")
        client_secret = current_app.config.get("GITHUB_CLIENT_SECRET", "")
        meta_json = requests.get(
            current_app.config["GITHUB_URL"],
            params=dict(client_id=client_id, client_secret=client_secret),
        ).json()

        try:
            cached_web_hook_blocks = meta_json["hooks"]
        except KeyError:
            g.log.critical(
                f"Failed to retrieve hook IP's from GitHub! API returned {meta_json}"
            )

    return cached_web_hook_blocks


def is_github_web_hook_ip(request_ip: IPAddress) -> bool:
    """Check if the given IP address is matching one provided by the API of GitHub

    Args:
        request_ip (IPAddress): The IP address the request came from

    Returns:
        bool: True if the IP address is a valid GitHub Web Hook requester
    """
    for block in get_cached_web_hook_blocks():
        if request_ip in ip_network(block):
            return True
    return False


def request_from_github(abort_code: int = 418) -> Callable:
    """Provide decorator to handle request from GitHub on the web hook

    Args:
        abort_code (int, optional): Defaults to 418.
    """

    def decorator(f):
        """Decorate the function to check if a request is a GitHub hook request."""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method != "POST":
                return "OK"

            request_ip = ip_address(f"{request.remote_addr}")
            if not is_github_web_hook_ip(request_ip):
                g.log.warning(f"Unauthorized attempt to deploy by IP {request_ip}")
                abort(abort_code)

            for header in [
                "X-GitHub-Event",
                "X-GitHub-Delivery",
                "X-Hub-Signature",
                "User-Agent",
            ]:
                if header not in request.headers:
                    g.log.critical(f"{header} not in headers!")
                    abort(abort_code)

            ua = request.headers.get("User-Agent")
            if not ua.startswith("GitHub-Hookshot/"):
                g.log.critical("User-Agent does not begin with GitHub-Hookshot/!")
                abort(abort_code)

            if not request.is_json:
                g.log.critical("Request is not JSON!")
                abort(abort_code)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def is_valid_signature(x_hub_signature: str, data: bytearray, private_key: str) -> bool:
    """Re-check if the GitHub hook request got valid signature

    Args:
        x_hub_signature (str): Signature to check
        data (bytearray): Signature's data
        private_key (str): Signature's token

    Returns:
        bool: True if valid else false
    """
    hash_algorithm, github_signature = x_hub_signature.split("=", 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, "latin-1")
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)
