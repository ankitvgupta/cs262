# Run several jobs with default parameters (max_speed = 6, internal = 10, time_limit = 60)
python processes.py
sleep .1
python processes.py 
sleep .1
python processes.py 
sleep .1


# Change prob of internal process
python processes.py -internal 5
sleep .1
python processes.py -internal 15
sleep .1
python processes.py -internal 35
sleep .1



# Change maximum ticks per second
python processes.py -max_speed 3
sleep .1
python processes.py -max_speed 10
sleep .1
python processes.py -max_speed 20
sleep .1

# Try other combinations
python processes.py -max_speed 3 -internal 5
sleep .1
python processes.py -max_speed 3 -internal 15
sleep .1
python processes.py -max_speed 10 -internal 5
sleep .1
python processes.py -max_speed 10 -internal 15
sleep .1
python processes.py -max_speed 20 -internal 5
sleep .1
python processes.py -max_speed 20 -internal 15
sleep .1



