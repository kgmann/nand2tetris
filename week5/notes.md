## Summary
This week has mainly been about building the Hack computer. We built the Memory Unit, the CPU, and the Hack computer. The main concepts are pretty much the same as in the previous weeks, which is building a complex chip from simpler ones according to a given chip specification. In this case we're bulding the Hack computer,using the Harvard Architecture, which is a variant of the Von Neumann architecture that uses two separate buses for fetching instructions and managing data on the RAM.

# Terminologies
data bus, address bus, control bus, fetch-execute cycle, data memory, instruction / program memory, cartridge, device controllers, 

## Other Notes
I now understand why we did the chapter on machine language before actually building the computer. Machine language is tighly linked to the actual hardware and as we did with the basic chips that we built in the first few chapters, we needed to define the chip specifications first. For complex units like the CPU are a bit more complex than basic logical gates, and I guess that's why we dedicated an entire chapter on machine language first, which can be seen as the chip specifications (functionality of our CPU and Computer chips).

- Something that I've noticed is that the way I think  about programming at the hardware level is a bit different than the way I do at the software level. From implementing simple functions like a Mux/DMux to other things like addressing a Register in a RAM etc..., the way I approach it feels a bit different than when writing code in a high level programming language.
