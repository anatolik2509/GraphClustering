import networkx as nx

nucleus = {}
synapses = []

NUCLEUS_NAME_LABEL = 'nucleus_name'
NEURONS_COUNT_LABEL = 'nucleus_count'
NUCLEUS_TYPE_LABEL = 'nucleus_type'

SYNAPSE_DELAY_LABEL = 'delay'
SYNAPSE_OUTDEGREE_LABEL = 'outdegree'
SYNAPSE_WEIGHT_LABEL = 'syn_weight'


def add_nucleus(nucleus_name, neurons_count, nucleus_type=1):
    nucleus[nucleus_name] = {NEURONS_COUNT_LABEL: neurons_count, NUCLEUS_TYPE_LABEL: nucleus_type}


def add_synapse(out_nucleus, in_nucleus, delay, outdegree, syn_weight):
    synapses.append({'out': out_nucleus, 'in': in_nucleus, SYNAPSE_DELAY_LABEL: delay, SYNAPSE_WEIGHT_LABEL: syn_weight
                    , SYNAPSE_OUTDEGREE_LABEL: outdegree})


def build():
    nucleus_to_num = {}
    topology = nx.DiGraph()
    for i, (key, value) in enumerate(nucleus.items()):
        topology.add_node(i, nucleus_name=key, nucleus_count=value[NEURONS_COUNT_LABEL],
                          nucleus_type=value[NUCLEUS_TYPE_LABEL], weight=value[NEURONS_COUNT_LABEL])
        nucleus_to_num[key] = i

    for synapse in synapses:
        weight = synapse[SYNAPSE_OUTDEGREE_LABEL] * nucleus[synapse['out']][NEURONS_COUNT_LABEL]
        if nucleus[synapse['out']][NUCLEUS_TYPE_LABEL] == 0:
            weight = weight * 100
        topology.add_edge(nucleus_to_num[synapse['out']], nucleus_to_num[synapse['in']],
                          delay=synapse[SYNAPSE_DELAY_LABEL], outdegree=synapse[SYNAPSE_OUTDEGREE_LABEL],
                          syn_weight=synapse[SYNAPSE_WEIGHT_LABEL],
                          weight=weight)
    return topology


def clean():
    nucleus.clear()
    synapses.clear()
