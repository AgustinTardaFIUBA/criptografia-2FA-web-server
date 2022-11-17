import hashlib
import hmac
import math
import secrets
import time
import threading

def generate_seed():
    return secrets.token_hex(16)

def generate_totp(seed, digits):
    current_time = time.time()
    time_step = 30 # In seconds
    t = math.floor(current_time / time_step)
    h = hmac.new(
        bytes(seed, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha1,
    )
    digest = h.hexdigest()
    return truncate(digest, digits)

def truncate(digest, digits):
    offset = int(digest[-1], 16)
    binary = int(digest[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
    passcode = binary % 10 ** digits
    return str(passcode).zfill(digits) # Pads passcode with 0s if necessary
 
def verify_totp(totp, seed):
    return totp == generate_totp(seed,6)    