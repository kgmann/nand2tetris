## Summary
This week we mainly focused on general modern computer systems following the von Neumann architecture, as well as machine language.
The course briefly introduced the concept of turing machines, then the von Neumann architecture which is widely used in modern computer systems.
After that it introduced binary machine language, and an assembly language. Binary is obvious as it's the two values that computers understand (low vs high voltages at the chips' level). And assembly is generally a symbolic language with a set of mneumonics that directly maps to binary instructions tighthly linked to the hardware. It's converted to binary by an assembler.
We also mentionned memory hierarchy. Retrieving and saving data to memory is generally expensive compared to the actual computations done in the CPU itself,so we have the concept of memory hierarchy. it allows us to have some very fast memory units in the cpu itself (registers), and other levels of fast but small sized memory units in addition to larger and slower ones (e.g. registers -> cache -> RAM).
We mainly focused of the registers (inside the CPU itself) this time and for the Hack computer we have two of them: The A, D and M registers. They  can be used to store data (data register) or adresses (adress register, the A register only) and can be used as pointers in that case.

The Hack language (binary and the symbolyc syntax (assembly)) has been introduced and it has two main types of instructions. A-instructions and C-instructions. A-instructions are mainly used for addressing, to deal with memory chips (registers, RAM) and C-intructions can be used to do an operation, save the result to a given register and optionally jump to a certain line in the program. We also have symbolic LABELS and references that allow us to write relocatable code. This allows the Hack language to deal with symbolic variables, branching, loops, pointers, I/O managements (through memory maps) etc...
After that we wrote two programs as part of the assignments.


# Terminologies
machine language, assembly language, assembler, symbols, memory hierarchy, opcode, peripherals, screen memory map [16384], keyboard memory map [24576], key's scan code, symbolic language, Von Neumann architecture, turing machine, NOP slide, base address (of I/O memory maps), symbolic label, symbolic variable, references, relocatable code, trace table, data register, address register,


## Other Notes
In this chapter we kind of jumped a bit ahead to write code that can be loaded in a ROM and run by a CPU with information stored in a RAM  unit. We haven't built all those things yet. Just the RAM unit and the ALU which is a part of the CPU, but the autors thought it was a good idea to do that jump first as the assembler language of a machine is typically just a symbolic wrapper around binary intructions for that machine so it's very low level.

- Read more about turing machines and the UTM. Same for the von Neumann arch.
- I had a question about how input informations from a keyboard and a mouse is managed and this has a lot to do with the OS which provide loads of things to ease interacting with those in programm written in high level languages.
- The authors didn't say the difference between the A, D and M registers in the Hack computer. I might look it up later.
- Computers never stand still, they always do something - Shimon. (This is consistant with my understanding of computer architecture)
- Good idea to end programs with an infinite loop (assembly programs loaded in ROM) to avoid attacks like NOP slide.
- I was wondering how if conditions in modern high level languages (above ASM) are constructed at the low level, and well, it's just a bunch of jumping instructions (goto). It's pretty interesting to see how it works out at the lowest level in binary or assembly.
- Random questions: what's a linker? a loader?
- Random notes: OSes use interrupt driven inputs for handling input devices like keyboard and mouse. 
- TODO: I might really need to come back to reading more on turing machines and computable functions. It seems cool.


