
.data
.org 0x0
buffer:          .byte '________________________________'

.org 0x300

quest_start:     .word  'W' , 'h' , 'a' , 't' , ' ' , 'i' , 's' , ' ' , 'y' , 'o' , 'u' , 'r' , ' ' , 'n' , 'a' , 'm' , 'e' , '?' , 10
hello_start:     .word  'H' , 'e' , 'l' , 'l' , 'o' , ',' , ' '
exclam:          .word  '!'

; Переменные
ptr:             .word  0
cnt:             .word  0
first_char:      .word  0
one:             .word  1
four:            .word  4
newline:         .word  10

.text
.org 0x400

_start:
    ; Выводим вопрос
    load_imm     quest_start
    store        ptr
    load_imm     19
    store        cnt

print_question:
    load         cnt
    beqz         read_first

    load         ptr
    load_acc
    store_addr   0x84

    load         ptr
    add          four
    store        ptr

    load         cnt
    sub          one
    store        cnt

    jmp          print_question

read_first:
    ; Читаем первый символ и сохраняем его
    load_addr    0x80
    store        first_char
    
    ; Выводим "Hello, "
    load_imm     hello_start
    store        ptr
    load_imm     7
    store        cnt

print_hello:
    load         cnt
    beqz         print_first

    load         ptr
    load_acc
    store_addr   0x84

    load         ptr
    add          four
    store        ptr

    load         cnt
    sub          one
    store        cnt

    jmp          print_hello

print_first:
    ; Выводим первый символ
    load         first_char
    store_addr   0x84
    
    ; Читаем и выводим остальные символы до newline
read_next:
    load_addr    0x80
    store        cnt
    
    ; Проверяем на newline
    load         cnt
    sub          newline
    beqz         print_exclam
    
    ; Выводим символ
    load         cnt
    store_addr   0x84
    
    jmp          read_next

print_exclam:
    load         exclam
    store_addr   0x84
    halt
