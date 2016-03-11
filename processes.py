import random
import multiprocessing
import time
import Queue
import argparse
import sys

def clock(ticks_per_second):
    clock_wait = 1.0/ticks_per_second
    last_tick = time.time()
    while True:
        next_tick = last_tick + clock_wait
        yield
        time.sleep(max(next_tick - time.time(), 0))
        last_tick = next_tick

class QueueBuf(object):
    def __init__(self, ipc_queue):
        self.ipc_queue = ipc_queue
        self.queue = Queue.Queue()

    def get_nowait(self):
        while not self.ipc_queue.empty():
            self.queue.put(self.ipc_queue.get_nowait())
        return self.queue.get_nowait()

    def qsize(self):
        return self.queue.qsize()

def worker(name, recv_queue, internal, max_ticks, global_start_time, other_queue, third_queue):
    our_queue = QueueBuf(recv_queue)
    lc = 1
    ticks_per_second = random.randint(1, max_ticks)
    # Create a log file
    f = open(str(global_start_time)+"_"+name+".txt", 'w')
    #print max_ticks, internal

    def log(*args):
        f.write(', '.join([str(e) for e in [name, time.time(), lc, our_queue.qsize()] + list(args)]) + "\n")

    for tick in clock(ticks_per_second):
        try:
            (recieved_value, machine) = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None

        if recieved_value != None:
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

    args = parser.parse_args(sys.argv[1:])
    internal = args.internal
    max_speed = args.max_speed
	# Create three queues
    qs = [multiprocessing.Queue() for i in range(3)]
    # Create three processes, and pass in the shared queues
    # This assigns a unique start time to this job.
    global_start_time = int(time.time())
    jobs = [multiprocessing.Process(target=worker,
        args=tuple([str(i), q,internal,max_speed, global_start_time] + without(q, qs)))
        for i, q in enumerate(qs)]

    # Start the jobs
    for j in jobs:
        j.start()

    # Wait for them to finish
    for j in jobs:
        j.join()
