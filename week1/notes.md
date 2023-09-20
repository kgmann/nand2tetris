## Summary
The Week 1 mainly  focused on boolean functions and boolean albegra on the abstract side, and on logic gates on the physical side.
Boolean algebra (w/ functions, operations, formulas, etc...) is an important part in designing composite chips as a combination of elementary and other composite chips. It's abstract but turns out to be a be a good analytical entity to design and build composie chips by using it to come up with analytical expressions for boolean functions; making them more compact to use as less operations as possible; then using the final analytical expression with existing elementary or composite physical chips that are logically equivalent to the operations in the expression and building a new composite chip that exhibits the behavior of the boolean function.
Physical chips are more in the domain of physics and electrical engineering than in computer science so the course didn't go deeper and moving forward we'll be using some elementary chips (e.g. NAND) as given and operate on them to build the Hack computer.
To build a new composite chip, we typically go from the requirements (free form function) of the chip and derive the interface, the chip diagram and then the HDl code to simulate the chip and test it to ensure that it's coherent with the chip contract. For testing it's generally more convenient to use a hardware simulator with an automated test script and a compare file rather than doing interative testing. The course also mentioned the concept of buses which is bery handy when dealing with a group of bits simultaneously in a circuit.
As part of the Project 1, we have to build 15 chips including a set of Mux and Demux chips that are respectively a multiplexer and a demultiplexer which are very often used in most digital circuits and can be used to build programmable gates for example.

# Terminologies
digital circuits, gate logic, logic gates, boolean algebra, elementary logic gate (e.g. nand), boolean functions,
chip interface, chip contract, hdl (hardware description language), chip/gate logic diagram, bus, multibit buses,
sub-buses, multiplexer (mux), demultiplexer (dmux), programmable gate, input signals, output line, select/control lines, 
fan in/fan out, 



## Other Notes
* It's pretty cool to see how the entire process of building the hack computer can be modularized and implemented in a layered manner. At each level we have some abstractions / APIs made available to the next level and so on. I think it's a cool SWE practice in action.  
* See boolean functions for what they are, functions. For the multiplexer for example, it's a if condition which is a boolean function basically.
* 
