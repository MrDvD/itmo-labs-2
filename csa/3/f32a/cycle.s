    .data

n:      .word  18
number: .word  0xDEADBEEF

    .text
_start:
    lit 1 eam

    @p number

    dup
    +
    dup
    >r
    here ;

    .org 0x50

here:
    halt

\ commands which don't change Carry flag:
\ dup, r>, a!, b!, !b, !p <address>, !, !+, <label> ;