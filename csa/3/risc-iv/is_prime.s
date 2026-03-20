    .data

input_addr:      .word  0x80
output_addr:     .word  0x84
sqrt_bound:      .word  0xB504

    .text
    .org     0x100

_start:
    lui      t0, %hi(input_addr)             ; int input_addr_val = mem[input_addr] & 0xfffff000;
    addi     t0, t0, %lo(input_addr)         ; input_addr_val += mem[input_addr] & 0xfff;
    lw       t0, 0(t0)                       ; input_addr_val = *input_addr_val;

    lw       a1, 0(t0)                       ; int n = *input_addr_val;
    jal      ra, func_is_prime               ; bool a0 = is_prime(n);

    lui      t0, %hi(output_addr)            ; int output_addr_val = mem[output_addr] & 0xfffff000;
    addi     t0, t0, %lo(output_addr)        ; output_addr_val += mem[output_addr] & 0xfff;
    lw       t0, 0(t0)                       ; output_addr_val = *output_addr_val;

    sw       a0, 0(t0)                       ; *output_addr_val = a0;
    halt

func_is_prime:                               ; bool func_is_prime(int n) { ... }
    mv       a0, zero                        ; set return value to 0

    bgt      a1, zero, _prime_is_one         ; if (n < 1) {
    addi     a0, zero, -1                    ;   return -1;
    jr       ra                              ; }
_prime_is_one:
    addi     t1, a1, -1                      
    bnez     t1, _prime_is_two               ; if (n == 1)
    jr       ra                              ;   return 0;
_prime_is_two:
    addi     t1, t1, -1                      
    bnez     t1, _prime_is_big               ; if (n == 2) { 
    addi     a0, zero, 1                     ;   return 1;
    jr       ra                              ; }
_prime_is_big:
    mv       a3, a1
    lui      t1, %hi(sqrt_bound)             
    addi     t1, t1, %lo(sqrt_bound)         
    lw       t1, 0(t1)
    ble      a3, t1, _prime_is_minimal_bound
    mv       a3, t1
_prime_is_minimal_bound:
    sw       ra, 0(sp)                       ; saving initial ra to stack
    jal      ra, func_sqrt                   
    mv       a2, a0                          ; int sqrt_n = sqrt(n, 1, min(n, sqrt_bound))
    addi     a3, zero, 2
    jal      ra, func_div                    ; a0 = div(n, sqrt_n, 2)
    lw       ra, 0(sp)                       ; loading initial ra from stack 
    jr       ra

func_div:                                    ; bool div(int n, int sqrt_n, int divider) { ... }
    bne      a2, a3, _div_not_equal          ; if (sqrt_n == divider)
    rem      a0, a1, a3                      ; {
    beqz     a0, _div_false                  ;   return n % divider > 0;
    addi     a0, zero, 1                     ;   // filler comment line
    jr       ra                              ; }
_div_not_equal:
    rem      t1, a1, a3                      
    bne      t1, zero, _div_not_divides      ; if (n % divider == 0)
_div_false:                                  ; {
    mv       a0, zero                        ;   return 0;
    jr       ra                              ; } else
_div_not_divides:                            ; {
    addi     a3, a3, 1                       ;   return div (n, sqrt_n, divider + 1);
    j        func_div                        ; }

func_sqrt:                                   ; int sqrt(int n, int l, int r) { ... }
    bne      a2, a3, _sqrt_bounds_not_equal  ; if (l == r) {
    mv       a0, a3                          ;   return r;
    jr       ra                              ; }
_sqrt_bounds_not_equal:
    sub      t1, a3, a2
    addi     t2, zero, 1
    srl      t1, t1, t2
    add      t1, a2, t1                      ; int mid = l + ((r - l) >> 1);
    mul      t2, t1, t1                      ; int x = mid * mid;
    bne      a1, t2, _sqrt_not_found         ; if (x == n) {
    mv       a0, t1                          ;   return mid;
    jr       ra                              ; }
_sqrt_not_found:
    ble      t2, a1, _sqrt_less_than         ; if (x > n) {
    mv       a3, t1                          ;   return sqrt(n, l, mid);
    j        func_sqrt                       ; }
_sqrt_less_than:
    addi     a2, t1, 1                       
    j        func_sqrt                       ; return sqrt(n, mid + 1, r);
