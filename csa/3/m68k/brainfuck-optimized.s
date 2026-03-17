    .data
    .org     0x60
mem_ptr:         .word  0x0
line_ptr:        .word  0x150

input_addr:      .word  0x80               ; Input device address
output_addr:     .word  0x84               ; Output device address
stack_top:       .word  0x120              ; Stack top address

    .text
    .org     0x200
_start:
    movea.l   stack_top, A7
    movea.l   (A7), A7                     ; Memory Addressing (Indirect)

    move.l    0, -(A7)                     ; for return code
    jsr       func_read_line
    link      A1, -8                       ; A7(SP) += 4

    cmp.b     0, -4(A7)
    beq       check_brackets

    movea.l   output_addr, A1
    movea.l   (A1), A1
    move.l    0xCC, (A1)

    jmp       end
check_brackets:
    move.l    0, -(A7)                     ; for return code
    jsr       func_validate_brackets
    link      A1, -8                       ; A7(SP) += 4

    cmp.b     0, -4(A7)
    beq       start_processing

    movea.l   output_addr, A1
    movea.l   (A1), A1
    move.l    -1, (A1)

    jmp       end
start_processing:
    jsr       func_process_all_commands
end:
    halt

func_read_line:                            ; int read_line() { ... }
    link      A6, 0
    move.l    0, (A6)                      ; int line_idx = 0
    move.l    0, 8(A6)                     ; set return code to 0

    movea.l   input_addr, A2
    movea.l   (A2), A2
    movea.l   line_ptr, A3
_while_read:
    move.l    (A2), D0

    cmp.b     10, D0                       ; reading till 'LF' (\n)
    beq       _end_read

    move.l    (A6), D1                     ; saving to the buffer
    add.l     (A3), D1
    movea.l   D1, A1

    move.b    D0, (A1)                     

    add.l     1, (A6)

    jmp       _while_read
_end_read:
    unlk      A6
    rts

func_validate_brackets:                    ; bool validate_brackets()
    link      A6, 4
    move.l    0, (A6)                      ; int bracket_count = 0
    move.l    0, -4(A6)                    ; int line_idx = 0
    move.l    0, 8(A6)                     ; set return code to 0
    movea.l   line_ptr, A2
_while_validate:
    move.l    -4(A6), D0
    add.l     (A2), D0
    movea.l   D0, A1

    cmp.b     0, (A1)
    beq       _end_validate
    cmp.b     83, (A1)
    beq       _found_opening_bracket
    cmp.b     85, (A1)
    beq       _found_closing_bracket

    jmp       _rest_while
_found_closing_bracket:
    sub.l     1, (A6)
    bmi       _error_validate
    jmp       _rest_while
_found_opening_bracket:
    add.l     1, (A6)
_rest_while:
    add.l     1, -4(A6)                    ; line_idx++
    jmp       _while_validate
_error_validate:
    move.l    1, 8(A6)
    unlk      A6
    rts
_end_validate:
    cmp.l     0, (A6)
    bne       _error_validate
    unlk      A6
    rts

func_process_all_commands:                 ; void process_all_commands()
    link      A6, 0
    move.l    0, (A6)                      ; int line_idx = 0
    movea.l   line_ptr, A3
    movea.l   (A3), A3
_while_process:
    move.l    0, -(A7)                     ; for return code
    move.l    0, -(A7)                     ; for return idx
    move.l    (A6), -(A7)
    movea.l   (A6), A1
    move.l    (A1,A3), -(A7)
    jsr       func_process_command
    link      A1, -20                      ; A7(SP) += 16

    move.l    -8(A7), (A6)
    cmp.b     0, -4(A7)
    bne       _end_process_all

    add.l     1, (A6)

    jmp       _while_process
_end_process_all:
    cmp.b     1, -4(A7)
    beq       _ignore_error_code

    movea.l   output_addr, A1
    movea.l   (A1), A1
    move.l    -4(A7), (A1)
_ignore_error_code:
    unlk      A6
    rts

func_process_command:                      ; struct { int idx, int exit_code; } process_command(cmd, line_idx) { ... }
    move.l    8(A7), 12(A7)                ; set return idx to line_idx
    move.l    0, 16(A7)                    ; set return code to 0
    cmp.b     0, 4(A7)
    bne       _command_not_null

    move.l    1, 16(A7)

    jmp       _end_process
