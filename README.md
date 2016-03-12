# Assignment 2 - CS 262
## Ankit Gupta, Jared Pochtar

In this assignment, we implemented logical clocks in three processes, and allowed them to communicate with one another. In particular we made two implementations, which deal with the fact that Python has a GIL and thus cannot truly support multithreading. These two implements simulate having two threads in separate ways.

## Implementations
- [processes.py](processes.py): Contains implementation 1, as explained below.
- [processes2.py](processes2.py): Contains implementation 2, as explained below.

### Implementation 1 - Pull from queue on tick, and adjust sleeping time
In this implementation, we handle simulation of multithreading by pulling from interprocess communication queues at the clock's tick time. Then, we adjust the amount of waiting time for the next tick by subtracting the amount of time that the work took. This makes sure that work is done every 1/ticks_per_second seconds. You can confirm that this works by looking at the clock values in the outputted log files. At every tick, there is a log output.

### Implementation 2 - Wait for items to come in queue by blocking, and block again if item comes before timeout.
In this implementation, we handle simulation of multithreading by repeatedly blocking (with a timeout) and waiting for a process to receive a message from another one. If a message comes before a timeout, this is repeated for the remaining time, until a timeout occurs. This ensures that processes do work at every 1/ticks_per_second seconds. You can confirm that this works by looking at the clock values in the outputted log files. At every tick, there is a log output.