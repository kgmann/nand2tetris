## Summary
This week mainly focused on building an ALU chip. The Arithmetic Logic Unit is an important piece of a CPU (in addition to the control unit and the memory unit) and is reponsible as the name suggest to arithmetic logic. Before building it, we first built some Adders (half, full, add16) chips, and then used some of the previous chips that we built to build the ALU chip. The Hack computer's ALU is pretty simple and only suports a combination of basic operations like (setting to zero, logical not, addition, logical and) between two inputs. Some more sophisticated ALUs can support more operations like multiplication among other, but those can also be added at the software level with the basic chip that we built. In general, if an ALU support agiven operation natively (the physical chip), it would be faster than when we add support for that operation at the software lvel, but it also makes the ALU more complex. We also learned a bit about signed integer representations on hardware level where we used the 2's complement method as it makes arithmetic operations like susbtraction easier by reusing addition, and it doesn't have two zeros with different sign like the sign-magnitude method.

# Terminologies
Adder, ALU (Arithmetic Logic Unit), CPU (Central Processing Unit), carry look ahead, sign-magnitude, 1's complement, 2's complement.


## Other Notes
- read more about the 2's complement representation method. it's beautiful btw
- Apparently, they are four main methods for representing signed binary numbers (sign-magnitude, 1's complement, 2's complement, offset binary)

