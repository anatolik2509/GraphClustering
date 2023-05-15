def write_time_to_file(elapsed_times, sim_elapsed_time, file_name):
    with open(file_name, 'w+') as file:
        for time, sim_time in zip(elapsed_times, sim_elapsed_time):
            file.write(f'{time},{sim_time}' + '\n')


def write_logs_to_file(logs, file_name):
    with open(file_name, 'w+') as file:
        for line in logs:
            file.write(line + '\n')
