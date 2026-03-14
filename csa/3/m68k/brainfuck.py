import itertools

overflow_error_value = 0xCC

def read_line(s, buf_size):
    """Read line from input with buffer size limits."""
    assert "\n" in s, "input should have a newline character"
    line = "".join(itertools.takewhile(lambda x: x != "\n", s))

    if len(line) > buf_size - 1:
        return None, s[buf_size:]

    return line, s[len(line) + 1 :]

def brainfuck_interpreter(input):
    """Brainfuck interpreter with 8 commands: ><+-.,[]

    Commands:
    - > : increment data pointer
    - < : decrement data pointer
    - + : increment 32-bit value at data pointer
    - - : decrement 32-bit value at data pointer
    - . : output low byte of 32-bit value at data pointer
    - , : input byte to low byte of 32-bit value at data pointer
    - [ : jump forward after matching ] if value at data pointer is 0
    - ] : jump back after matching [ if value at data pointer is not 0

    - Memory: 30 cells, each 32-bit signed integer, initially 0
    - Data pointer starts at 0
    - End of input -- new line
    - On error (invalid command, pointer out of bounds) return -1
    - Input comes from remaining characters after newline

    Python example args:
        input (str): The input string containing brainfuck code and input data.

    Returns:
        tuple: A tuple containing the output string and the remaining input.
    """
    line, rest = read_line(input, 0x40)
    if line is None:
        return [overflow_error_value], rest

    try:
        # Initialize Brainfuck state
        memory = [0] * 30  # 30 cells of 32-bit values
        data_ptr = 0
        code_ptr = 0
        output = []
        input_data = rest
        input_ptr = 0

        code = line

        # Validate bracket matching first
        bracket_count = 0
        for c in code:
            if c == "[":
                bracket_count += 1
            elif c == "]":
                bracket_count -= 1
                if bracket_count < 0:
                    return [-1], rest  # Unmatched closing bracket
        if bracket_count != 0:
            return [-1], rest  # Unmatched opening bracket

        while code_ptr < len(code):
            cmd = code[code_ptr]

            if cmd == ">":
                data_ptr += 1
                if data_ptr >= 30:
                    return [-1], rest
            elif cmd == "<":
                data_ptr -= 1
                if data_ptr < 0:
                    return [-1], rest
            elif cmd == "+":
                memory[data_ptr] = memory[data_ptr] + 1
                # Check for 32-bit overflow
                if memory[data_ptr] > 2147483647:
                    return [overflow_error_value], rest
            elif cmd == "-":
                memory[data_ptr] = memory[data_ptr] - 1
                # Check for 32-bit underflow
                if memory[data_ptr] < -2147483648:
                    return [overflow_error_value], rest
            elif cmd == ".":
                # Output low byte of 32-bit value
                byte_val = memory[data_ptr] & 0xFF
                output.append(chr(byte_val))
            elif cmd == ",":
                if input_ptr < len(input_data):
                    # Set low byte, keep high bits
                    memory[data_ptr] = (memory[data_ptr] & 0xFFFFFF00) | ord(
                        input_data[input_ptr]
                    )
                    input_ptr += 1
                else:
                    memory[data_ptr] = (
                        memory[data_ptr] & 0xFFFFFF00
                    )  # EOF sets low byte to 0
            elif cmd == "[":
                if memory[data_ptr] == 0:
                    # Jump forward to matching ]
                    bracket_count = 1
                    code_ptr += 1
                    while code_ptr < len(code) and bracket_count > 0:
                        if code[code_ptr] == "[":
                            bracket_count += 1
                        elif code[code_ptr] == "]":
                            bracket_count -= 1
                        code_ptr += 1
                    if bracket_count > 0:
                        return [-1], rest  # Unmatched opening bracket
                    code_ptr -= 1  # Adjust for the increment at end of loop
            elif cmd == "]":
                if memory[data_ptr] != 0:
                    # Jump back to matching [
                    bracket_count = 1
                    code_ptr -= 1
                    while code_ptr >= 0 and bracket_count > 0:
                        if code[code_ptr] == "]":
                            bracket_count += 1
                        elif code[code_ptr] == "[":
                            bracket_count -= 1
                        code_ptr -= 1
                    if bracket_count > 0:
                        return [-1], rest  # Unmatched closing bracket
                    code_ptr += 1  # Adjust for the increment at end of loop
            elif cmd in " \t\n\r":
                pass  # Ignore whitespace
            else:
                return [-1], rest  # Invalid command

            code_ptr += 1

        # Update rest to remove consumed input
        remaining_input = input_data[input_ptr:]

        return "".join(output), remaining_input

    except Exception:
        return [-1], rest


assert brainfuck_interpreter('++.\n') == ('\x02', '')
assert brainfuck_interpreter('++++++++++++++++++++++++++++++++++++++++++++++++++.\n') == ('2', '')
assert brainfuck_interpreter(',.\nA') == ('A', '')
assert brainfuck_interpreter('<\n') == ([-1], '')