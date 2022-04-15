def repeating_key_xor(text: bytes, key: bytes) -> bytes:
    repetitions = 1 + (len(text) // len(key))
    key = key * repetitions
    key = key[:len(text)]
    return bytes([b ^ k for b, k in zip(text, key)])

with open('secret', 'rb') as f:
    data = f.read()

result = repeating_key_xor(data, b'CSIT')

with open('result', 'wb+') as f:
    f.write(result)
