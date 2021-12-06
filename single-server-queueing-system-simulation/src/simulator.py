# import statements
from queue import Queue
import math
import numpy as np
import os
from matplotlib import pyplot as plt
import csv
import statistics

# components and organization of a discrete-event simulation model

# system states
# ref: https://www.geeksforgeeks.org/queue-in-python/
server_status = False  # False = idle, True = busy
number_in_queue = 0
times_of_arrival = Queue()
time_of_last_event = 0

# simulation_clock
simulation_clock = 0

# random variates lists
uniform_random_variates = []
exponential_random_variates_with_mean_inter_arrival_time = []
exponential_random_variates_with_mean_service_time = []

# event list
# ref: https://www.geeksforgeeks.org/python-infinity/
next_arrival_event = math.inf
next_departure_event = math.inf

# statistical counters
number_delayed = 0
total_delay = 0
area_under_Qt = 0
area_under_Bt = 0

# additional system states
customer_arrived = 0

def initialization_routine(mean_inter_arrival_time):
    global server_status, number_in_queue, times_of_arrival, time_of_last_event, \
        simulation_clock, \
        uniform_random_variates, exponential_random_variates_with_mean_inter_arrival_time, exponential_random_variates_with_mean_service_time, \
        next_arrival_event, next_departure_event, \
        number_delayed, total_delay, area_under_Qt, area_under_Bt, \
        customer_arrived

    # system states
    server_status = False
    number_in_queue = 0
    times_of_arrival = Queue()
    time_of_last_event = 0

    # simulation_clock
    simulation_clock = 0

    # random variates lists
    uniform_random_variates = []
    exponential_random_variates_with_mean_inter_arrival_time = []
    exponential_random_variates_with_mean_service_time = []

    # event list
    # ref: https://www.w3schools.com/python/python_variables_global.asp
    next_arrival_event = library_routine(mean_inter_arrival_time)
    next_departure_event = math.inf

    exponential_random_variates_with_mean_inter_arrival_time.append(next_arrival_event)

    # statistical counters
    number_delayed = 0
    total_delay = 0
    area_under_Qt = 0
    area_under_Bt = 0

    # additional system states
    customer_arrived = 1

def timing_routine():
    global simulation_clock

    if next_arrival_event < next_departure_event:
        simulation_clock = next_arrival_event
        return 1  # 1 = arrival event
    else:
        simulation_clock = next_departure_event
        return 2  # 2 = departure event

def arrival_routine(mean_inter_arrival_time, mean_service_time, number_of_customers):
    global server_status, number_in_queue, times_of_arrival, time_of_last_event, \
        exponential_random_variates_with_mean_inter_arrival_time, exponential_random_variates_with_mean_service_time, \
        next_arrival_event, next_departure_event, \
        number_delayed, total_delay, area_under_Qt, area_under_Bt, \
        customer_arrived

    if customer_arrived < number_of_customers:
        A = library_routine(mean_inter_arrival_time)
        next_arrival_event = simulation_clock + A
        exponential_random_variates_with_mean_inter_arrival_time.append(A)

        customer_arrived = customer_arrived + 1
    else:
        next_arrival_event = math.inf

    if server_status:
        area_under_Qt = area_under_Qt + number_in_queue * (simulation_clock - time_of_last_event)
        area_under_Bt = area_under_Bt + (simulation_clock - time_of_last_event)

        number_in_queue = number_in_queue + 1
        assert number_in_queue <= number_of_customers, 'The queue is full.'
        times_of_arrival.put(simulation_clock)
        time_of_last_event = simulation_clock
    else:
        total_delay = total_delay + 0
        number_delayed = number_delayed + 1
        server_status = True

        B = library_routine(mean_service_time)
        next_departure_event = simulation_clock + B
        exponential_random_variates_with_mean_service_time.append(B)

        time_of_last_event = simulation_clock

