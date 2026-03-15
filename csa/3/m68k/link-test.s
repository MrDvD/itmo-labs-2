    .data

stack_top:    .word   0x40

    .text
    .org    0x100

_start:
    movea.l   stack_top, A7
    movea.l   (A7), A7

    jsr       func_test

    move.l   0xAAAAAAAA, (A7)

    halt

func_test:
    link     A6, -4

    jsr      func_dummy

    move.l   0xFFFFFFFF, (A6)

    unlk     A6
    rts

func_dummy:
    rts