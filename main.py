#!/usr/bin/env python3

import base64
from datetime import datetime
import hashlib
import hmac
import json
import os
from typing import Dict
from typing import NamedTuple

import requests

class _ENV(NamedTuple):
    HOOK_KEY = os.getenv("HOOK_KEY")
    TARGET_URL = os.getenv("TARGET_URL")
ENV = _ENV()


def get_signing_key()-> bytes:
    hook_key_bytes = ENV.HOOK_KEY.encode("utf-8")
    return base64.b64decode(hook_key_bytes)


def get_request_body()-> Dict:
    key = get_signing_key()
    now_utc = datetime.utcnow().timestamp()
    now_hmac = hmac.new(
        key,
        msg = b"%f" % now_utc,
        digestmod = hashlib.sha256
    )
    now_signed = base64.b64encode(now_hmac.digest()).decode("utf-8")
    return {
        "time_utc": now_utc,
        "time_utc_signed": now_signed,
    }


def main():
    body = get_request_body()
    with requests.Session() as s:
        s.post(ENV.TARGET_URL, data = json.dumps(body))
    return


if __name__ == "__main__":
    main()
