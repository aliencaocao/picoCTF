#! /usr/bin/python3

from random import randint


class ByteRotator():

    def __init__(self, data):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if type(value) != bytes:
            raise TypeError('\'data\' must be of type \'bytes\'')
        self._data = value

    def encrypt(self):
        return self.__rotate(self.data, randint(1, 0xff + 1))

    def decrypt(self):
        # Implement this
        raise NotImplementedError('\'decrypt\' has not been implemented')

    def __rotate(self, data, key):
        return bytes([(byte + key) % 256 for byte in data])
