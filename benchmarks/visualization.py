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
    config_set = [[20, 30],
                  [50, 80],
                  [100, 200],
                  [300, 900]]
    folders = ['1_1_1', '05_1', '05_05_1']
    algorithms = ['weighted fluid', 'fluid', 'spin glass', 'fast greedy', 'walktrap']
    folder = '1_1_1'
    files = [f'res/{folder}/weighted_fluid_reflect_arc.csv',
             f'res/{folder}/fluid_reflect_arc.csv',
             f'res/{folder}/spinglass_reflect_arc.csv',
             f'res/{folder}/fast_greedy_reflect_arc.csv',
             f'res/{folder}/walktrap_reflect_arc.csv',
             ]
    plot_title = f"Simulation time (cpu1=1.0, cpu2=1.0, cpu3=1.0, reflect arc, \nIzhikevich model)"
    compare_sym_times(files, algorithms, plot_title)
    plt.savefig(f'fig/{folder}__izh_reflect_arc.png')
    # for folder in folders:
    #     for config in config_set:
    #         files = [f'res/{folder}/weighted_fluid_{config[0]}_{config[1]}.csv',
    #                  f'res/{folder}/fluid_{config[0]}_{config[1]}.csv',
    #                  f'res/{folder}/spin_glass_{config[0]}_{config[1]}.csv',
    #                  f'res/{folder}/fast_greedy_{config[0]}_{config[1]}.csv',
    #                  f'res/{folder}/walktrap_{config[0]}_{config[1]}.csv']
    #         algorithms = ['weighted fluid', 'fluid', 'spin glass', 'fast greedy', 'walktrap']
    #         plot_title = f"Simulation time (vertex = {config[0]}, edges = {config[1]})"
    #         compare_sym_times(files, algorithms, plot_title)
    #         plt.savefig(f'fig/{folder}__{config[0]}_{config[1]}.png')
