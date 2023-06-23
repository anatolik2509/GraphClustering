import matplotlib.pyplot as plt


def read_data(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        times = [list(map(float, line.rstrip('\n').split(','))) for line in lines]
        return times


def create_boxplot(data_array, algorithm_names, title):
    fig, ax = plt.subplots()
    plt.boxplot(data_array, labels=algorithm_names)
    plt.grid(visible=True, axis='y')
    plt.title(title)
    plt.margins(0.2)
    # plt.show()


def compare_sym_times(file_names, algorithm_names, title):
    data_for_vis = []
    for file_name in file_names:
        data = read_data(file_name)
        sym_times = [row[1] for row in data]
        data_for_vis.append(sym_times)
    create_boxplot(data_for_vis, algorithm_names, title)


if __name__ == '__main__':
    algorithms = ['weighted fluid', 'fluid', 'spin glass', 'fast greedy', 'walktrap']
    folder = '1_1_1'
    model = 'izh'
    files = [f'res/{folder}/weighted_fluid_{model}_reflect_arc.csv',
             f'res/{folder}/fluid_{model}_reflect_arc.csv',
             f'res/{folder}/spinglass_{model}_reflect_arc.csv',
             f'res/{folder}/fast_greedy_{model}_reflect_arc.csv',
             f'res/{folder}/walktrap_{model}_reflect_arc.csv',
             ]
    plot_title = f"Simulation time (cpu1=1.0, cpu2=1.0, cpu3=1.0, reflect arc, \nIzhikevich model)"
    compare_sym_times(files, algorithms, plot_title)
    plt.show()
