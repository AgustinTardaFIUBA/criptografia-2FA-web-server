import hashlib
import hmac
import math
import secrets
import time
import sys
import threading

def generate_seed():
    #RANDOM SEED
    return secrets.token_hex(16)

def generate_totp(seed, digits):
    # The current time must be hashed together with the shared key to make the passcode constantly change the hash digest.

    # TIMESTAMP
    current_time = time.time()
    # 30 seconds are given to the user to enter the passcode.
    time_step = 30 # In seconds
    t = math.floor(current_time / time_step)

    # HMAC
    # The hash digest is calculated using the HMAC-SHA1 algorithm.
    h = hmac.new(
        bytes(seed, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha1,
    )


    digest = h.hexdigest()
    return truncate(digest, digits), (time_step - (current_time % time_step))

def generateTotpForTime(seed, digits,time):
    # The current time must be hashed together with the shared key to make the passcode constantly change the hash digest.

    # 30 seconds are given to the user to enter the passcode.
    time_step = 30 # In seconds
    t = math.floor(time / time_step)

    # HMAC
    # The hash digest is calculated using the HMAC-SHA1 algorithm.
    h = hmac.new(
        bytes(seed, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha1,
    )


    digest = h.hexdigest()
    return truncate(digest, digits), (time_step - (time % time_step))

def generateTotpsForFiveMinutes(seed, digits):
    totps = []
    current_time = time.time()
    for i in range(0,10):
        totp, t = generateTotpForTime(seed, digits, current_time + (i * 30))
        totps.append({"totp": totp, "time": t + (i * 30)})
    return {"tokens": totp, "startinTime":current_time}

def truncate(digest, digits):
    # Dynamic Truncation
    offset = int(digest[-1], 16)
    binary = int(digest[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff

    # Passcode Decimal Conversion of "digits" length
    passcode = binary % 10 ** digits
    print(passcode)
    return str(passcode).zfill(digits) # Pads passcode with 0s if necessary
 
def verify_totp(totp, seed):
    a, b = generate_totp(seed,6)   
    return totp == a