def departure_routine(mean_service_time):
    global server_status, number_in_queue, times_of_arrival, time_of_last_event, \
        exponential_random_variates_with_mean_service_time, \
        next_departure_event, \
        number_delayed, total_delay, area_under_Qt, area_under_Bt

    if number_in_queue == 0:
        area_under_Bt = area_under_Bt + (simulation_clock - time_of_last_event)

        server_status = False
        next_departure_event = math.inf
        time_of_last_event = simulation_clock
    else:
        area_under_Qt = area_under_Qt + number_in_queue * (simulation_clock - time_of_last_event)
        area_under_Bt = area_under_Bt + (simulation_clock - time_of_last_event)

        number_in_queue = number_in_queue - 1
        total_delay = total_delay + (simulation_clock - times_of_arrival.get())
        number_delayed = number_delayed + 1

        B = library_routine(mean_service_time)
        next_departure_event = simulation_clock + B
        exponential_random_variates_with_mean_service_time.append(B)

        time_of_last_event = simulation_clock

def library_routine(exponential_probability_distribution_mean):
    global uniform_random_variates

    # ref: https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html
    uniform_random_variate = np.random.uniform(low=0, high=1)

    # ref: https://www.w3schools.com/python/ref_keyword_assert.asp
    assert 0 < uniform_random_variate < 1, 'Invalid uniform random variate generated.'
    uniform_random_variates.append(uniform_random_variate)

    # ref: https://www.geeksforgeeks.org/numpy-log-python/
    return -1 * exponential_probability_distribution_mean * np.log(uniform_random_variate)

def report_generator(write_output_to_file=True):
    average_delay_in_queue = total_delay / number_delayed
    average_number_in_queue = area_under_Qt / time_of_last_event
    server_utilization = area_under_Bt / time_of_last_event
    time_simulation_ended = time_of_last_event

    if write_output_to_file:
        if not os.path.exists('./outputdir'):
            os.makedirs('./outputdir')

        with open('./outputdir/outputs.txt', 'w') as outputs_txt:
            outputs_txt.write(
                f'Average delay in queue: {format(average_delay_in_queue, ".3f")} minutes\n'
                f'Average number in queue: {format(average_number_in_queue, ".3f")}\n'
                f'Server utilization: {format(server_utilization, ".3f")}\n'
                f'Time simulation ended: {format(time_simulation_ended, ".3f")} minutes'
            )

    return (
        average_delay_in_queue,
        average_number_in_queue,
        server_utilization,
        time_simulation_ended
    )

def main_program(mean_inter_arrival_time, mean_service_time, number_of_customers, write_output_to_file=True):
    # invoking initialization_routine
    initialization_routine(mean_inter_arrival_time)

    while number_delayed < number_of_customers:
        # invoking timing_routine
        event_type = timing_routine()
        assert event_type == 1 or event_type == 2, 'Invalid event type encountered.'

        # invoking event_routine
        if event_type == 1:
            # arrival of a customer
            arrival_routine(mean_inter_arrival_time, mean_service_time, number_of_customers)
        elif event_type == 2:
            # departure of a customer
            departure_routine(mean_service_time)

    # invoking report_generator
    return report_generator(write_output_to_file=write_output_to_file)

# helping function definition
def plot_histogram(list_random_variates, bins, color, cumulative, title):
    plt.figure(figsize=(9, 9))
    plt.hist(
        list_random_variates,
        bins=bins,
        color=color,
        edgecolor='white',
        cumulative=cumulative
    )
    plt.title(f'{"Cumulative " if cumulative else ""}Frequency Histogram for {title}')
    plt.xlabel('Random Variates')
    plt.ylabel(f'{"Cumulative " if cumulative else ""}Frequency')
    plt.show()

