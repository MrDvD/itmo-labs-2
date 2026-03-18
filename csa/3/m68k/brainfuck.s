    .data
    .org     0x60
mem_ptr:         .word  0x0
line_ptr:        .word  0x150
hash_ptr:        .word  0x200
line_idx:        .word  0

input_addr:      .word  0x80               ; Input device address
output_addr:     .word  0x84               ; Output device address
stack_top:       .word  0x140              ; Stack top address

    .text
    .org     0x300
_start:
    movea.l   stack_top, A7
    movea.l   (A7), A7                     ; Memory Addressing (Indirect)
    movea.l   input_addr, A0               ; Immediate Addressing
    move.l    (A0), D0
    movea.l   output_addr, A1
    move.l    (A1), D2

    move.l    0, -(A7)                     ; for return code
    movea.l   line_ptr, A1
    move.l    (A1), -(A7)
    move.l    D0, -(A7)                    ; Memory Addressing (Indirect with Predecrement)

    jsr       func_read_line

    link      A1, -16                      ; A7(SP) += 12

    cmp.b     0, -4(A7)
    beq       check_brackets

    movea.l   D2, A1
    move.l    0xCCCCCCCC, (A1)

    jmp       end  

check_brackets:
    move.l    0, -(A7)                     ; for return code
    movea.l   hash_ptr, A1
    move.l    (A1), -(A7)
    movea.l   line_ptr, A1
    move.l    (A1), -(A7)                  ; pass-by value

    jsr       func_validate_brackets

    link      A1, -16                      ; A7(SP) += 12
    cmp.b     0, -4(A7)
    beq       start_processing

    movea.l   D2, A1
    move.l    -1, (A1)

    jmp       end

start_processing:
    movea.l   input_addr, A0
    move.l    (A0), -(A7)
    move.l    D2, -(A7)
    movea.l   line_ptr, A1
    move.l    (A1), -(A7)

    jsr       func_process_all_commands
    link      A1, -20                      ; A7(SP) += 16
end:
    halt

func_read_line:                            ; int read_line(in_ptr, line_ptr) { ... }
    link      A6, 4
    move.l    0, -4(A6)                    ; int line_idx = 0
    move.l    0, 16(A6)                    ; set return code to 0
_while_read:
    cmp.l     64, -4(A6)
    beq       _buffer_overflow

    movea.l   8(A6), A1
    move.l    (A1), D0

    cmp.b     10, D0                       ; reading till 'LF' (\n)
    beq       _end_read

    movea.l   -4(A6), A1                   ; saving to the buffer
    movea.l   12(A6), A2
    move.b    D0, (A1,A2)                     

    add.l     1, -4(A6)

    jmp       _while_read
_buffer_overflow:
    move.l    1, 16(A6)
_end_read:
    unlk      A6
    rts

func_validate_brackets:                    ; bool validate_brackets(line_ptr, hash_ptr)
    link      A6, 8
    move.l    0, -4(A6)                    ; int bracket_count = 0
    move.l    0, -8(A6)                    ; int line_idx = 0
    move.l    0, 16(A6)                    ; set return code to 0
_while_validate:
    move.l    -8(A6), D1
    movea.l   8(A6), A2

    cmp.b     0, (A2,D1)
    beq       _end_validate
    cmp.b     91, (A2,D1)
    beq       _found_opening_bracket
    cmp.b     93, (A2,D1)
    beq       _found_closing_bracket

    jmp       _rest_while
_found_closing_bracket:
    sub.l     1, -4(A6)
    bmi       _error_validate

    movea.l   12(A6), A1
    move.l    D1, D3
    asl.l     2, D1
    move.l    (A7), (A1,D1)
    move.l    (A7), D1
    asl.l     2, D1
    move.l    D3, (A1,D1)
    link      A1, -8

    jmp       _rest_while
_found_opening_bracket:
    add.l     1, -4(A6)

    move.l    D1, -(A7)
_rest_while:
    add.l     1, -8(A6)                    ; line_idx++
    jmp       _while_validate
