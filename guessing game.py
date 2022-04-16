from pwn import *

io = remote('jupiter.challenges.picoctf.org', 51462)

for i in range(101):
    io.recvuntil(b'What number would you like to guess?')
    io.sendline(str(i).encode())
    io.interactive()
    print(i)