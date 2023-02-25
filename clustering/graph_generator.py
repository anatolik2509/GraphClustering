import networkx as nx


def generate() -> nx.Graph:
    g = nx.gnm_random_graph(20, 30)
    if g.is_connected():
        return g
    return generate()


def generate(nodes, edges) -> nx.Graph:
    g = nx.gnm_random_graph(nodes, edges)
    i = 0
    while not g.is_connected() and i < 100:
        g = nx.gnm_random_graph(nodes, edges)
        i += 1
    if i == 100:
        raise Exception('Max retries to generate graph')
    return g
