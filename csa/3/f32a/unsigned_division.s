    .data

counter:      .word   31
divisor:      .word   0

    .text

_start:
    lit 135
    a!
    lit 0
    !p divisor
    lit divisor
    b!
    lit 0 lit 0
while:
    @p counter lit -1 + !p counter
    +/
    @p counter
    -if while
    halt