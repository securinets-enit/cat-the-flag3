; ---------------------------------------------------------------------------
; check.asm - the real flag-check logic, written AS bytecode for the LayerUp VM.
;
; Two running accumulators (A and B) over the WHOLE input in a single pass.
; Each round feeds the HIGH bits of A (a lossy, information-destroying
; truncation) into B, and the verdict requires BOTH accumulators to match
; their targets at the very end:
;
;     A = BASIS_A
;     B = BASIS_B
;     for i in 0 .. len-1:
;         A = A XOR input[i]
;         A = rotate_left(A, R1)
;         A = A * MULT_A            (mod 2^32, MULT_A odd -> bijective in A)
;         A = A + i
;         t = A >> SHIFT            ; LOSSY: only the high bits of A survive
;         B = B + t * MULT_B
;         B = rotate_left(B, R2)
;         B = B XOR input[i]
;     verdict = (A == TARGET_A) AND (B == TARGET_B)
;
; There are NO per-byte comparisons. The A >> SHIFT truncation means the chain
; cannot be cleanly inverted backwards, and the two coupled targets cannot be
; satisfied independently - recovering the input needs a solver (e.g. Z3), not
; mechanical back-stepping. TARGET_A / TARGET_B are computed by the assembler
; from the .target flag below.
;
; Variable slots:  v0 = A,  v1 = B,  v2 = i,  v3 = current input byte
; ---------------------------------------------------------------------------

; --- mixing parameters (arbitrary, non-recognizable constants) ------------
.def BASIS_A 0x7E4A1C3B
.def BASIS_B 0x2D5F8E11
.def MULT_A  0xA3C59AC3        ; odd  -> bijective multiply in A
.def MULT_B  0xCF1BBCDD        ; odd
.def R1      11
.def R2      7
.def SHIFT   16

.target SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}

; --- init -----------------------------------------------------------------
    PUSH BASIS_A
    STOREV 0                 ; A = BASIS_A
    PUSH BASIS_B
    STOREV 1                 ; B = BASIS_B
    PUSH 0
    STOREV 2                 ; i = 0

; --- loop condition:  while i != len -------------------------------------
loop_cond:
    LOADV 2                  ; i
    LEN                      ; len
    CMP_EQ                   ; (i == len) ? 1 : 0
    JZ loop_body             ; if not equal (0) -> run the body
    JMP loop_end             ; else done

; --- loop body ------------------------------------------------------------
loop_body:
    LOADV 2                  ; i
    LOAD                     ; input[i]
    STOREV 3                 ; b = input[i]

    ; A = ((rol(A ^ b, R1)) * MULT_A) + i
    LOADV 0                  ; A
    LOADV 3                  ; b
    XOR                      ; A ^ b
    PUSH R1
    ROL                      ; rol(A ^ b, R1)
    PUSH MULT_A
    MUL                      ; * MULT_A
    LOADV 2
    ADD                      ; + i
    STOREV 0                 ; A = ...

    ; B = rol(B + (A >> SHIFT) * MULT_B, R2) ^ b
    LOADV 0                  ; A
    PUSH SHIFT
    SHR                      ; t = A >> SHIFT   (lossy)
    PUSH MULT_B
    MUL                      ; t * MULT_B
    LOADV 1
    ADD                      ; B + t*MULT_B
    PUSH R2
    ROL                      ; rol(..., R2)
    LOADV 3
    XOR                      ; ^ b
    STOREV 1                 ; B = ...

    ; i++
    LOADV 2
    PUSH 1
    ADD
    STOREV 2
    JMP loop_cond

; --- final verdict:  (A == TARGET_A) AND (B == TARGET_B) -----------------
loop_end:
    LOADV 0                  ; A
    PUSH TARGET_A
    CMP_EQ                   ; A == TARGET_A ?
    LOADV 1                  ; B
    PUSH TARGET_B
    CMP_EQ                   ; B == TARGET_B ?
    MUL                      ; 1 only if BOTH are 1
    HALT                     ; consumes top of stack as the verdict
