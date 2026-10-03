.intel_syntax noprefix

.global solve
.type solve, @function
.section .text
solve:
    lea rsi, [rsp + 0x40]
    mov edi, 1
    mov edx, 0x80
    mov eax, 1
    syscall
    ret
.size solve, .-solve

.section .note.GNU-stack,"",@progbits
