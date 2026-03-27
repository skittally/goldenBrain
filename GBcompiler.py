import os, sys, argparse, re
from typing import List, Tuple
from time import sleep

# Parser shit for commend arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input raw brainfuck code")
parser.add_argument("--output", help="output compiled file")
args = parser.parse_args()

# remove me!
print(f"{args.input}")
print(f"{args.output}")

# init vars
bf_code = ""


def read(): # Read the input from the --input flag and clean the code
    with open(args.input, 'r') as f:
        bf_code_dirty = f.read()
        f.close()
    bf_code = re.sub(r'[^+\-<>.,\[\]\*]', '', bf_code_dirty)

    return(bf_code)

def convert_and_write(bf_code):
    binaryData = bytearray()
    buffer = None
    max_count = 15
    compressible = set("+-<>")

    if not bf_code:
        with open(args.output, "wb") as f:
            f.write(binaryData)
        return

    def op_to_nibble(op):
        if op == "+":
            return 0x1
        if op == "-":
            return 0x2
        if op == "<":
            return 0x3
        if op == ">":
            return 0x4
        if op == ".":
            return 0x5
        if op == ",":
            return 0x6
        if op == "[":
            return 0x7
        if op == "]":
            return 0x8
        if op == "*":
            return 0x9
        return None

    prev = None
    cnt = 0

    # iterate over characters and build runs on the fly
    for char in bf_code:
        if prev is None:
            prev = char
            cnt = 1
            continue

        if char == prev:
            cnt += 1
            continue

        # run ended -> set op and opNumber, then emit in chunks
        op = prev
        opNumber = cnt
        while opNumber > 0:
            if op in compressible:
                take = min(opNumber, max_count)
            else:
                take = 1
            opNumber -= take

            nibble_op = op_to_nibble(op)
            if nibble_op is None:
                print("- WARN: the code is still dirty? (skipping)", op)
                continue

            nibble_cnt = take & 0xF

            # emit op nibble then count nibble (pack two nibbles per byte)
            for nibble in (nibble_op, nibble_cnt):
                if buffer is None:
                    buffer = nibble & 0xF
                else:
                    byte = ((buffer & 0xF) << 4) | (nibble & 0xF)
                    binaryData.append(byte)
                    buffer = None

        prev = char
        cnt = 1

    # handle final run
    if prev is not None and cnt > 0:
        op = prev
        opNumber = cnt
        while opNumber > 0:
            if op in compressible:
                take = min(opNumber, max_count)
            else:
                take = 1
            opNumber -= take

            nibble_op = op_to_nibble(op)
            if nibble_op is None:
                print("- WARN: the code is still dirty? (skipping)", op)
                continue

            nibble_cnt = take & 0xF
            for nibble in (nibble_op, nibble_cnt):
                if buffer is None:
                    buffer = nibble & 0xF
                else:
                    byte = ((buffer & 0xF) << 4) | (nibble & 0xF)
                    binaryData.append(byte)
                    buffer = None

    if buffer is not None:
        binaryData.append((buffer & 0xF) << 4)

    with open(args.output, "wb") as f:
        f.write(binaryData)
    print("- CODE COMPILED SUCCESSFULLY")

    with open(args.output, "rb") as f:
        data = f.read()
    print([f"0x{b:02x}" for b in data])
    print(" ".join(f"{b:02x}" for b in data))



def main(): # do i have to fucking explain?
    bf_code = read()
    print("- CODE READ WITH 0 ERRORS")
    convert_and_write(bf_code)

if __name__ ==  "__main__": main()
