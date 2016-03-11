# Run several jobs with default parameters
python processes.py
python processes.py 
python processes.py 
python processes.py
python processes.py

# Change prob of internal process
python processes.py -internal 5
python processes.py -internal 5
python processes.py -internal 15
python processes.py -internal 15
python processes.py -internal 35
python processes.py -internal 35


# Change maximum ticks per second
python processes.py -max_speed 3
python processes.py -max_speed 3
python processes.py -max_speed 10
python processes.py -max_speed 10
python processes.py -max_speed 20
python processes.py -max_speed 20

# Try other combinations
python processes.py -max_speed 3 -internal 5
python processes.py -max_speed 3 -internal 15
python processes.py -max_speed 10 -internal 5
python processes.py -max_speed 10 -internal 15
python processes.py -max_speed 20 -internal 5
python processes.py -max_speed 20 -internal 15



