import random
import multiprocessing
import time
import queue

def worker(q0, q1, q2):
    name = multiprocessing.current_process().name
    personal_queue, alt_queue1, alt_queue2 = 0,0,0
    clock_speed = 1.0/random.randint(1,6)
    if name == "0":
    	#q0.put(name)
        queue_wanted = q0
        alt_queue1 = q1
        alt_queue2 = q2
    elif name == "1":
    	#q1.put(name)
        queue_wanted = q0
        alt_queue1 = q1
        alt_queue2 = q2
    else:
    	#q2.put(name)
        queue_wanted = q0
        alt_queue1 = q1
        alt_queue2 = q2


    while True:
        timeleft = clock_speed
        queue_wanted.get(block=True, timeout=timeleft)







if __name__ == '__main__':
	# Create three queues
    q0 = multiprocessing.Queue()
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    # Create three processes, and pass in the shared queues
    jobs = [multiprocessing.Process(target=worker, name=str(i), args=(q0, q1, q2,)) for i in range(3)]

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