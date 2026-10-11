import hashlib
import hmac
import os


def verify_password(password: str) -> bool:
    stored = os.environ.get("DASHBOARD_PASSWORD_HASH", "")

    try:
        algorithm, iterations, salt, expected = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations),
        )

        return hmac.compare_digest(actual, bytes.fromhex(expected))
    except (ValueError, TypeError, OverflowError):
        return False
