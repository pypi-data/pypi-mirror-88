def make_sign( secret):
    import time
    import hmac
    import hashlib
    import base64
    import urllib
    # if isinstance(secret, unicode):
    #     secret = secret.encode('utf-8')
    timestamp = long(round(time.time() * 1000))
    secret_enc = bytes(secret).encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.quote_plus(base64.b64encode(hmac_code))
    params = {
        'sign': sign,
        'timestamp': timestamp
    }
    return params

a = make_sign('asdfsaf')
print a