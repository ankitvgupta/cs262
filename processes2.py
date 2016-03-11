import random
import multiprocessing
import time
import Queue
import argparse
import sys

def clock(ticks_per_second, our_queue):
    clock_wait = 1.0/ticks_per_second
    last_tick = time.time()
    while True:
        yield
        next_tick = last_tick + clock_wait
        time_needed = next_tick - time.time()
        while True:
            try:
                our_queue.pull_from_main(time_needed)
                time_needed = next_tick - time.time()
            except:
                # Will go into exception when we run out of blocking time. This means it's time for next tick.
                break
        last_tick = next_tick


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

def worker(name, recv_queue, internal, max_ticks, global_start_time, time_limit, other_queue, third_queue):
    our_queue = QueueBuf(recv_queue)
    lc = 1
    ticks_per_second = random.randint(1, max_ticks)
    # Create a log file
    f = open(str(global_start_time)+"_"+name+".txt", 'w')
    #print max_ticks, internal
    process_start_time = time.time()
    def log(*args):
        f.write(', '.join([str(e) for e in [name, time.time(), lc, our_queue.qsize()] + list(args)]) + "\n")

    for tick in clock(ticks_per_second, our_queue):
        if time.time()  - process_start_time > time_limit:
            sys.exit()
        try:
            (recieved_value, machine) = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None

        if recieved_value != None:
            #print("Going to log")
            lc = max(lc, recieved_value) + 1
            log("recieved", machine, recieved_value)

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

def without(elem, arr):
    return [x for x in arr if elem != x]

if __name__ == '__main__':
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
	# Create three queues
    qs = [multiprocessing.Queue() for i in range(3)]
    # Create three processes, and pass in the shared queues
    # This assigns a unique start time to this job.
    global_start_time = time.time()
    f = open(str(global_start_time)+".txt", 'w')
    f.write("Internal," + str(internal)+", MaxSpeed," + str(max_speed) + ",TimeLimit," + str(time_limit) + "\n")
    f.close()
    jobs = [multiprocessing.Process(target=worker,
        args=tuple([str(i), q,internal,max_speed, global_start_time, time_limit] + without(q, qs)))
        for i, q in enumerate(qs)]

    # Start the jobs
    for j in jobs:
        j.start()

    # Wait for them to finish
    for j in jobs:
        j.join()
