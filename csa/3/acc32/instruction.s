    .data
    .org 0x7
answer:          .word  0xDEADBEEF
fool:            .word  0xF00DD00F
    .org 0x5F
addr:            .word  0x7

    .text

_start:
    load_addr    addr
    store        10
    load_addr    fool
    halt