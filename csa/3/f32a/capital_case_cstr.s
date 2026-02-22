    .data

do_capitalize:   .word  1
input_addr:      .word  0x80
output_addr:     .word  0x84

    .text
.org 0x200
_start:
    @p input_addr a!         \ a for input
    @p output_addr b!        \ b for output

    lit 1
    !p do_capitalize
    
    lit 0x20                 \ hardcoded counter on T
while:
    dup
    if end

    @ lit 0xFF and
    dup lit -10 + if end

    dup lit -32 + if set_flag

    @p do_capitalize
    if print_char
    try_capitalize

    lit 1
    !p do_capitalize
    print_char ;

set_flag:
    lit 1
    !p do_capitalize
    
print_char:
    !b

    lit -1 +
    while ;
end:
    halt

try_capitalize:
    dup lit -97 +
    -if upper_bound_check
    ;
upper_bound_check:
    dup lit -122 +
    -if capitalize_lowercase_ascii
    ;
capitalize_lowercase_ascii:
    lit -32 +
    ;