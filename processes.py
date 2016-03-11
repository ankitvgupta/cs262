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


# if __name__ == '__main__':
#     for tick in clock(1):
#         print time.time()
#         time.sleep(0.5)

class QueueBuf(object):
    def __init__(self, ipc_queue):
        self.ipc_queue = ipc_queue
        self.queue = Queue.Queue()

    def get_nowait():
        while not self.ipc_queue.empty():
            self.queue.put(self.ipc_queue.get_nowait())
        return self.queue.get_nowait()

    def qsize():
        return self.queue.qsize()

#def QueueBuf(ipc_queue):
#    return ipc_queue


def worker(our_queue, other_queue, third_queue):
    our_queue = QueueBuf(our_queue)
    lc = 1
    for tick in clock(ticks_per_second):
        try:
            recieved_value = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None

        if recieved_value != None:
            print recieved_value,




def without(elem, arr):
    return [x for x in arr if elem != x]



if __name__ == '__main__':
	# Create three queues
    qs = [multiprocessing.Queue() for i in range(3)]
    # Create three processes, and pass in the shared queues
    jobs = [multiprocessing.Process(target=worker, args=tuple(q, *without(q, qs)) for q in qs]

    # Start the jobs
    for j in jobs:
        j.start()

    # Wait for them to finish
    for j in jobs:
        j.join()

    # Print what is in the queues
    print "Q0"
    while not q0.empty():
    	print q0.get()
    print "Q1"
    while not q1.empty():
    	print q1.get()
    print "Q2"
    while not q2.empty():
    	print q2.get()