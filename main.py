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
    ACTION = os.getenv("ACTION")
ENV = _ENV()


def get_signing_key()-> bytes:
    hook_key_bytes = ENV.HOOK_KEY.encode("utf-8")
    return base64.b64decode(hook_key_bytes)


def get_request_body()-> Dict:
    key = get_signing_key()
    now = datetime.now().timestamp()
    payload = {
        "req_ts": now,
        "action": ENV.ACTION,
    }
    payload_s = json.dumps(payload)
    payload_hmac = hmac.new(key, digestmod = hashlib.sha256)
    payload_hmac.update(payload_s.encode("utf-8"))
    payload_signed = payload_hmac.digest()
    payload_signed_b64 = base64.b64encode(payload_signed) \
                               .decode("utf-8")
    return {
        "digest_algo": "SHA256",
        "payload": payload_s,
        "payload_signed_b64": payload_signed_b64,
    }


def main():
    body = get_request_body()
    with requests.Session() as s:
        s.post(ENV.TARGET_URL, data = json.dumps(body))
    return


if __name__ == "__main__":
    main()
