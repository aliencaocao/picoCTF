num = [14, 16, 5, 7, 8, 13, 19, 1, 11, 18, 0, 10, 15, 4, 6, 12, 9, 2, 3, 17]
strings = 'this is not the flag'
strings_no = [ord(x) for x in strings]


def check(string):
    for i in range(20):
        target = strings_no[i] + 5
        if ord(string[num[i]]) != target:  # target is int
            return False
    return True


def solve():
    ans = [None] * (max(num) + 1)
    for i in range(20):
        target = strings_no[i] + 5
        # print(num[i])
        ans[num[i]] = chr(target)
    return ans


ans = solve()
print(''.join(ans))

"""
Assembly code:

checkFlag(char*):
        push    rbx
        sub     rsp, 112
        mov     rbx, rdi
        movabs  rax, 2338328219631577204
        movabs  rdx, 2334386829831466862
        mov     QWORD PTR [rsp+80], rax
        mov     QWORD PTR [rsp+88], rdx
        mov     DWORD PTR [rsp+96], 1734437990
        mov     BYTE PTR [rsp+100], 0
        mov     DWORD PTR [rsp], 14
        mov     DWORD PTR [rsp+4], 16
        mov     DWORD PTR [rsp+8], 5
        mov     DWORD PTR [rsp+12], 7
        mov     DWORD PTR [rsp+16], 8
        mov     DWORD PTR [rsp+20], 13
        mov     DWORD PTR [rsp+24], 19
        mov     DWORD PTR [rsp+28], 1
        mov     DWORD PTR [rsp+32], 11
        mov     DWORD PTR [rsp+36], 18
        mov     DWORD PTR [rsp+40], 0
        mov     DWORD PTR [rsp+44], 10
        mov     DWORD PTR [rsp+48], 15
        mov     DWORD PTR [rsp+52], 4
        mov     DWORD PTR [rsp+56], 6
        mov     DWORD PTR [rsp+60], 12
        mov     DWORD PTR [rsp+64], 9
        mov     DWORD PTR [rsp+68], 2
        mov     DWORD PTR [rsp+72], 3
        mov     DWORD PTR [rsp+76], 17
        lea     rdi, [rsp+80]
        call    strlen
        mov     edx, 0
.L2:
        cmp     rax, rdx
        je      .L7
        movsx   rsi, DWORD PTR [rsp+rdx*4]
        movzx   edi, BYTE PTR [rsp+80+rdx]
        lea     ecx, [rdi+5]
        add     rdx, 1
        cmp     BYTE PTR [rbx+rsi], cl
        je      .L2
        mov     eax, 0
        jmp     .L1
.L7:
        mov     eax, 1
.L1:
        add     rsp, 112
        pop     rbx
        ret
.LC0:
        .string "%s"
.LC1:
        .string "Correct flag"
main:
        sub     rsp, 40
        mov     rsi, rsp
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    __isoc99_scanf
        mov     rdi, rsp
        call    checkFlag(char*)
        test    eax, eax
        jne     .L11
.L9:
        mov     eax, 0
        add     rsp, 40
        ret
.L11:
        mov     edi, OFFSET FLAT:.LC1
        call    puts
        jmp     .L9
"""