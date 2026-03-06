    .data
    .org 0x7
multiple:        .word 0

    .text

_start:
    load_imm     0x7FFFFFFF
    div          multiple
    halt