# main function definition
def main():
    # reading inputs from inputs_txt
    with open('./inputdir/inputs.txt', 'r') as inputs_txt:
        inputs = inputs_txt.read().split('\n')

    mean_inter_arrival_time = float(inputs[0])
    mean_service_time = float(inputs[1])
    number_of_customers = int(inputs[2])

    assert mean_inter_arrival_time > mean_service_time, 'mean_inter_arrival_time not greater than mean_service_time.'
    assert number_of_customers > 0, 'Invalid number_of_customers received.'

    # task(a): running single-server queueing system simulation for provided mean_inter_arrival_time and mean_service_time
    main_program(mean_inter_arrival_time, mean_service_time, number_of_customers, write_output_to_file=True)

    # saving generated uniform & exponential random variates in separate lists
    list_uniform = uniform_random_variates
    list_inter_arrival_exp = exponential_random_variates_with_mean_inter_arrival_time
    list_service_exp = exponential_random_variates_with_mean_service_time

    print('Task(a) completed.')

    # task(b): running single-server queueing system simulation for different values of mean_service_time
    # ref: https://www.geeksforgeeks.org/writing-csv-files-in-python/
    fields = ['k', 'Average delay in queue (minutes)', 'Average number in queue', 'Server utilization', 'Time simulation ended (minutes)']
    rows = []

    # running simulation for different values of mean_service_time and storing stats
    k_values = [0.5, 0.6, 0.7, 0.8, 0.9]

    for k_value in k_values:
        (
            average_delay_in_queue,
            average_number_in_queue,
            server_utilization,
            time_simulation_ended
        ) = main_program(
            mean_inter_arrival_time,
            k_value * mean_inter_arrival_time,
            number_of_customers,
            write_output_to_file=False
        )
        rows.append([k_value, average_delay_in_queue, average_number_in_queue, server_utilization, time_simulation_ended])

    # writing stats to stats.csv
    if not os.path.exists('./outputdir'):
        os.makedirs('./outputdir')

    with open('./outputdir/stats.csv', 'w') as stats_csv:
        csv_writer = csv.writer(stats_csv)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)

    print('Task(b) completed.')

    # task(c): displaying statistics for generated uniform and exponential random variates during task(a)

    # writing statistics to stats.txt
    # ref: https://www.geeksforgeeks.org/python-statistics-median/
    with open('./outputdir/stats.txt', 'w') as stats_txt:
        stats_txt.write(
            f'Uniform random variates ({len(list_uniform)} generated)\n'
            f'Min: {min(list_uniform)}\n'
            f'Max: {max(list_uniform)}\n'
            f'Median: {statistics.median(list_uniform)}\n\n'
            f'Exponential random variates with mean_inter_arrival_time ({len(list_inter_arrival_exp)} generated)\n'
            f'Min: {min(list_inter_arrival_exp)}\n'
            f'Max: {max(list_inter_arrival_exp)}\n'
            f'Median: {statistics.median(list_inter_arrival_exp)}\n\n'
            f'Exponential random variates with mean_service_time ({len(list_service_exp)} generated)\n'
            f'Min: {min(list_service_exp)}\n'
            f'Max: {max(list_service_exp)}\n'
            f'Median: {statistics.median(list_service_exp)}'
        )

    # plotting histograms on frequency & cumulative frequency for generated random variates
    # ref: https://www.kite.com/python/answers/how-to-set-the-bin-size-of-a-matplotlib-histogram-in-python
    # ref: https://matplotlib.org/stable/gallery/statistics/histogram_cumulative.html
    bins_uniform = np.arange(0, 1.1, 0.1)
    bins_inter_arrival_exp = [
            0,
            mean_inter_arrival_time / 4,
            mean_inter_arrival_time / 2,
            3 * mean_inter_arrival_time / 4,
            mean_inter_arrival_time,
            4 * mean_inter_arrival_time / 3,
            5 * mean_inter_arrival_time / 3,
            2 * mean_inter_arrival_time,
            5 * mean_inter_arrival_time / 2,
            3 * mean_inter_arrival_time,
            4 * mean_inter_arrival_time
        ]
    bins_service_exp = [
            0,
            mean_service_time / 4,
            mean_service_time / 2,
            3 * mean_service_time / 4,
            mean_service_time,
            4 * mean_service_time / 3,
            5 * mean_service_time / 3,
            2 * mean_service_time,
            5 * mean_service_time / 2,
            3 * mean_service_time,
            4 * mean_service_time
        ]

    plot_histogram(list_uniform, bins_uniform, 'crimson', False, 'Uniform Random Variates')
    plot_histogram(list_uniform, bins_uniform, 'goldenrod', True, 'Uniform Random Variates')
    plot_histogram(list_inter_arrival_exp, bins_inter_arrival_exp, 'fuchsia', False, 'Exponential Random Variates with mean_inter_arrival_time')
    plot_histogram(list_inter_arrival_exp, bins_inter_arrival_exp, 'indigo', True, 'Exponential Random Variates with mean_inter_arrival_time')
    plot_histogram(list_service_exp, bins_service_exp, 'limegreen', False, 'Exponential Random Variates with mean_service_time')
    plot_histogram(list_service_exp, bins_service_exp, 'darkcyan', True, 'Exponential Random Variates with mean_service_time')

    print('Task(c) completed.')


# ref: https://www.geeksforgeeks.org/python-main-function/
if __name__ == "__main__":
    main()
