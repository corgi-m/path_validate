import hashlib
import hmac


def calc_md5(message):
    md5 = hashlib.md5()
    md5.update(message.encode('utf-8'))
    return md5.hexdigest()


def calc_hmac(key, message):
    return hmac.new(key, message.encode('utf-8'), 'MD5').hexdigest()
