// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// I could optimize the code ans instead of always running the clear/blacken screen loop at each iteration 
// I will only do that when there's a change in an event
@8192
D=A
@screen_registers
M=D // total number of registers in the screen memory map


(MAIN_LOOP) // Infinite loop
    @KBD
    D=M // read keyboard

    @CLEAR_SCREEN
    D;JEQ // if keyboard==0 clear the screen
    @BLACKEN_SCREEN // else blacken it

(BLACKEN_SCREEN)
    @0
    D=A
    @temp_counter
    M=D // counter for screen register

    @1
    D=-A
    @black_value
    M=D

    (BLACK_SCREEN_LOOP)
        @temp_counter
        D=M
        @SCREEN
        D=A+D
        @temp
        M=D
        @black_value
        D=M
        @temp
        A=M
        M=D // set screen[temp_counter] to black

        @screen_registers
        D=M
        @temp_counter
        M=M+1 // increment temp_counter
        D=D-M
        @MAIN_LOOP
        D;JEQ // if screen_register - temp_counter == 0 go to main loop
        @BLACK_SCREEN_LOOP
        0;JEQ // else contiune filling with black


(CLEAR_SCREEN)
    @0
    D=A
    @temp_counter
    M=D // counter for screen register

    @0
    D=A
    @white_value
    M=D

    (CLEAR_SCREEN_LOOP)
        @temp_counter
        D=M
        @SCREEN
        D=A+D
        @temp
        M=D
        @white_value
        D=M
        @temp
        A=M
        M=D // set screen[temp_counter] to white

        @screen_registers
        D=M
        @temp_counter
        M=M+1 // increment temp_counter
        D=D-M
        @MAIN_LOOP
        D;JEQ // if screen_register - temp_counter == 0 go to main loop
        @CLEAR_SCREEN_LOOP
        0;JEQ // else contiune filling with black

