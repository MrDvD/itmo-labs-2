    .data

temp:            .word  0x80                 ; input address
input_value:     .word  0
output_addr:     .word  0x84
byte_1:          .word  8
bytes_3:         .word  24
mask_FF:         .word  0xFF

    .text

_start:

    load         temp
    load_acc
    store        input_value

    shiftl       bytes_3                     ; first byte
    store        temp

    load_imm     0xFF00                      ; second byte
    and          input_value
    ; load         input_value               ; alternative way,
    ; and          mask_FF00                 ; uses 2 bytes more
    shiftl       byte_1
    or           temp
    store        temp

    load_imm     0xFF0000                    ; third byte
    and          input_value
    shiftr       byte_1
    or           temp
    store        temp

    load         input_value                 ; fourth byte
    shiftr       bytes_3                     ; it's an arithmetic shift,
    and          mask_FF                     ; so we need to apply mask in the end
    or           temp
    store_ind    output_addr

    halt
