import random

from Crypto.Cipher import AES

key = random.randbytes(32)
aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
data = b'The secret I want to send.'
print(data)
cipher = aes.encrypt(data)
print(cipher)
#nonce = random.randbytes(16)
aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
ans = aes.decrypt(cipher)
print(ans)

