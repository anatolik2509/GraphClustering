import networkx as nx


def generate() -> nx.Graph:
    g = nx.gnm_random_graph(20, 30)
    return g
