import base64
import hashlib
import hmac
import time

from tornado import escape
from tornado.escape import utf8


def create_signed_value(secret, name, value, version=None, clock=None,
                        key_version=None):
    if version is None:
        version = 1
    if clock is None:
        clock = time.time

    timestamp = utf8(str(int(clock())))
    value = base64.b64encode(utf8(value))
    if version == 1:
        signature = create_signature_v1(secret, name, value, timestamp)
        value = b"|".join([value, timestamp, signature])
        return value
    elif version == 2:
        def format_field(s):
            return utf8("%d:" % len(s)) + utf8(s)

        to_sign = b"|".join([
            b"2",
            format_field(str(key_version or 0)),
            format_field(timestamp),
            format_field(name),
            format_field(value),
            b''])

        if isinstance(secret, dict):

          assert key_version is not None, 'Key version must be set when sign key dict is used'
          assert version >= 2, 'Version must be at least 2 for key version support'
          secret = key_version

        signature = create_signature_v2(secret, to_sign)
        return to_sign + signature
    else:
        raise ValueError("Unsupported version %d" % version)


def create_signature_v2(secret, s):
    hash = hmac.new(utf8(secret), digestmod=hashlib.sha256)
    hash.update(utf8(s))
    return utf8(hash.hexdigest())

def create_signature_v1(secret, *parts):
    hash = hmac.new(utf8(secret), digestmod=hashlib.sha1)
    for part in parts:
        hash.update(utf8(part))
    return utf8(hash.hexdigest())


key = 'JDIOtOQQjLXklJT/N4aJE.tmYZ.IoK9M0_IHZW448b6exe7p1pysO'
print escape.native_str(create_signed_value(key, 'username', 'as', version=None,key_version=None))