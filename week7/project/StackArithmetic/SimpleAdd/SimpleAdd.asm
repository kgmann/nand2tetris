//push constant 7
@7
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 8
@8
D=A
@SP
M=M+1
A=M-1
M=D
//add
@SP
A=M-1
D=M
A=A-1
D=M+D
M=D
@SP
M=M-1
