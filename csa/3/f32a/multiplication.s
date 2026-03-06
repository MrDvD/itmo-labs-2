    .data

counter:      .word   31

    .text

_start:
    lit -57
    lit 135
    a!
    lit 0
while:
    @p counter lit -1 + !p counter
    +*
    @p counter
    -if while
    halt