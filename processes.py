import random
import multiprocessing
import time
import Queue

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

def worker(name, recv_queue, other_queue, third_queue):
    our_queue = QueueBuf(recv_queue)
    lc = 1
    ticks_per_second = 1.0/random.randint(1, 6)
    for tick in clock(ticks_per_second):
        try:
            (recieved_value, machine) = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None

        if recieved_value != None:
            lc = max(lc, recieved_value) + 1
            print "machine " + name + " recieved", machine, recieved_value, time.time(), lc

        else:
            die = random.randint(1, 10)
            if die == 1:
                lc += 1
                other_queue.put((lc, name))
                print "machine " + name + " sent (1)", time.time(), lc

            elif die == 2:
                lc += 1
                third_queue.put((lc, name))
                print "machine " + name + " sent (2)", time.time(), lc

            elif die == 3:
                lc += 1
                other_queue.put((lc, name))
                third_queue.put((lc, name))
                print "machine " + name + " sent (3)", time.time(), lc

            else:
                # internal event
                lc += 1
                print "machine " + name + " internal event", time.time(), lc

def without(elem, arr):
    return [x for x in arr if elem != x]

if __name__ == '__main__':
	# Create three queues
    qs = [multiprocessing.Queue() for i in range(3)]
    # Create three processes, and pass in the shared queues
    jobs = [multiprocessing.Process(target=worker,
        args=tuple([str(i), q] + without(q, qs)))
        for i, q in enumerate(qs)]

    # Start the jobs
    for j in jobs:
        j.start()

    # Wait for them to finish
    for j in jobs:
        j.join()
