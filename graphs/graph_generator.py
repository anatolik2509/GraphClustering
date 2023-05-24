import networkx as nx


def generate(nodes=20, edges=40) -> nx.Graph:
    g = nx.gnm_random_graph(nodes, edges)
    while not nx.is_connected(g):
        g = nx.gnm_random_graph(nodes, edges)
    return g


def generate_directed(nodes=20, edges=40) -> nx.Graph:
    g = nx.gnm_random_graph(nodes, edges, directed=True)
    if nx.is_connected(g):
        return g
    return generate(nodes, edges)
