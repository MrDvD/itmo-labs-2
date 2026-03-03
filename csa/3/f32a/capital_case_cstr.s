    .data
.org             0x0
buffer:          .byte  '________________________________'
buf_idx:         .word  0
do_capitalize:   .word  1
input_addr:      .word  0x80
output_addr:     .word  0x84

    .text
    .org 0x100
_start:
    @p buf_idx a!            \ 'a' for filling a buffer
    @p input_addr b!         \ 'b' for input

    lit 1 !p do_capitalize

    lit 0 a!
while:
    a lit -32 +
    if handle_buffer_overflow

    @b lit 0xFF and
    dup lit -10 + if end

    dup lit -32 + if set_flag

    @p do_capitalize
    if lowercase_current_char
    func_try_capitalize

    lit 0
    !p do_capitalize
    print_char_to_buffer ;

lowercase_current_char:
    func_try_lowercase
    print_char_to_buffer ;

set_flag:
    lit 1
    !p do_capitalize

print_char_to_buffer:
    lit 0x5F5F0000 inv over inv and inv \ removes the trailing \0\0\0 (as it writes a whole word)
    !+

    while ;
end:
    func_print_the_buffer
    drop drop                \ clean the stack
    halt

handle_buffer_overflow:
    lit 0 a!
_while_overflow:
    a lit -32 + if _end_rest
    lit 0xCC !+
    _while_overflow ;
_end_rest:
    @p output_addr b!
    lit 0xCCCCCCCC !b
    halt

func_try_lowercase:
    dup lit -65 +
    -if _upper_bound_capital_check
    ;
_upper_bound_capital_check:
    dup lit 'Z' over inv lit 1 + +
    -if _lowercase_capital_ascii
    ;
_lowercase_capital_ascii:
    lit 32 +
    ;

func_try_capitalize:
    dup lit -97 +
    -if _upper_bound_lower_check
    ;
_upper_bound_lower_check:
    dup lit 'z' over inv lit 1 + +
    -if _capitalize_lowercase_ascii
    ;
_capitalize_lowercase_ascii:
    lit -32 +
    ;

func_print_the_buffer:
    @p output_addr b!

    lit 0 a!
_while_print:
    a lit -32 + if _stop_print

    @+ lit 0xFF and
    dup if _stop_print
    !b

    _while_print ;
_stop_print:
    ;
