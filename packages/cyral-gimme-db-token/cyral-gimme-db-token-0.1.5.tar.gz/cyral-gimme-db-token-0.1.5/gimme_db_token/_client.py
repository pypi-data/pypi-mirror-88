import json
import logging
import sys
import time
import webbrowser

import requests

logger = logging.getLogger("gimme_db_token")


def browser_authenticate(tenant, public_key):
    url = f"https://{tenant}.cyral.com/app/cli/{public_key}"
    webbrowser.open(url)
    print("Please continue the authentication in the opened browser window.")
    print(
        "If the window didn't automatically start, please open the following URL in \
your browser:"
    )
    print(url)


def poll_opaque_token_service(tenant, public_key, timeout):
    time_before_retry = 1  # in seconds
    num_tries = int(timeout / time_before_retry)
    if num_tries == 0:
        num_tries = 1
    url = f"https://{tenant}.cyral.com:8000/v1/opaqueToken/tokens/{public_key}"
    for _ in range(num_tries):
        try:
            r = requests.get(url)
            logger.debug(r)
            logger.debug(r.text)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue
        if r.status_code == 200:
            # successful, return
            return json.loads(r.text)
        time.sleep(time_before_retry)
    # if here, then timed out
    raise requests.exceptions.Timeout(
        f"Timeout error. Latest response from server is {r.status_code}:{r.text}"
    )
