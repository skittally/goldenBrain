import os, sys, argparse, time

# Parser shit for commend arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input compiled brainfuck code")
parser.add_argument("--debugging", help="used for program debugging. WARNING: this will fuck speed", action="store_true")
args = parser.parse_args()

def sysCall(memory, position, printBuffer):
    sysMemoryCall = memory[position]
    printInput = memory[position + 1]
    printOut = memory[position + 2]

    if sysMemoryCall == 1:
        printBuffer += chr(printInput)
        if printOut == 1:
            print(printBuffer)
    
    return printBuffer

def build_jump_table(instructions):
    stack = []
    jump = [0]*len(instructions)

    for i, instr in enumerate(instructions):
        if instr == 7:  # [
            stack.append(i)
        elif instr == 8:  # ]
            if not stack:
                raise ValueError("Unmatched ]")
            j = stack.pop()
            jump[i] = j
            jump[j] = i

    if stack:
        raise ValueError("Unmatched [")

    return jump


def process_and_run(): # converts the binary to proper OP codes and then runs it
        
    with open(args.input, 'rb') as f:
        bf_binary = f.read()

    
    debugging = args.debugging
    callCounter = 0
    position = 0

    memory = bytearray(512)

    instructions = [((byte >> 4) & 0x0F, byte & 0x0F ) for byte in bf_binary]
    jump = build_jump_table([op for op, _ in instructions])

    instructionCounter = 0

    instructionLength = len(instructions)   

    printBuffer = "" # setting up the print buffer for the print syscall.

    while instructionCounter < instructionLength: # the main instruction loop

        op, mult = instructions[instructionCounter]

        if op == 1:  # (+)
            memory[position] = (memory[position] + mult) & 0xFF

        elif op == 2:  # (-)
            memory[position] = (memory[position] - mult) & 0xFF

        elif op == 3:  # (<)
            if position - mult < 0:
                print(f"Pointer < 0 error")
                sys.exit(1)
            position -= mult

        elif op == 4:  # (>)
            position += mult
            if position >= len(memory):
                memory.extend(b'\x00' * len(memory) if len(memory) else b'\x00')

        elif op == 5:  # (.)
            sys.stdout.write(chr(memory[position]))

        elif op == 6:  # (,)
            memory[position] = ord(sys.stdin.read(1) or '\0')

        elif op == 7:  # [

            loop_end = jump[instructionCounter]
            loop_len = loop_end - instructionCounter

            # 1. CLEAR LOOP: [-] or [+]
            if loop_len == 2:
                inner_op, inner_mult = instructions[instructionCounter + 1]

                if inner_op in (1, 2):  # + or -
                    memory[position] = 0
                    instructionCounter = loop_end
                    continue

                # 2. SCAN LOOPS: [>] or [<]
                if inner_op == 4:  # >
                    while position < len(memory) and memory[position] != 0:
                        position += inner_mult
                        if position >= len(memory):
                            memory.extend(b'\x00' * len(memory))
                    instructionCounter = loop_end
                    continue

                elif inner_op == 3:  # <
                    while position > 0 and memory[position] != 0:
                        position -= inner_mult
                    instructionCounter = loop_end
                    continue

            # 3. COPY LOOP: [->+<]
            elif loop_len == 5:
                p = instructions[instructionCounter+1:loop_end]

                if (
                    p[0] == (2, 1) and  # -
                    p[1] == (4, 1) and  # >
                    p[2] == (1, 1) and  # +
                    p[3] == (3, 1)      # <
                ):
                    val = memory[position]
                    if val:
                        if position + 1 >= len(memory):
                            memory.extend(b'\x00' * len(memory))

                        memory[position + 1] = (memory[position + 1] + val) & 0xFF
                        memory[position] = 0

                    instructionCounter = loop_end
                    continue

            if memory[position] == 0:
                instructionCounter = loop_end

        elif op == 8:  # (])
            if memory[position] != 0:
                instructionCounter = jump[instructionCounter]
        
        elif op == 9: # golden brain syscall
            printBuffer = sysCall(memory, position, printBuffer)
        
        else:
            pass

        instructionCounter += 1

        if debugging:
            callCounter += 1
            if instructionCounter == len(instructions):
                print(f"steps: {callCounter}")
        

def main(): # do i must explain??
    _start = time.perf_counter()
    process_and_run()
    elapsed = time.perf_counter() - _start
    print(f"Elapsed: {elapsed:.6f} s ({elapsed*1000:.3f} ms)")

if __name__ ==  "__main__": main()
