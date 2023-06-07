from statistics import mean
import matplotlib.pyplot as plt

from benchmarks.utils import read_data


def read_mean_sym_time(file):
    data = read_data(file)
    sym_times = [row[1] for row in data]
    return mean(sym_times)


def create_plot(file_template, algorithms, models):
    bar_width = 0.2
    x_step = bar_width * (len(models) + 1)
    x_poses = [x_step * i for i in range(len(algorithms))]
    colors = ['blue', 'red']
    for i, model in enumerate(models):
        x = []
        y = []
        for j, alg in enumerate(algorithms):
            sym_time = read_mean_sym_time(file_template.format(alg, model))
            x.append(x_step * j + i * bar_width)
            y.append(sym_time)
        plt.bar(x, y, color=colors[i], width=bar_width, edgecolor='grey', label=model)
    plt.xlabel('Algorithm')
    plt.ylabel('Simulation time (secs.)')
    print(x_poses)
    plt.xticks([r + bar_width / 2 for r in x_poses], algorithms)
    plt.legend()
    plt.title('Compairing ESRN and Izhikevich(cpu1=1, cpu2=1, cpu3=1')
    plt.savefig('fig/esrn_izh_1_1_1.png', dpi=500)


if __name__ == '__main__':
    algs = ['weighted_fluid', 'fluid', 'spinglass', 'fast_greedy', 'walktrap']
    input_models = ['esrn', 'izh']
    create_plot('res/1_1_1/{}_{}_reflect_arc.csv', algs, input_models)
