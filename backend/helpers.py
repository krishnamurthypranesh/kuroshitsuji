import hashlib
import random
import time
from datetime import datetime, timezone
from typing import Optional

import ksuid
from kuroshitsuji import settings


def get_current_datetime():
    return datetime.now().astimezone(timezone.utc)


def get_current_date():
    return datetime.utcnow().date()


def generate_id(prefix: Optional[str] = None):
    _id = str(ksuid.Ksuid())
    if prefix:
        return f"{prefix}_{_id}"
    return _id


# this is copied from: https://www.hacksplaining.com/prevention/weak-session
# I didn't want to use ksuid's (because brute forcing is fairly easy)
# and uuids for their (probable) low entropy
# this seemed like a good alternative (based on what I read online and my minimal understanding of cryptography)
# TODO: revisit this when there's more time
def generate_session_id():
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    length = 64
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # This is ugly, and a hack, but it makes things better than
    # the alternative of predictability. This re-seeds the PRNG
    # using a value that is hard for an attacker to predict, every
    # time a random string is required. This may change the
    # properties of the chosen random sequence slightly, but this
    # is better than absolute predictability.
    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (random.getstate(), time.time(), settings.SECRET_KEY)).encode(
                "utf-8"
            )
        ).digest()
    )
    return "".join(random.choice(allowed_chars) for i in range(length))
