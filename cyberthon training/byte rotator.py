#! /usr/bin/python3

from sys import argv
from ByteRotator import ByteRotator


with open('flag.jpg', 'rb') as f:
    data = ByteRotator(f.read())

with open('flag.jpg.encrypted', 'wb') as f:
    f.write(data.encrypt())
