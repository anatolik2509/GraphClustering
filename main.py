import graph_generator
import graph_utils
import networkx as nx


if __name__ == '__main__':
    g = graph_generator.generate()
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    for _ in range(10):
        partitions = nx.community.asyn_fluidc(g, 3)
        graph_utils.draw_graph(g, partitions)
