import hashlib
import hmac


def to_bytes(obj):
    if isinstance(obj, bytes):
        return obj
    return obj.encode('utf-8')


def calc_md5(message):
    md5 = hashlib.md5()
    md5.update(to_bytes(message))
    return md5.hexdigest()


def calc_hmac(key, message):
    return hmac.new(to_bytes(key), to_bytes(message), 'MD5').hexdigest()
