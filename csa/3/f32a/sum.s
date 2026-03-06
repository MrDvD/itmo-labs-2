    .data

n:               .word  6
array:           .word  0x12, 0x13, 0x16, 0x21, 0x17, 0x8

    .text

_start:
    @p n lit -1 + >r
    lit array a!

    lit 0 eam
    lit 0         \ current_sum
while:
    @ +

    a lit 4 + a!  \ i++
    
    next while
end:
    b!
    halt