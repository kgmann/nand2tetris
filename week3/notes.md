## Summary
This chapter mainly focused on building memory units for the Hack computer. Sequential Logic has been introduced and it's a logic implemented by sequential circuits in which outputs depend on the current input and the previous output or state. Combinational chips on the other hand operate only on the present input for generating outputs. An example of a sequential chip is the delay flip flop dff that sets the current output to the input at the previous clock cycle (timestep). THe chip is clock edge sensitive and only changes its output at a given clock edge signal. The chip can be created with nand gates with some loops, but they are considered as primitive in the course.

We then used it to create other composite sequential circuits like Bit, Register, RAM and Program Counter. The Bit chip stores a binary signal and remembers it as long it's not asked to remember a new value (the Dff only remembers the previous input). The Register is a multibit memory unit made of multiple Bit chips and it can store a 'word' of a given width (basically store w binary signals). A RAM unit is generally composed of multiple randomly adressable registers and allow read/write operations on them, one register at a time. Finally the Program Counter is chip with multiple capabilities and can function as a counter that sets, resets or increments its value based on the input pins' values.

Regarding the clock, it has many roles in a computer and it's very useful to build synchronous systems. It's not required to build sequential logic chips, in fact we have some chips like SR gates that can remember without a need for a clock signal.
That said, in the chips that we discussed so far (both combinational and sequential), there is a propagation delay to account for when an input is passed to the chip before we get a stable and valid output that's a function of the input. The clock also makes discrete time units for the entire system based on its cycle instead which is convenient to work with.
This exerptfromthe book is pretty good:
-   This ‘‘discretization’’ of the sequential chips’ outputs has an important side effect:
    It can be used to synchronize the overall computer architecture. To illustrate, sup-
    pose we instruct the arithmetic logic unit (ALU) to compute x þ y where x is the
    value of a nearby register and y is the value of a remote RAM register. Because of
    various physical constraints (distance, resistance, interference, random noise, etc.) the
    electric signals representing x and y will likely arrive at the ALU at different times.
    However, being a combinational chip, the ALU is insensitive to the concept of time—
    it continuously adds up whichever data values happen to lodge in its inputs. Thus, it
    will take some time before the ALU’s output stabilizes to the correct x þ y result.
    Until then, the ALU will generate garbage.
    How can we overcome this difﬁculty? Well, since the output of the ALU is always
    routed to some sort of a sequential chip (a register, a RAM location, etc.), we don’t
    really care. All we have to do is ensure, when we build the computer’s clock, that
    the length of the clock cycle will be slightly longer that the time it takes a bit to travel
    the longest distance from one chip in the architecture to another. This way, we are
    guaranteed that by the time the sequential chip updates its state (at the beginning of
    the next clock cycle), the inputs that it receives from the ALU will be valid. This, in a
    nutshell, is the trick that synchronizes a set of stand-alone hardware components into
    a well-coordinated system, as we shall see in chapter 5.


# Terminologies
RAM (Random Access Memory), flip-flops, latch, registers, combinational logc, sequential logic, clock cycle, level-sensitive, edge-sensitive, synchronous systems, master clock, clock cycle, memory banks.

## Other Notes
- Combinational vs sequential logic is mainly about the behavior of the chips. 
- We used d flip flop as elementary gates here. Dive a bit into it building it later.
- We also use clock signal to cooridnate tasks in synchronous systems.
- Think about improving the chips that I built. I first made sure to have something working,but I could try to make them better (use fewer gates).
- The course also mentionned other memory types like ROM, flash memories and cache memories.
