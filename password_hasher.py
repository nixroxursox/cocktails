import nacl.pwhash
import nacl.utils

password = b'11111111'

pw = nacl.pwhash.argon2id.str(password)
print(pw)
