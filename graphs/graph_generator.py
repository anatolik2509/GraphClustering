import networkx as nx


def generate(nodes=20, edges=40) -> nx.Graph:
    g = nx.gnm_random_graph(nodes, edges)
    if nx.is_connected(g):
        return g
    return generate()
