# import statements
import numpy as np
import os
import csv

# global simulation variables declaration
simulation_termination = -1
num_floors = num_elevators = elevator_capacity = max_customer_batch_size = -1
door_holding_time = inter_floor_travelling_time = door_opening_time = door_closing_time = -1
passenger_embarking_time = passenger_disembarking_time = -1
mean_inter_arrival_time = -1

# auxiliary functions definition
def generate_exponential_random_variate(exponential_scale_parameter):
    # generating uniform random variate
    # ref: https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html
    uniform_random_variate = np.random.uniform()
    assert 0 < uniform_random_variate < 1, 'Unexpected uniform_random_variate generated.'

    # generating and returning exponential random variate with provided mean
    return -1 * exponential_scale_parameter * np.log(uniform_random_variate)

def run_elevator_system_simulation():
    assert simulation_termination > 0, 'Invalid simulation_termination detected.'

    assert num_floors > 1, 'Invalid num_floors detected.'
    assert num_elevators > 0, 'Invalid num_elevators detected.'
    assert elevator_capacity > 0, 'Invalid elevator_capacity detected.'
    assert max_customer_batch_size > 0, 'Invalid max_customer_batch_size detected.'

    assert door_holding_time >= 0, 'Invalid door_holding_time detected.'
    assert inter_floor_travelling_time >= 0, 'Invalid inter_floor_travelling_time detected.'
    assert door_opening_time >= 0, 'Invalid door_opening_time detected.'
    assert door_closing_time >= 0, 'Invalid door_closing_time detected.'

    assert passenger_embarking_time >= 0, 'Invalid passenger_embarking_time detected.'
    assert passenger_disembarking_time >= 0, 'Invalid passenger_disembarking_time detected.'

    assert mean_inter_arrival_time > 0, 'Invalid mean_inter_arrival_time detected.'

    # step-1: initializing local simulation variables
    num_customers_serviced = 0

    avg_queue_length = avg_delay_time = avg_elevator_time = avg_delivery_time = 0
    max_queue_length = max_delay_time = max_elevator_time = max_delivery_time = 0

    list_avg_load_size = [0] * num_elevators
    list_num_departs = [0] * num_elevators
    list_percentage_operation_time = [0] * num_elevators
    list_num_max_loads = [0] * num_elevators
    list_num_stops = [0] * num_elevators

    num_customers_waited = 0

    current_customer_batch_size = 0

    current_customer_index = 0
    list_destination_floor = list()
    list_delivery_time = list()
    list_delay_time = list()

    # step-2 & step-3: setting up local simulation variables for first customer and elevators

    # determining batch size for arrival of new customers (from binomial probability distribution)
    # ref: https://numpy.org/doc/stable/reference/random/generated/numpy.random.binomial.html

    # choosing destination floor for new customer (from discrete uniform probability distribution)
    # ref: https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html

    if current_customer_batch_size == 0:
        current_customer_batch_size = 1 + np.random.binomial(n=(max_customer_batch_size - 1), p=0.5)
        inter_arrival_time = generate_exponential_random_variate(mean_inter_arrival_time)
    else:
        inter_arrival_time = 0

    current_customer_index = current_customer_index + 1
    current_customer_batch_size = current_customer_batch_size - 1

    simulation_clock = inter_arrival_time
    list_elevator_available_clock_times = [simulation_clock] * num_elevators

    list_destination_floor.append(np.random.randint(low=2, high=(num_floors + 1)))
    list_delivery_time.append(15)
    list_delay_time.append(0)

    # step-4: getting started with elevator system simulation
    elevator_loaded_with_no_one_in_queue = False
    elevator_loaded_with_customers_waiting_in_queue = False

    starting_time_of_current_queue = current_queue_length = first_customer_index_in_current_queue = -1
    current_elevator_index = customer_occupancy_in_current_elevator = -1
    floor_selection_vector = floor_counting_vector = list()
    first_customer_index_in_current_elevator = last_customer_index_in_current_elevator = -1

    while simulation_clock <= simulation_termination or elevator_loaded_with_no_one_in_queue or elevator_loaded_with_customers_waiting_in_queue:
        # step-5: selecting first available elevator
        if not elevator_loaded_with_no_one_in_queue and not elevator_loaded_with_customers_waiting_in_queue:
            current_elevator_index = -1

            for i in range(num_elevators):
                if list_elevator_available_clock_times[i] <= simulation_clock:
                    current_elevator_index = i
                    break

        # step-6 ~ step-32: running elevator system simulation for different scenarios
        if current_elevator_index == -1:
            # step-19: initializing queue of customers waiting for elevator service
            if not elevator_loaded_with_customers_waiting_in_queue:
                first_customer_index_in_current_queue = current_customer_index
                starting_time_of_current_queue = simulation_clock
                current_queue_length = 1
                list_delay_time[current_customer_index - 1] = simulation_clock

            # step-20 ~ step-21: waiting and receiving new customers until an elevator is available for service
            elevator_loaded_with_customers_waiting_in_queue = False

            while True:
                # step-20: getting new customer and setting up local simulation variables for new customer
                if current_customer_batch_size == 0:
                    current_customer_batch_size = 1 + np.random.binomial(n=(max_customer_batch_size - 1), p=0.5)
                    inter_arrival_time = generate_exponential_random_variate(mean_inter_arrival_time)
                else:
                    inter_arrival_time = 0

                current_customer_index = current_customer_index + 1
                current_customer_batch_size = current_customer_batch_size - 1

                simulation_clock = simulation_clock + inter_arrival_time

                list_destination_floor.append(np.random.randint(low=2, high=(num_floors + 1)))
                list_delivery_time.append(15)
                list_delay_time.append(simulation_clock)

                avg_queue_length = avg_queue_length + current_queue_length * (simulation_clock - starting_time_of_current_queue)
                starting_time_of_current_queue = simulation_clock
                current_queue_length = current_queue_length + 1

                for i in range(num_elevators):
                    list_elevator_available_clock_times[i] = simulation_clock if list_elevator_available_clock_times[i] <= simulation_clock else list_elevator_available_clock_times[i]

                # step-21: checking for elevator availability
                current_elevator_index = -1

                for i in range(num_elevators):
                    if list_elevator_available_clock_times[i] <= simulation_clock:
                        current_elevator_index = i
                        break

                if current_elevator_index != -1:
                    break

            # step-22 & step-23: setting up local simulation variables for current queue and current elevator
            floor_selection_vector = [0] * num_floors
            floor_counting_vector = [0] * num_floors
            remaining_customers_in_queue = current_queue_length - elevator_capacity

            if remaining_customers_in_queue <= 0:
                last_customer_index_in_current_elevator = current_customer_index
                customer_occupancy_in_current_elevator = current_queue_length
            else:
                last_customer_index_in_current_elevator = first_customer_index_in_current_queue + (elevator_capacity - 1)
                customer_occupancy_in_current_elevator = elevator_capacity

            # step-24: loading customers onto current elevator
            for i in range(first_customer_index_in_current_queue - 1, last_customer_index_in_current_elevator):
                floor_selection_vector[list_destination_floor[i] - 1] = 1
                floor_counting_vector[list_destination_floor[i] - 1] = floor_counting_vector[list_destination_floor[i] - 1] + 1

            # step-25, step-26 & step-27: calculating and updating local simulation variables for current queue
            max_queue_length = max_queue_length if max_queue_length > current_queue_length else current_queue_length

            num_customers_serviced = num_customers_serviced + customer_occupancy_in_current_elevator
            num_customers_waited = num_customers_waited + customer_occupancy_in_current_elevator

            max_waiting_time = -1

            for i in range(first_customer_index_in_current_queue - 1, last_customer_index_in_current_elevator):
                list_delay_time[i] = (simulation_clock - list_delay_time[i])
                avg_delay_time = avg_delay_time + list_delay_time[i]

                if list_delay_time[i] > max_waiting_time:
                    max_waiting_time = list_delay_time[i]

            max_delay_time = max_delay_time if max_delay_time > max_waiting_time else max_waiting_time

            # step-28 & step-29: calculating and updating local simulation variables for passengers on current elevator
            first_customer_index_in_current_elevator = first_customer_index_in_current_queue

            for i in range(first_customer_index_in_current_elevator - 1, last_customer_index_in_current_elevator):
                list_delivery_time[i] = list_delivery_time[i] + list_delay_time[i]

            simulation_clock = simulation_clock + passenger_embarking_time

            for i in range(num_elevators):
                list_elevator_available_clock_times[i] = simulation_clock if list_elevator_available_clock_times[i] <= simulation_clock else list_elevator_available_clock_times[i]

            # step-30: deciding on how to proceed with later part of simulation
            if remaining_customers_in_queue <= 0:
                avg_queue_length = avg_queue_length + current_queue_length * (simulation_clock - starting_time_of_current_queue)
                current_queue_length = 0
                elevator_loaded_with_no_one_in_queue = True
            else:
                avg_queue_length = avg_queue_length + current_queue_length * (simulation_clock - starting_time_of_current_queue)
                starting_time_of_current_queue = simulation_clock
                current_queue_length = remaining_customers_in_queue
                elevator_loaded_with_customers_waiting_in_queue = True

                # step-31 & step-32: updating first_customer_index_in_current_queue
                first_customer_index_in_current_queue = last_customer_index_in_current_elevator + 1
        else:
            if not elevator_loaded_with_customers_waiting_in_queue:
                # step-6: setting up local simulation variables for current elevator
                if not elevator_loaded_with_no_one_in_queue:
                    first_customer_index_in_current_elevator = current_customer_index
                    customer_occupancy_in_current_elevator = 0
                    floor_selection_vector = [0] * num_floors
                    floor_counting_vector = [0] * num_floors

                # step-7 ~ step-10: allowing new customers to embark on current elevator
                while True:
                    # step-7: loading current customer and setting up local simulation variables for current customer
                    if not elevator_loaded_with_no_one_in_queue:
                        customer_occupancy_in_current_elevator = customer_occupancy_in_current_elevator + 1
                        floor_selection_vector[list_destination_floor[current_customer_index - 1] - 1] = 1
                        floor_counting_vector[list_destination_floor[current_customer_index - 1] - 1] = floor_counting_vector[list_destination_floor[current_customer_index - 1] - 1] + 1

                        num_customers_serviced = num_customers_serviced + 1
                        simulation_clock = simulation_clock + passenger_embarking_time

                        for i in range(num_elevators):
                            list_elevator_available_clock_times[i] = simulation_clock if list_elevator_available_clock_times[i] <= simulation_clock else list_elevator_available_clock_times[i]

                    # step-8: getting new customer and setting up local simulation variables for new customer
                    elevator_loaded_with_no_one_in_queue = False

                    if current_customer_batch_size == 0:
                        current_customer_batch_size = 1 + np.random.binomial(n=(max_customer_batch_size - 1), p=0.5)
                        inter_arrival_time = generate_exponential_random_variate(mean_inter_arrival_time)
                    else:
                        inter_arrival_time = 0

                    current_customer_index = current_customer_index + 1
                    current_customer_batch_size = current_customer_batch_size - 1

                    simulation_clock = simulation_clock + inter_arrival_time

                    list_destination_floor.append(np.random.randint(low=2, high=(num_floors + 1)))
                    list_delivery_time.append(15)
                    list_delay_time.append(0)

                    # step-9: setting all available elevators' available clock time to current clock time
                    for i in range(num_elevators):
                        list_elevator_available_clock_times[i] = simulation_clock if list_elevator_available_clock_times[i] <= simulation_clock else list_elevator_available_clock_times[i]

                    # step-10: deciding on whether to allow current customer to embark on current elevator
                    if inter_arrival_time <= door_holding_time and customer_occupancy_in_current_elevator < elevator_capacity:
                        for i in range(first_customer_index_in_current_elevator - 1, current_customer_index - 1):
                            list_delivery_time[i] = list_delivery_time[i] + inter_arrival_time + passenger_embarking_time
                    else:
                        break

                # step-10: sending off current elevator
                last_customer_index_in_current_elevator = current_customer_index - 1

            # step-11: getting started with delivering passengers on current elevator to destination floors
            for i in range(first_customer_index_in_current_elevator - 1, last_customer_index_in_current_elevator):
                # step-12, step-13, step-14, step-15 & step-16: calculating elevator_time and delivery_time for the customer
                floor_displacement = list_destination_floor[i] - 1

                elevator_time = inter_floor_travelling_time * floor_displacement
                elevator_time = elevator_time + (door_opening_time + door_closing_time) * sum(floor_selection_vector[: floor_displacement])
                elevator_time = elevator_time + passenger_disembarking_time * sum(floor_counting_vector[: floor_displacement])
                elevator_time = elevator_time + door_opening_time + passenger_disembarking_time

                avg_elevator_time = avg_elevator_time + elevator_time
                max_elevator_time = max_elevator_time if max_elevator_time > elevator_time else elevator_time

                list_delivery_time[i] = list_delivery_time[i] + elevator_time
                avg_delivery_time = avg_delivery_time + list_delivery_time[i]
                max_delivery_time = max_delivery_time if max_delivery_time > list_delivery_time[i] else list_delivery_time[i]

            # step-17 & step-18: calculating and updating local simulation variables for current elevator
            list_avg_load_size[current_elevator_index] = list_avg_load_size[current_elevator_index] + customer_occupancy_in_current_elevator
            list_num_departs[current_elevator_index] = list_num_departs[current_elevator_index] + 1

            highest_floor_visited = -1

            for i in range(num_floors - 1, -1, -1):
                if floor_selection_vector[i] == 1:
                    highest_floor_visited = i
                    break

            operation_time = 2 * highest_floor_visited * inter_floor_travelling_time
            operation_time = operation_time + (door_opening_time + door_closing_time) * sum(floor_selection_vector)
            operation_time = operation_time + passenger_disembarking_time * sum(floor_counting_vector)

            list_elevator_available_clock_times[current_elevator_index] = simulation_clock + operation_time
            list_percentage_operation_time[current_elevator_index] = list_percentage_operation_time[current_elevator_index] + operation_time

            list_num_max_loads[current_elevator_index] = list_num_max_loads[current_elevator_index] + (0 if customer_occupancy_in_current_elevator < elevator_capacity else 1)
            list_num_stops[current_elevator_index] = list_num_stops[current_elevator_index] + sum(floor_selection_vector)

            if elevator_loaded_with_customers_waiting_in_queue:
                current_elevator_index = -1
                elevator_loaded_with_customers_waiting_in_queue = not simulation_clock > simulation_termination

    # step-33, step-34, step-35 & step-36: calculating performance measures for this run of simulation
    # ref: https://www.geeksforgeeks.org/python-dividing-two-lists/
    # ref: https://stackoverflow.com/questions/8244915/how-do-you-divide-each-element-in-a-list-by-an-int/8247234
    performance_measures = dict()

    performance_measures['Number of Customers Serviced'] = num_customers_serviced

    performance_measures['Avg Queue Length'] = avg_queue_length / simulation_clock
    performance_measures['Max Queue Length'] = max_queue_length
    performance_measures['Avg Delay Time'] = avg_delay_time / num_customers_waited if num_customers_waited > 0 else 0
    performance_measures['Max Delay Time'] = max_delay_time
    performance_measures['Avg Elevator Time'] = avg_elevator_time / num_customers_serviced
    performance_measures['Max Elevator Time'] = max_elevator_time
    performance_measures['Avg Delivery Time'] = avg_delivery_time / num_customers_serviced
    performance_measures['Max Delivery Time'] = max_delivery_time

    performance_measures['Avg Load Size'] = [avg_load_size / num_departs for avg_load_size, num_departs in zip(list_avg_load_size, list_num_departs)]
    performance_measures['Percentage Operation Time'] = [100 * percentage_operation_time / simulation_clock for percentage_operation_time in list_percentage_operation_time]
    performance_measures['Percentage Available Time'] = [100 * (1 - percentage_operation_time / simulation_clock) for percentage_operation_time in list_percentage_operation_time]
    performance_measures['Number of Maximum Loads'] = list_num_max_loads
    performance_measures['Number of Total Stops'] = list_num_stops

    return performance_measures

