import os, sys

# THIS IS NOT DONE, IDFK WHEN ITL BE DONE.

def emit_print(char, is_last):
    return (
        "[-]"                      # syscall id cell
        + "+"                      # syscall id = 1
        + ">" + "[-]" + "+" * ord(char)   # char
        + ">" + "[-]" + ("+" if is_last else "")  # printOut flag
        + "<<*"                    # syscall trigger
    )


def transpile(program):
    bf_code = []

    for line in program.splitlines():
        line = line.strip()

        if line.startswith("print"):
            start = line.find('"')
            end = line.rfind('"')

            if start == -1 or end == -1 or end <= start:
                continue  # skip malformed lines

            text = line[start + 1:end]

            for i, char in enumerate(text):
                is_last = (i == len(text) - 1)
                bf_code.append(emit_print(char, is_last))

    return "".join(bf_code)


# =========================
# Example usage
# =========================

program = '''
print "HELLO WORLD"
print "!!!"
'''

bf_output = transpile(program)

print(bf_output)