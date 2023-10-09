// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// ram0 = RAM[0]
@R0
D=M
@ram0
M=D

// ram1 = RAM[1]
@R1
D=M
@ram1
M=D

// result=R2=0
@0
D=A
@R2
M=D

// counter=0
@0
D=A
@counter
M=D

(LOOP)
    @ram1
    D=M
    @counter
    D=D-M
    @END
    D;JEQ // end when ram1-counter == 0

    @ram0
    D=M
    @R2
    M=D+M // result = result + ram0

    @counter
    M=M+1 // counter += 1

    @LOOP
    0;JEQ // jump back to loop

(END)
    @END
    0;JEQ
