    .data
    .org 0x7
multiple:        .word 0xFFFFFFFF

    .text

_start:
    load_imm     0x7FFFFFFF
    mul          multiple
    halt