_command_not_null:
    cmp.b     62, 4(A7)                    ; char == '>'
    bne       _command_not_inc_ptr

    movea.l   mem_ptr, A1
    add.l     1, (A1)

    cmp.l     30, (A1)
    bge       _out_of_bounds_error

    jmp       _end_process
_command_not_inc_ptr:
    cmp.b     60, 4(A7)                    ; char == '<'
    bne       _command_not_dec_ptr

    movea.l   mem_ptr, A1
    sub.l     1, (A1)

    cmp.l     0, (A1)
    blt       _out_of_bounds_error

    jmp       _end_process
_command_not_dec_ptr:
    cmp.b     43, 4(A7)                    ; char == '+'
    bne       _command_not_inc_val

    movea.l   mem_ptr, A1
    movea.l   (A1), A1                     ; dereferencing *mem_ptr
    add.l     1, (A1)

    bvs       _overflow_error

    jmp       _end_process
_command_not_inc_val:
    cmp.b     45, 4(A7)                    ; char == '-'
    bne       _command_not_dec_val

    movea.l   mem_ptr, A1
    movea.l   (A1), A1                     ; dereferencing *mem_ptr
    sub.l     1, (A1)

    bvs       _overflow_error

    jmp       _end_process
_command_not_dec_val:
    cmp.b     46, 4(A7)                    ; char == '.'
    bne       _command_not_output

    movea.l   mem_ptr, A1
    movea.l   (A1), A1
    move.l    (A1), D0
    
    movea.l   output_addr, A1
    movea.l   (A1), A1
    move.b    D0, (A1)

    jmp       _end_process
_command_not_output:
    cmp.b     44, 4(A7)                    ; char == ','
    bne       _command_not_input

    movea.l   input_addr, A1
    movea.l   (A1), A1

    movea.l   mem_ptr, A2
    movea.l   (A2), A2
    move.b    (A1), (A2)

    jmp       _end_process
_command_not_input:
    cmp.b     91, 4(A7)                    ; char == '['
    bne       _command_not_jump_forward

    movea.l   16(A7), A1
    movea.l   (A1), A1
    move.l    (A1), D0

    cmp.l     0, D0
    bne       _skip_jump_forward

    link      A6, 0
    move.l    1, (A6)                      ; int bracket_count = 1
    move.l    24(A6), D0
_while_jump_forward:
    add.l     1, D0
    
    move.l    D0, D1
    add.l     24(A6), D1
    movea.l   D1, A1

    move.b    (A1), D1
    cmp.b     91, D1
    bne       _jump_forward_not_open_br

    add.l     1, (A6)

    jmp       _check_bracket_count_forward
_jump_forward_not_open_br:
    cmp.b     93, D1
    bne       _while_jump_forward

    sub.l     1, (A6)
_check_bracket_count_forward:
    cmp.l     0, (A6)
    beq       _exit_jump_forward
    jmp       _while_jump_forward
_exit_jump_forward:
    unlk      A6

    move.l    D0, 24(A7)
_skip_jump_forward:
    jmp       _end_process
_command_not_jump_forward:
    cmp.b     93, 4(A7)                    ; char == ']'
    bne       _out_of_bounds_error

    movea.l   16(A7), A1
    movea.l   (A1), A1
    move.l    (A1), D0

    cmp.l     0, D0
    beq       _skip_jump_back

    link      A6, 0
    move.l    1, (A6)                      ; int bracket_count = 1
    move.l    24(A6), D0
_while_jump_back:
    sub.l     1, D0
    
    move.l    D0, D1
    add.l     24(A6), D1
    movea.l   D1, A1

    move.b    (A1), D1
    cmp.b     91, D1
    bne       _jump_back_not_open_br

    sub.l     1, (A6)

    jmp       _check_bracket_count_back
_jump_back_not_open_br:
    cmp.b     93, D1
    bne       _while_jump_back

    add.l     1, (A6)
_check_bracket_count_back:
    cmp.l     0, (A6)
    beq       _exit_jump_back
    jmp       _while_jump_back
_exit_jump_back:
    unlk      A6

    move.l    D0, 24(A7)
_skip_jump_back:
    jmp       _end_process
_overflow_error:
    move.l    0xCC, 16(A7)
    jmp       _end_process
_out_of_bounds_error:
    move.l    -1, 16(A7)
    jmp       _end_process
_end_process:
    rts