    .data
    .org     0x100
mem_ptr:         .word  0x0
line_ptr:        .word  0x40

input_addr:      .word  0x80               ; Input device address
output_addr:     .word  0x84               ; Output device address
stack_top:       .word  0x100              ; Stack top address

    .text
    .org     0x200
_start:
    movea.l   stack_top, A7
    movea.l   (A7), A7                     ; Memory Addressing (Indirect)
    movea.l   input_addr, A0               ; Immediate Addressing
    move.l    (A0), D0
    movea.l   output_addr, A2
    movea.l   (A2), A2

    move.l    0, -(A7)                     ; for return code
    movea.l   line_ptr, A1
    move.l    (A1), -(A7)
    move.l    D0, -(A7)                    ; Memory Addressing (Indirect with Predecrement)

    jsr       func_read_line

    link      A1, -16                      ; A7(SP) += 12

    halt

    cmp.b     0, -4(A7)
    beq       start_interpretation

    movea.l   (A2), A2
    move.l    0xCC, (A2)

    jmp       end       

start_interpretation:
    move.l    0, -(A7)
    movea.l   mem_ptr, A1
    move.l    (A1), -(A7)

    jsr       func_validate_brackets

    halt

    link      A1, -12
    cmp.b     0, -4(A7)
    beq       while

    movea.l   (A2), A2
    move.l    -1, (A2)

    jmp       end

while:
    move.l    (A0), D0
    cmp.b     10, D0                       ; reading till 'LF' (\n)
    beq       end

    move.l    A0, -(A7)
    move.l    (A2), -(A7)
    move.l    D0, -(A7)

    jsr       func_process_command

    move.l    A7, D0
    add.l     12, D0
    movea.l   D0, A7

    cmp.b     0, -8(A7)
    bne       end

    jmp       while
end:
    halt

func_read_line:                            ; int read_line(in_ptr, line_ptr) { ... }
    link      A6, 0
    move.l    0, (A6)                      ; int line_idx = 0
    move.l    0, 12(A7)                    ; set return code to 0
_while_read:
    cmp.l     32, (A6)
    beq       _overflow_read

    movea.l   8(A6), A1
    move.l    (A1), D0

    cmp.b     10, D0                       ; reading till 'LF' (\n)
    beq       _end_read

    ; move.l    (A6), D1                     ; don't work as expected (0x0+0x40=0x0)
    ; movea.l   12(A6), A1
    ; movea.l   0(A1,D1), A1
    move.l    (A6), D1                     ; saving to the buffer
    add.l     12(A6), D1
    movea.l   D1, A1
    move.b    D0, (A1)                     

    add.l     1, (A6)

    jmp       _while_read
_overflow_read:
    move.l    0xCC, 12(A7)                 ; update return code
_end_read:
    unlk      A6
    rts

func_validate_brackets:                    ; bool validate_brackets(line_ptr)
    link      A6, 4
    move.l    0, (A6)                      ; int bracket_count = 0
    move.l    0, -4(A6)                    ; int line_idx = 0
    move.l    0, 12(A6)
_while_validate:
    cmp.l     32, -4(A6)
    beq       _end_validate

    move.l    -4(A6), D0
    cmp.l     83, 8(A6,D0)
    beq       _found_opening_bracket
    cmp.l     85, 8(A6,D0)
    beq       _found_closing_bracket

    jmp       _rest_while
_found_closing_bracket:
    add.l     -1, (A6)
    bmi       _error_validate
    jmp       _rest_while
_found_opening_bracket:
    add.l     1, (A6)
_rest_while:
    add.l     1, -4(A6)                    ; line_idx++
    jmp       _while_validate
_error_validate:
    move.l    1, 8(A7)
    unlk      A6
    rts
_end_validate:
    cmp.l     0, (A6)
    bne       _error_validate
    unlk      A6
    rts

func_process_command:                      ; bool process_command(cmd, out_ptr, mem_ptr) { ... }
    link      A6, 8

    cmp.b     50, (A6)
    bne       _command_not_inc_ptr

    movea.l   -8(A6), A1

    cmp.l     29, (A1)
    bge       _out_of_bounds_error

    add.l     1, (A1)

    jmp       _end_process
_command_not_inc_ptr:
    cmp.b     48, D0
    bne       _command_not_dec_ptr

    movea.l   -8(A6), A1

    cmp.l     1, (A1)
    blt       _out_of_bounds_error

    add.l     -1, (A1)

    jmp       _end_process
_command_not_dec_ptr:
    jmp       _end_process
_out_of_bounds_error:
    movea.l   -4(A6), A1                   ; Memory Addressing (Indirect with Displacement)
    move.b    -1, (A1)
    jmp       _end_process

_end_process:
    unlk      A6 
    rts