# main function definition
def main():
    global simulation_termination, \
        num_floors, num_elevators, elevator_capacity, max_customer_batch_size, \
        door_holding_time, inter_floor_travelling_time, door_opening_time, door_closing_time, \
        passenger_embarking_time, passenger_disembarking_time, \
        mean_inter_arrival_time

    # reading inputs from input_file
    with open('./inputdir/inputs.txt', 'r') as input_file:
        inputs = input_file.read().split('\n')

    # assigning values from input_file to global simulation variables
    # ref: https://stackoverflow.com/questions/48841186/how-to-take-n-numbers-as-input-in-single-line-in-python
    simulation_termination = float(inputs[0])
    num_floors, num_elevators, elevator_capacity, max_customer_batch_size = tuple(map(int, inputs[1].split()))
    door_holding_time, inter_floor_travelling_time, door_opening_time, door_closing_time = tuple(map(float, inputs[2].split()))
    passenger_embarking_time, passenger_disembarking_time = tuple(map(float, inputs[3].split()))
    mean_inter_arrival_time = 60 * float(inputs[4])  # converting from minute to second

    # running multiple-server queueing system simulation
    num_simulations = 3
    performance_measures = list()

    for i in range(num_simulations):
        print(f'Running simulation run no.{i + 1}/{num_simulations}')
        performance_measures.append(run_elevator_system_simulation())

    # generating result presenting statistics on num_simulations runs of simulation
    # ref: https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
    # ref: https://www.geeksforgeeks.org/writing-csv-files-in-python/
    if not os.path.exists('./outputdir'):
        os.makedirs('./outputdir')

    dictionary_keys = list(performance_measures[0].keys())
    result_rows = list()

    for i in range(num_simulations):
        result_rows.append([i + 1] + [round(performance_measures[i][key], 2) for key in dictionary_keys[: 9]])

    with open('./outputdir/customer_statistics.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Simulation Run'] + dictionary_keys[: 9])
        csv_writer.writerows(result_rows)

    for i in range(num_elevators):
        result_rows = list()

        for j in range(num_simulations):
            result_rows.append([j + 1] + [round(performance_measures[j][key][i], 2) for key in dictionary_keys[9:]])

        with open(f'./outputdir/elevator{i + 1}_statistics.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Simulation Run'] + dictionary_keys[9:])
            csv_writer.writerows(result_rows)

if __name__ == '__main__':
    main()
