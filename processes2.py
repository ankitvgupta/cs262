# processes.py: Implements logical clocks on three processes, which communicate via interprocess communcation.
#   Handles simulation of multithreading by repeatedly blocking (with a timeout) and waiting for a process to receive a message from 
#   another one. If a message comes before a timeout, this is repeated for the remaining time, until a timeout occurs.
#   This ensures that processes do work at every 1/ticks_per_second seconds. 
#   You can confirm that this works by looking at the clock values in the outputted log files.
# Authors: Ankit Gupta, Jared Pochtar
# CS 262, Harvard University

import random
import multiprocessing
import time
import Queue
import argparse
import sys

# This is a generator that defines the process clock.
# It takes the ticks per second for the proocess as an input, along with a reference to the local queue buffer.
# It works by repeatedly blocking (with a timeout) and waiting for a process to receive a message from another one. If a message comes before a timeout, this is repeated for the remaining time, until a timeout occurs.
# This ensures that processes do work at every 1/ticks_per_second seconds. 
def clock(ticks_per_second, our_queue):
    # Determine the time to wait between ticks.
    clock_wait = 1.0/ticks_per_second
    last_tick = time.time()
    while True:
        yield
        # Determine when the next should be be.
        next_tick = last_tick + clock_wait
        # Determine how long the timeout for the block should be.
        time_needed = next_tick - time.time()
        while True:
            try:
                # If we get something, move it to our queue from the interprocess queue, and block for the remaining time.
                our_queue.pull_from_main(time_needed)
                time_needed = next_tick - time.time()
            except:
                # Will go into exception when we run out of blocking time. This means it's time for next tick.
                break
        last_tick = next_tick

# This is our implementation of an in-process buffer. 
# It works by storing a reference to the inter-process communication channel, and the local buffer.
class QueueBuf(object):
    def __init__(self, ipc_queue):
        self.ipc_queue = ipc_queue
        self.queue = Queue.Queue()

    def pull_from_main(self, timeout):
        self.queue.put(self.ipc_queue.get(block=True, timeout=timeout))
    def get_nowait(self):
        return self.queue.get_nowait()
    def qsize(self):
        return self.queue.qsize()

# This defines the function that each worker process does
#   name: the name of the process
#   recv_queue: The interprocess communication channel that sends information to this process.
#   internal: In order to determine if there is an internal event, this process samples between 1 and internal. {1,2,3} are send events. [4,internal] are internal events.
#   max_ticks: In order to determine the clock speed, the process samples between 1 and max_ticks
#   global_start_time: This is just the time that the master process began. It lets us uniquely identify this job
#   time_limit: how long the worker should run
#   other_queue: The interprocess communcation channel for the first of the other processes
#   third_queue: The interprocess communcation channel for the second of the other processes
def worker(name, recv_queue, internal, max_ticks, global_start_time, time_limit, other_queue, third_queue):
    our_queue = QueueBuf(recv_queue)
    # Initialize the logical clock value
    lc = 1
    # Sample to determine the clock speed
    ticks_per_second = random.randint(1, max_ticks)
    # Create a log file
    f = open(str(global_start_time)+"_"+name+".txt", 'w')
    # Record when the pricess began
    process_start_time = time.time()
    # A simple function for unified logging. This lets us log essential parameters (name, time, logical clock value), along with any other passed args.
    def log(*args):
        f.write(', '.join([str(e) for e in [name, time.time(), lc, our_queue.qsize()] + list(args)]) + "\n")
    # Start ticking
    for tick in clock(ticks_per_second, our_queue):
        # timeout
        if time.time()  - process_start_time > time_limit:
            sys.exit()
        # If there is anything in the queue, get it.
        try:
            (recieved_value, machine) = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None
        
        # If we got something, log it.
        if recieved_value != None:
            #print("Going to log")
            lc = max(lc, recieved_value) + 1
            log("recieved", machine, recieved_value)        
        # Else, determine if we have an internal event or a sending event, and log accordingly.
        else:
            die = random.randint(1, internal)
            if die == 1:
                lc += 1
                other_queue.put((lc, name))
                log("sent", 1)

            elif die == 2:
                lc += 1
                third_queue.put((lc, name))
                log("sent", 2)

            elif die == 3:
                lc += 1
                other_queue.put((lc, name))
                third_queue.put((lc, name))
                log("sent", 3)

            else:
                # internal event
                lc += 1
                log("internal")
# A little helper function for setting up the jobs.
def without(elem, arr):
    return [x for x in arr if elem != x]

if __name__ == '__main__':
    # Parse command line arguments.
    global args
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-internal', default=10, help="Max value used for internal event (1,2,3 used for sending, 4-internal used for internal events)",
                        type=int)
    parser.add_argument('-max_speed', default=6, help="Maximum ticks per second",
                        type=int)
    parser.add_argument('-time_limit', default=60, help="Maximum time for run each process.",
                        type=int)

    args = parser.parse_args(sys.argv[1:])
    internal = args.internal
    max_speed = args.max_speed
    time_limit = args.time_limit

    # Create three queues. These queues are implemented under the hood as pipes between the processes.
    qs = [multiprocessing.Queue() for i in range(3)]

    # This assigns a unique start time to this job. 
    global_start_time = time.time()

    # Log the job arguments to a file.
    f = open(str(global_start_time)+".txt", 'w')
    f.write("Internal," + str(internal)+", MaxSpeed," + str(max_speed) + ",TimeLimit," + str(time_limit) + "\n")
    f.close()

    # Create three processes, and pass in the queues for the other processes.
    jobs = [multiprocessing.Process(target=worker,
        args=tuple([str(i), q,internal,max_speed, global_start_time, time_limit] + without(q, qs)))
        for i, q in enumerate(qs)]

    # Start the processes.
    for j in jobs:
        j.start()

    # Wait for them to finish (this will happen when they each time out.)
    for j in jobs:
        j.join()
