    .data
    .org     0x0
memory:          .word  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
ptr:             .word  0

input_addr:      .word  0x80               ; Input device address
output_addr:     .word  0x84               ; Output device address

    .text
    .org     0x100
_start:
    movea.l input_addr, A0                 ; Immediate Addressing
    movea.l (A0), A0                       ; Memory Addressing (Indirect)
while:
    move.l (A0), D0
    cmp.b 10, D0                           ; reading till 'LF' (\n)
    beq end

    move.l D0, (A7)+                       ; weird init of stack???????????????
    jsr func_process_command

    jmp while
end:
    halt

func_process_command:
    rts