from pwn import *

context.binary = elf = ELF('./fried-clams')
context.log_level = 'debug'
io = remote('tjc.tf', 31413)

payload = b''  # get yummy
io.send(payload)
io.interactive()