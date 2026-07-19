    .data
input_addr:      .word  0x80
output_addr:     .word  0x84
ovrflow_val:     .word  0xCCCCCCCC

; a0 - input ptr
; a1 - output ptr
; t0 - prev sum(X) for total overflow check
; t1 - i = 0..N
; t2 - x, i.e. current number in stream
;      OR sum(X) - x for total overflow check
; t3 - sum(X)
; t4 - sum(x*x for x in X)
;      OR error code
; t5 - x*x, i.e. squared current number in stream
;      OR sum(X) - x for overflow check
; t6 - prev sum(x*x for x in X) for squared_total overflow check

    .text
    .org 0x100
_start:
    lui a0, %hi(input_addr)       / nop               / nop          / nop
    addi a0, a0, %lo(input_addr)  / nop               / nop          / nop
    lui a1, %hi(output_addr)      / nop               / lw a0, 0(a0) / nop
    addi a1, a1, %lo(output_addr) / nop               / lw t1, 0(a0) / nop

    nop                           / nop               / lw a1, 0(a1) / bgt t1, zero, while
    nop                           / nop               / nop          / beqz t1, output
    addi t4, zero, -1             / nop               / nop          / j end

; main cycle
while:
    addi t1, t1, -1               / mv t0, t3         / lw t2, 0(a0) / nop
    add t3, t3, t2                / mul t5, t2, t2    / nop          / blt t5, zero, overflow_while
    sub t2, t3, t2                / mv t6, t4         / nop          / nop
    add t4, t4, t5                / nop               / nop          / bne t2, t0, overflow_while
    sub t5, t4, t5                / nop               / nop          / bne t5, t6, overflow_while
    nop                           / nop               / nop          / bnez t1, while
    nop                           / nop               / nop          / j output

; reading the whole buffer till it empties
overflow_while:
    nop                           / nop               / nop          / beqz t1, overflow_done
    addi t1, t1, -1               / mv t0, t3         / lw t2, 0(a0) / j overflow_while
overflow_done:
    lui t4, %hi(ovrflow_val)      / nop               / nop          / nop
    addi t4, t4, %lo(ovrflow_val) / nop               / nop          / nop
    nop                           / nop               / lw t4, 0(t4) / j end

; outputting results
output:
    nop                           / nop               / sw t3, 0(a1) / nop
end:
    nop                           / nop               / sw t4, 0(a1) / nop
    nop                           / nop               / nop          / halt