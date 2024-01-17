# x86 Assembler

### What the program does

> This is a python script that reads instructions based on the x86 instruction set in 32-bit mode from a file called ‘input.txt’ and outputs the listing file translation of those instructions to a file called ‘output.txt’.
> 

### Supported Instructions

The script supports the following instructions:

- ADD, SUB, AND, OR, XOR (support only reg/reg, reg/mem, mem/reg operands with zero displacement)
- INC, DEC, POP (support only registers as operand)
- PUSH (supports  register, imm8, imm16 & imm32 as operand)


### The visulizer
The visualizer script is a simple variation of the assembler that visualizes how the code, data and stack segments look after the program is done running.
A sample input would be:
```
.stack(180)

.data(90)

var1 byte
var2 word
HeyDword Dword

.code(50)
add eax, ecx
xor [eax],ebx
push ebx
push 113
and ax, si
pop ecx
```
