    .data

    .org    0x123
input_addr:      .word  0x80
output_addr:     .word  0x84
sqrt_bound:      .word  0xB504

    .text
    .org     0x300

_start:
    ; lui      t0, %hi(0xffffffff)
    addi     t0, t0, 0x80000000
    lui      t0, %hi(input_addr)             ; int * input_addr_const = input_addr;
    addi     t0, t0, %lo(input_addr)         ; // t0 <- input_addr;
    lw       t0, 0(t0)                       ; int input_addr = *input_addr_const;
    halt
