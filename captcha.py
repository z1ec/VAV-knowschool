import json
import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)


def verify_captcha(token, ip):
    secret = os.environ.get("CAPTCHA_SECRET_KEY")
    if not secret:
        return True

    try:
        data = urllib.parse.urlencode({"secret": secret, "token": token, "ip": ip}).encode()
        with urllib.request.urlopen(
            "https://smartcaptcha.yandexcloud.net/validate", data=data, timeout=5
        ) as response:
            return json.load(response).get("status") == "ok"
    except Exception:
        logger.exception("SmartCaptcha verification request failed")
        return False
