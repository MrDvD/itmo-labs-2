    .data

input_addr:      .word  0x80
output_addr:     .word  0x84
do_capitalize:   .word  0x82 \ why i can't put there 1?

    .text

try_capitalize:
    dup lit 'a' inv lit 1 + +
    -if upper_bound_check
    ;
upper_bound_check:
    dup lit 'z' over inv lit 1 + +
    -if capitalize_lowercase_ascii
    ;
capitalize_lowercase_ascii:
    lit -32 +
    ;

_start:
    @p input_addr a!         \ a for input
    @p output_addr b!        \ b for output

    lit 1
    !p do_capitalize
    
    lit 0x20                 \ hardcoded counter on T
while:
    dup
    if end

    @ lit 255 and
    dup lit ' ' inv lit 1 + + \ input != ' '
    if set_flag

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
