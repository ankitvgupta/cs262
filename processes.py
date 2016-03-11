import random
import multiprocessing
from multiprocessing import Queue
import time

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

# class QueueBuf(object):
#     def __init__(self, ipc_queue):
#         pass

#     def get_nowait():
#         pass

#     def qsize():
#         pass

def QueueBuf(ipc_queue):
    return ipc_queue


def worker(name, recv_queue, other_queue, third_queue):
    our_queue = QueueBuf(recv_queue)
    lc = 1
    for tick in clock(ticks_per_second):
        try:
            recieved_value = our_queue.get_nowait()
        except Queue.Empty:
            recieved_value = None

        if recieved_value != None:
            lc = max(lc, recieved_value) + 1
            print "machine " + name + " recieved", time.time(), lc

        else:
            die = random.randint(1, 10)
            if die == 1:
                other_queue.put(lc)
                lc += 1
                print "machine " + name + " sent (1)", time.time(), lc

            else if die == 2:
                third_queue.put(lc)
                lc += 1
                print "machine " + name + " sent (2)", time.time(), lc

            else if die == 3:
                other_queue.put(lc)
                third_queue.put(lc)
                lc += 1
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
        args=tuple(str(i), q, *without(q, qs))
        for i, q in enumerate(qs)]

    # Start the jobs
    for j in jobs:
        j.start()

    # Wait for them to finish
    for j in jobs:
        j.join()
