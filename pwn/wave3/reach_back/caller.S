.intel_syntax noprefix

.equ FRAME_SIZE, 0x108
.equ SOLVE_SLOT, 0x18
.equ FD_SLOT, 0x20
.equ READ_RESULT_SLOT, 0x28
.equ FLAG_OFFSET, 0x38
.equ FLAG_SIZE, 0x80

.section .rodata
flag_path:
    .asciz "/flag"
local_flag_path:
    .asciz "./flag"

.section .text
.global caller
.type caller, @function
.extern install_seccomp
.hidden install_seccomp
caller:
    .cfi_startproc
    sub rsp, FRAME_SIZE
    .cfi_def_cfa_offset FRAME_SIZE + 8

    # Preserve the contestant function pointer in our fixed frame.
    mov QWORD PTR [rsp + SOLVE_SLOT], rdi

    # Zero the full flag area so a short flag has deterministic padding.
    lea rdi, [rsp + FLAG_OFFSET]
    xor eax, eax
    mov ecx, FLAG_SIZE / 8
    rep stosq

    # openat(AT_FDCWD, "/flag", O_RDONLY, 0)
    mov eax, 257
    mov edi, -100
    lea rsi, [rip + flag_path]
    xor edx, edx
    xor r10d, r10d
    syscall
    test rax, rax
    jns .flag_opened

    # Development fallback so ./harness ./solve_example.so works locally.
    mov eax, 257
    mov edi, -100
    lea rsi, [rip + local_flag_path]
    xor edx, edx
    xor r10d, r10d
    syscall
    test rax, rax
    js .flag_failed

.flag_opened:
    mov QWORD PTR [rsp + FD_SLOT], rax

    # read(fd, caller_rsp + 0x38, 0x80)
    xor eax, eax
    mov rdi, QWORD PTR [rsp + FD_SLOT]
    lea rsi, [rsp + FLAG_OFFSET]
    mov edx, FLAG_SIZE
    syscall
    mov QWORD PTR [rsp + READ_RESULT_SLOT], rax

    # close(fd) before the seccomp filter is active.
    mov eax, 3
    mov rdi, QWORD PTR [rsp + FD_SLOT]
    syscall

    cmp QWORD PTR [rsp + READ_RESULT_SLOT], 0
    jle .flag_failed

    # rsp is 16-byte aligned at each call site, as required by SysV AMD64.
    call install_seccomp
    test eax, eax
    jne .seccomp_failed

    # call pushes eight bytes. At solve entry:
    #   (caller_rsp + 0x38) - (caller_rsp - 8) == 0x40
    call QWORD PTR [rsp + SOLVE_SLOT]

    xor eax, eax
    jmp .return

.flag_failed:
    mov eax, 1
    jmp .return

.seccomp_failed:
    mov eax, 2

.return:
    add rsp, FRAME_SIZE
    .cfi_def_cfa_offset 8
    ret
    .cfi_endproc
.size caller, .-caller

.section .note.GNU-stack,"",@progbits