_error_validate:
    move.l    1, 16(A6)
    unlk      A6
    rts
_end_validate:
    cmp.l     0, -4(A6)
    bne       _error_validate
    unlk      A6
    rts

func_process_all_commands:                 ; void process_all_commands(line_ptr, out_ptr, in_ptr)
    link      A6, 0
    movea.l   line_idx, A5
_while_process:
    move.l    0, -(A7)                     ; for return code
    move.l    8(A6), -(A7)
    move.l    16(A6), -(A7)
    move.l    12(A6), -(A7)
    movea.l   (A5), A1
    movea.l   8(A6), A2
    move.l    (A1,A2), -(A7)

    jsr       func_process_command

    link      A1, -24                      ; A7(SP) += 20
    cmp.b     0, -4(A7)
    bne       _end_process_all

    add.l     1, (A5)

    jmp       _while_process
_end_process_all:
    cmp.b     1, -4(A7)
    beq       _ignore_error_code

    movea.l   12(A6), A1
    move.l    -4(A7), (A1)
_ignore_error_code:
    unlk      A6
    rts

func_process_command:                      ; int process_command(cmd, out_ptr, in_ptr, line_ptr) { ... }
    move.l    0, 20(A7)                    ; set return code to 0

    cmp.b     43, 4(A7)                    ; char == '+'
    bne       _command_not_inc_val

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    add.l     1, (A1)

    bvs       _overflow_error

    rts
_command_not_inc_val:
    cmp.b     45, 4(A7)                    ; char == '-'
    bne       _command_not_dec_val

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    sub.l     1, (A1)

    bvs       _overflow_error

    rts
_command_not_dec_val:
    cmp.b     62, 4(A7)                    ; char == '>'
    bne       _command_not_inc_ptr

    movea.l   mem_ptr, A1
    add.l     4, (A1)

    cmp.l     120, (A1)
    bge       _out_of_bounds_error

    rts
_command_not_inc_ptr:
    cmp.b     60, 4(A7)                    ; char == '<'
    bne       _command_not_dec_ptr

    movea.l   mem_ptr, A1
    sub.l     4, (A1)

    cmp.l     0, (A1)
    blt       _out_of_bounds_error

    rts
_command_not_dec_ptr:
    cmp.b     93, 4(A7)                    ; char == ']'
    bne       _command_not_jump_back

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    move.l    (A1), D0

    cmp.l     0, D0
    bne       _continue_jump_back
    rts

_continue_jump_back:
    movea.l   line_idx, A2
    move.l    (A2), D0
    asl.l     2, D0
    movea.l   hash_ptr, A1
    movea.l   (A1), A1
    move.l    (A1,D0), (A2)
    rts
_command_not_jump_back:
    cmp.b     91, 4(A7)                    ; char == '['
    bne       _command_not_jump_forward

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    move.l    (A1), D0

    cmp.l     0, D0
    beq       _continue_jump_forward
    rts

_continue_jump_forward:
    movea.l   line_idx, A2
    move.l    (A2), D0
    asl.l     2, D0
    movea.l   hash_ptr, A1
    movea.l   (A1), A1
    move.l    (A1,D0), (A2)
    rts
_command_not_jump_forward:
    cmp.b     46, 4(A7)                    ; char == '.'
    bne       _command_not_output

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    move.b    (A1), D0
    
    movea.l   8(A7), A1                    ; this loads 0x16
    move.b    D0, (A1)

    rts
_command_not_output:
    cmp.b     44, 4(A7)                    ; char == ','
    bne       _command_not_input

    movea.l   mem_ptr, A1
    movea.l   (A1), A1

    movea.l   12(A7), A2
    move.b    (A2), (A1)

    rts
_command_not_input:
    cmp.b     0, 4(A7)
    bne       _out_of_bounds_error

    move.l    1, 20(A7)
    rts
_overflow_error:
    move.l    0xCC, 20(A7)
    rts
_out_of_bounds_error:
    move.l    -1, 20(A7)
    rts