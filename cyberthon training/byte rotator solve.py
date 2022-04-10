with open('flag.jpg.encrypted', 'rb') as f:
    data = f.read()

for key in range(1, 257):
    encrypted= bytes([(byte + key) % 256 for byte in data])
    if encrypted.hex().startswith('ffd8'):
        with open('flag.jpg', 'wb') as f:
            f.write(encrypted)
        print(key)
        break