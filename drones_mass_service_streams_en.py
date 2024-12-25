import numpy as np
from matplotlib import pyplot as plt

# System parameters
n = 5  # Drones count
max_efficiency = 20  # Max efficiency for all drones, packets per second
queue_max_size = 20  # Max packet queues size, packets
R = 100  # Initial rate of incoming packets (arrivals), packets per second
# Initial drones processing speeds and queues
s = np.array([10, 15, 20, 12, 8])  # Processing speeds (power) of drones
print(f'Total productivity: {s.sum()}')
queues = np.zeros(n)  # Initial packet queues (all empty)

def distribute_tasks_with_queues(s, R, queues):
    n = len(s)
    p = np.zeros(n)
    remaining_R = R

    # Whichever drones have non-empty queues - their contents must processed first
    for i in range(n):
        if queues[i] > 0:
            # Determining how many packets are to be processed
            to_process = min(queues[i], s[i], max_efficiency)
            # Data is processed
            p[i] += to_process
            # As a consequence, this queue shortens
            queues[i] -= to_process

    # Distribute arriving packets among drones 
    for i in np.argsort(-s):  # Sorting drones by their processing power, starting with the most powerful ones
        if remaining_R <= 0:
            break
        # How much free space in this drone's queue?
        free_space = queue_max_size - queues[i]
        # How much unused power after taking data from the queue
        leftover_power = min((s[i] - p[i]), max_efficiency)
        # If no free space in the queue - this drone is a priori already busy
        if free_space > 0:
            # Max possible amount of packets for this drone, taking into account that it may be already be busy to some extent
            max_possible = min(max_efficiency, s[i] - p[i], remaining_R)
            # How many can be processed directly: since the queue size is larger than the power, 
            # data is rather put to processing directly
            direct_process = min(max_possible, free_space)
            p[i] += direct_process
            remaining_R -= direct_process
            # Add the remainder to the queue
            to_queue = min(remaining_R, free_space - direct_process)
            queues[i] += to_queue
            remaining_R -= to_queue

    return p, queues

queues_vals = []
processed_vals = []
r_vals = []

# Simulation over 100 seconds (iterations)
iterations = 100
for t in range(iterations):
    # Random fluctuations expressed as noise
    noise = np.random.uniform(-2, 2, size=n)
    s = np.clip(s + noise, 1, max_efficiency)  # Make sure s doesn't exceed max_efficiency

    # Random fluctuations of arrivals stream R
    R = max(50, R + np.random.randint(-10, 10))  # Random, but not below 50

    # Distribution of R among drones with individual packet queues
    p, queues = distribute_tasks_with_queues(s, R, queues)

    # Виведення результатів
    queues_vals.append(np.sum(queues) / n)
    processed_vals.append(np.sum(p))
    r_vals.append(R)

plt.figure(figsize=(12, 8))
plt.plot(range(iterations), r_vals, label='Arrival packet counts (R)')
plt.plot(range(iterations), queues_vals, label='Queues average fullness')
plt.plot(range(iterations), processed_vals, label='Processed values')
plt.legend()
plt.grid()
plt.show()