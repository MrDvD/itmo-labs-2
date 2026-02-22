    .data

input_addr:      .word  0x80
input_value:     .word  0
raw_result:      .word  0
output_addr:     .word  0x84
byte_1:          .word  8
bytes_3:         .word  24
mask_FF00:       .word  0xFF00
mask_FF:         .word  0xFF

    .text

_start:

    load         input_addr
    load_acc
    store        input_value

    shiftl       bytes_3                     ; first byte
    store        raw_result

    load         input_value                 ; second byte
    and          mask_FF00
    shiftl       byte_1
    or           raw_result
    store        raw_result

    load         input_value                 ; third byte
    shiftr       byte_1
    and          mask_FF00
    or           raw_result
    store        raw_result

    load         input_value                 ; fourth byte
    shiftr       bytes_3
    and          mask_FF
    or           raw_result
    store_ind    output_addr

    halt
