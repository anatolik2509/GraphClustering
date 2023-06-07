import matplotlib.pyplot as plt
import numpy as np


def read_data(file_name):
    with open(file_name) as file:
        x_len, y_len = map(int, file.readline().split(' '))
        x = np.zeros((x_len, y_len))
        y = np.zeros((x_len, y_len))
        z = np.zeros((x_len, y_len))
        x[2, 3] = 1
        print(x)
        x_curr = 0
        y_curr = 0
        for line in file:
            hosts, nodes, et = line.rstrip().split(',')
            hosts = int(hosts)
            nodes = int(nodes)
            et = float(et)
            x[x_curr, y_curr] = hosts
            y[x_curr, y_curr] = nodes
            z[x_curr, y_curr] = et
            y_curr += 1
            if y_curr == y_len:
                y_curr = 0
                x_curr += 1
        return x, y, z


def visualize(file_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x, y, z = read_data(file_name)

    ax.plot_surface(x, y, z, cmap='viridis', edgecolor='green')
    ax.set_xlabel('hosts')
    ax.set_ylabel('vertexes')
    ax.set_zlabel('time')
    ax.set_title('Simulation time (ESRN)')
    plt.savefig(f'fig/3d_plot_esrn.png', dpi=300)


if __name__ == '__main__':
    visualize('res/3d/data_esrn.csv')
