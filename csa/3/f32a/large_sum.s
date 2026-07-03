    .data

n:      .word  3
array:  .word  0x123, 0xFFFFFEED, 0x16, 0xFFFFBEEF, 0x1D01, 0xFFFFA812
result: .word  0, 0

    .text
_start:
    @p n lit -1 + >r
    lit array a!
    
    lit 0               \ High accumulator
    lit 0               \ Low accumulator

    lit 1 eam

while:
    @                   \ reading High word
    over
    a lit 4 + a!
    @                   \ reading Low word
    a lit 4 + a!
    +                   \ summing Low words
    
    >r                  \ stash the low word result
    +                   \ summing High words
    r>                  \ swapping them back
    
    next while

end:
    lit result a!
    !
    a lit 4 + a!
    !               
    halt