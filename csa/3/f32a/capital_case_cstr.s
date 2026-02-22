    .data
.org             0x0
buffer:          .byte  '________________________________'
buf_idx:         .word  0
do_capitalize:   .word  1
input_addr:      .word  0x80
output_addr:     .word  0x84
_mask:           .word  0x5F5F0000

    .text
    .org 0x100
_start:
    @p input_addr a!         \ a for input
    @p output_addr b!        \ b for output

    lit 1
    !p do_capitalize

    lit 0
while:
    dup lit -31 +            \ hardcoded counter on T
    if end

    @ lit 0xFF and
    dup lit -10 + if end

    dup lit -32 + if set_flag

    @p do_capitalize
    if lowercase_current_char
    try_capitalize

    lit 0
    !p do_capitalize
    print_char ;

lowercase_current_char:
    try_lowercase
    print_char ;

set_flag:
    lit 1
    !p do_capitalize

print_char:
    dup !b
    a over @p buf_idx a! _or !+ \ it writes word, so i use _or function
    a !p buf_idx a!

    while ;
end:
    drop drop
    halt

\\\\\\\\\\\\\\\\\\\\

_or:
 \ removes the trailing \0\0\0
    @p _mask inv over inv and inv ;

\\\\\\\\\\\\\\\\\\\\

try_lowercase:
    dup lit -65 +
    -if upper_bound_capital_check
    ;
upper_bound_capital_check:
    dup lit 'Z' over inv lit 1 + +
    -if lowercase_capital_ascii
    ;
lowercase_capital_ascii:
    lit 32 +
    ;

\\\\\\\\\\\\\\\\\\\\

try_capitalize:
    dup lit -97 +
    -if upper_bound_lower_check
    ;
upper_bound_lower_check:
    dup lit 'z' over inv lit 1 + +
    -if capitalize_lowercase_ascii
    ;
capitalize_lowercase_ascii:
    lit -32 +
    ;
