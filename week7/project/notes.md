## Summary

This is a good refresher on many of the things that I did in Nand to Tetris part 1. 
Refresher on combinational logic and sequential logic in digital circuits, with the latter adding a clock to make the current output of a chip depend on the results of inputs at a previous timestep. It's also a good refresher on some of the chips that I built in part 1, mainly the global architecture of the CPU and the computer chip.
It's based on the Von Neumann architecture and we use a ROM where the instructions are loaded from and a RAM to store and retrieve data. We also use memory mapping to handle devices like a keyboard and a screen. So yeah the hack computer is general purpose computer (but in this case we'll have to swap the ROM to load new programs I guess), and a computer, at the hardware level, is just a dumb calculator that has a CPU to do elementary logic and arithmetic calculations, and retrieve or save data to a memory chip (RAM). The computation is determined by the instruction it gets from the ROM in our case. So yeah now that I have some basic knowledge of a computer's hardware, I have the feeling that the magic of computers, is very much at the bridge between the hardware and the software, especially earlier on when modern computers (hardware + OS, compilers to write programs, etc...) were being built without modern computers to aid the process. I also have the feeling that there's actually a huge value added by the most fundamental software stack on a computer (OS, compilers, etc...) to make the whole thing easy to use for programmers. At the end of the day I think as a software engineer, we're mostly building on shoulders or giants and all that have been done to make it possible to write wild and complex programs in high level languages for all that to run on a dumb machine that can only do very basic arithmetic and logical operations (just some powerful and programmable calculator lol). 

It was also a good refresher on concepts like memory hierarchy in computers; the hack machine language made of A and C instructions; nop slide and how to avoid that; virtual registers and special symbols in the hack language, labels (branching symbols), variable declariation in the hack language, relocatable code, etc...
Fundamentally, I believe things like labels and variables are not intrisic to machine language but rather constructs that need to be parsed and process by the assembler, as opposed to having a one to one  mapping between the instruction and the resulting binary code.

I also briefly thought about parallel computing on multiple cores and made some quick search about it. The hack computer has a single CPU but with multiple CPU cores, I have the impression that it's gonna be a whole lot harder.

Anyway, I'll eventually submit the assignments I did in the part I of the course instead of doing it over again. 


## Terminologies


## Other Notes

