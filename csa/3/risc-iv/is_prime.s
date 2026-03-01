    .data

input_addr:      .word  0x80
output_addr:     .word  0x84
sqrt_bound:      .word  0xB504

    .text
    .org     0x100

_start:
    lui      t0, %hi(input_addr)             ; int * input_addr_const = input_addr;
    addi     t0, t0, %lo(input_addr)         ; // t0 <- input_addr;
    lw       t0, 0(t0)                       ; int input_addr = *input_addr_const;

    lw       a1, 0(t0)                       ; int n = *input_addr;
    jal      ra, func_prime

    lui      t0, %hi(output_addr)            ; int * output_addr_const = output_addr;
    addi     t0, t0, %lo(output_addr)        ; // t0 <- output_addr;
    lw       t0, 0(t0)                       ; ???

    sw       a0, 0(t0)                       ; ???
    halt

func_prime:
    bgt      a1, zero, _prime_is_one         ; if (n < 1) {
    addi     a0, zero, -1                    ;   // ???
    jr       ra                              ; }
_prime_is_one:
    addi     t1, a1, -1                      ; if (n == 1) {
    bnez     t1, _prime_is_two
    mv       a0, zero                        ;   // ???
    jr       ra
_prime_is_two:
    addi     t1, t1, -1
    bnez     t1, _prime_is_big
    lui      a0, 0 ;;;;;;;;;;;;
    addi     a0, zero, 1
    jr       ra
_prime_is_big:
    mv       a3, a1
    lui      t1, %hi(sqrt_bound)             ; int * input_addr_const = input_addr;
    addi     t1, t1, %lo(sqrt_bound)         ; // t0 <- input_addr;
    lw       t1, 0(t1)
    ble      a3, t1, _prime_already_minimal_bound
    mv       a3, t1
_prime_already_minimal_bound:
    sw       ra, 0(sp)
    jal      ra, func_sqrt
    mv       a2, a0
    addi     a3, zero, 2
    jal      ra, func_div
    lw       ra, 0(sp)
    jr       ra

func_div:
    bne      a2, a3, _div_not_equal
    rem      a0, a1, a3
    beqz     a0, _div_false
    addi     a0, zero, 1
    jr       ra
_div_not_equal:
    rem      t1, a1, a3
    bne      t1, zero, _div_not_divides
_div_false:
    mv       a0, zero
    jr       ra
_div_not_divides:
    addi     a3, a3, 1
    j        func_div

func_sqrt:
    bne      a2, a3, _sqrt_bounds_not_equal
    mv       a0, a3
    jr       ra
_sqrt_bounds_not_equal:
    sub      t1, a3, a2
    addi     t2, zero, 1
    srl      t1, t1, t2
    add      t1, a2, t1                      ; mid = l + ((r - l) >> 1)
    mul      t2, t1, t1                      ; x = mid * mid
    bne      a1, t2, _sqrt_not_found
    mv       a0, t1
    jr       ra
_sqrt_not_found:
    ble      t2, a1, _sqrt_less_than
    mv       a3, t1
    j        func_sqrt
_sqrt_less_than:
    addi     a2, t1, 1
    j        func_sqrt
