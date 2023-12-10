# x86 Assembler

### What the program does

> This is a python script that reads instructions based on the x86 instruction set in 32-bit mode from a file called ‘input.txt’ and outputs the listing file translation of those instructions to a file called ‘output.txt’.
> 

### Supported Instructions

The script supports the following instructions:

- ADD, SUB, AND, OR, XOR (support only reg/reg, reg/mem, mem/reg operands with zero displacement)
- INC, DEC, POP (support only registers as operand)
- PUSH (supports  register, imm8, imm16 & imm32 as operand)
