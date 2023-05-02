import time

import networkx as nx

import graphs.graph_utils
from core.core import Core
from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshConfig
from esrn_simulating import esrn_topology_constructor
from esrn_simulating.esrn_code_generator import EsrnCodeGenerator
from esrn_simulating.utils import to_data_set, draw_nuclei
from graphs.fluid_clustering_algorithm import FluidClusteringAlgorithm
from graphs.spin_glass_clustering_algorithm import SpinGlassClusteringAlgorithm
from graphs.walktrap_clustering_algorithm import WalktrapClusteringAlgorithm
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


def create_motif(gr1, gr2, gr3, gr4):
    esrn_topology_constructor.add_synapse(gr1, gr2, 60, 50, 5000)
    esrn_topology_constructor.add_synapse(gr2, gr3, 60, 50, 5000)
    esrn_topology_constructor.add_synapse(gr3, gr2, 60, 50, 5000)
    esrn_topology_constructor.add_synapse(gr2, gr4, 60, 50, 0.315)
    esrn_topology_constructor.add_synapse(gr3, gr4, 60, 50, 0.515)
    esrn_topology_constructor.add_synapse(gr4, gr3, 60, 50, -3080)
    esrn_topology_constructor.add_synapse(gr4, gr2, 60, 50, -3080)


def create_reflect_arc():
    layers = 6
    CV_number = 6
    step_number = 11
    neurons_number = 50
    neurons_in_ip = 196

    esrn_topology_constructor.add_nucleus('EES', 1, 0)
    esrn_topology_constructor.add_nucleus('MOTO_NOISE', 1, 0)

    for i in range(CV_number):
        esrn_topology_constructor.add_nucleus(f'C{i + 1}', 1, 0)

    for i in range(step_number):
        esrn_topology_constructor.add_nucleus(f'C_0_step_{i}', 1, 0)
        esrn_topology_constructor.add_nucleus(f'V0v_step_{i}', 1, 0)

    esrn_topology_constructor.add_nucleus('OM1_0E', neurons_number)
    esrn_topology_constructor.add_nucleus('OM1_0F', 50)

    for i in range(layers):
        esrn_topology_constructor.add_nucleus(f'OM{i + 1}_0', neurons_number)
        esrn_topology_constructor.add_nucleus(f'OM{i + 1}_1', neurons_number)
        esrn_topology_constructor.add_nucleus(f'OM{i + 1}_2E', neurons_number)
        esrn_topology_constructor.add_nucleus(f'OM{i + 1}_2F', neurons_number)
        esrn_topology_constructor.add_nucleus(f'OM{i + 1}_3', neurons_number)

    for i in range(CV_number):
        esrn_topology_constructor.add_nucleus(f'E{i + 1}', 50)
        esrn_topology_constructor.add_nucleus(f'CV_{i + 1}', 50)

    for layer in range(layers):
        esrn_topology_constructor.add_nucleus(f'IP_E_{layer + 1}', 50)
        esrn_topology_constructor.add_nucleus(f'IP_F_{layer + 1}', 50)

    esrn_topology_constructor.add_nucleus('Ia_aff_E', 120)
    esrn_topology_constructor.add_nucleus('Ia_aff_F', 120)

    esrn_topology_constructor.add_nucleus('mns_E', 210)
    esrn_topology_constructor.add_nucleus('mns_F', 180)

    esrn_topology_constructor.add_nucleus('muscle_E', 210 * 50)
    esrn_topology_constructor.add_nucleus('muscle_F', 180 * 50)

    esrn_topology_constructor.add_nucleus('Ia_E', neurons_in_ip)
    esrn_topology_constructor.add_nucleus('iIP_E', neurons_in_ip)
    esrn_topology_constructor.add_nucleus('R_E', neurons_number)

    esrn_topology_constructor.add_nucleus('Ia_F', neurons_in_ip)
    esrn_topology_constructor.add_nucleus('iIP_F', neurons_in_ip)
    esrn_topology_constructor.add_nucleus('R_F', neurons_number)

    create_motif('OM1_0E', 'OM1_1', 'OM1_2E', 'OM1_3')
    for layer in range(layers - 1):
        create_motif(f'OM{layer + 2}_0', f'OM{layer + 2}_1', f'OM{layer + 2}_2E', f'OM{layer + 2}_3')

    create_motif('OM1_0F', 'OM1_1', 'OM1_2F', 'OM1_3')
    for layer in range(layers - 1):
        create_motif(f'OM{layer + 2}_0', f'OM{layer + 2}_1', f'OM{layer + 2}_2F', f'OM{layer + 2}_3')

    for i in range(layers - 1):
        esrn_topology_constructor.add_synapse(f'OM{i + 1}_2F', f'OM{i + 2}_2F', 60, 50, 200)

    esrn_topology_constructor.add_synapse('E1', 'OM1_0F', 50, 50, 0.25)

    for i in range(step_number):
        esrn_topology_constructor.add_synapse(f'V0v_step_{i}', 'OM1_0F', 60, 50, 750)

    for i in range(layers - 1):
        esrn_topology_constructor.add_synapse(f'E{i + 1}', f'E{i + 2}', 50, 50, 750)

    esrn_topology_constructor.add_synapse('E1', 'OM1_0E', 50, 50, 4)

    for i in range(layers - 1):
        esrn_topology_constructor.add_synapse(f'E{i + 1}', f'OM{i + 1}_0', 50, 50, 4)

    for layer in range(2, layers):
        for i in range(layer - 1):
            esrn_topology_constructor.add_synapse(f'C{layer + 1}', f'OM{i + 1}_3', 50, 50, 1950)

    esrn_topology_constructor.add_synapse('EES', 'Ia_aff_E', 20, 50, 2500)
    esrn_topology_constructor.add_synapse('EES', 'Ia_aff_F', 20, 50, 2500)
    esrn_topology_constructor.add_synapse('EES', 'E1', 50, 50, 1000)
    esrn_topology_constructor.add_synapse('Ia_aff_E', 'mns_E', 20, 50, 45)
    esrn_topology_constructor.add_synapse('Ia_aff_F', 'mns_F', 40, 50, 6)

    esrn_topology_constructor.add_synapse('mns_E', 'muscle_E', 25, 45, 110)
    esrn_topology_constructor.add_synapse('mns_F', 'muscle_F', 25, 45, 380)

    esrn_topology_constructor.add_synapse('MOTO_NOISE', 'mns_E', 100, 50, 50)
    esrn_topology_constructor.add_synapse('MOTO_NOISE', 'mns_F', 100, 50, 500)

    esrn_topology_constructor.add_synapse('C1', 'Ia_aff_E', 40, 50, -400)
    esrn_topology_constructor.add_synapse('C2', 'Ia_aff_E', 40, 50, -200)
    esrn_topology_constructor.add_synapse('C5', 'Ia_aff_E', 40, 50, -200)
    esrn_topology_constructor.add_synapse('C6', 'Ia_aff_E', 40, 50, -400)

    for layer in range(layers):
        esrn_topology_constructor.add_synapse(f'OM{layer + 1}_2E', f'IP_E_{layer + 1}', 40, 50, 5)
        esrn_topology_constructor.add_synapse(f'IP_E_{layer + 1}', 'mns_E', 40, 50, 4.5)
        if layer > 3:
            esrn_topology_constructor.add_synapse(f'IP_E_{layer + 1}', 'Ia_aff_E', 20, 50, -0.2 * layer)
        else:
            esrn_topology_constructor.add_synapse(f'IP_E_{layer + 1}', 'Ia_aff_E', 20, 50, -0.1)
        esrn_topology_constructor.add_synapse(f'OM{layer + 1}_2F', f'IP_F_{layer + 1}', 40, 50, 5)
        esrn_topology_constructor.add_synapse(f'IP_F_{layer + 1}', 'mns_F', 40, 50, 4.5)

    for layer in range(CV_number):
        esrn_topology_constructor.add_synapse(f'C{layer + 1}', f'CV_{layer + 1}', 40, 50, 150)

    esrn_topology_constructor.add_synapse('CV_1', 'OM1_0E', 60, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_2', 'OM1_0E', 60, 50, 4.5)

    esrn_topology_constructor.add_synapse('CV_1', 'OM2_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_2', 'OM2_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_3', 'OM2_0', 80, 50, 4.5)

    esrn_topology_constructor.add_synapse('CV_1', 'OM3_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_2', 'OM3_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_3', 'OM3_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_4', 'OM3_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_5', 'OM3_0', 80, 50, 4.5)

    esrn_topology_constructor.add_synapse('CV_2', 'OM4_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_3', 'OM4_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_4', 'OM4_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_5', 'OM4_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_6', 'OM4_0', 80, 50, 4.5)

    esrn_topology_constructor.add_synapse('CV_2', 'OM5_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_3', 'OM5_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_4', 'OM5_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_5', 'OM5_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_6', 'OM5_0', 80, 50, 4.5)

    esrn_topology_constructor.add_synapse('CV_2', 'OM6_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_3', 'OM6_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_4', 'OM6_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_5', 'OM6_0', 80, 50, 4.5)
    esrn_topology_constructor.add_synapse('CV_6', 'OM6_0', 80, 50, 4.5)

    for layer in range(layers):
        esrn_topology_constructor.add_synapse(f'IP_E_{layer + 1}', 'iIP_E', 20, 50, 1)

    for layer in range(layers):
        esrn_topology_constructor.add_synapse(f'CV_{layer + 1}', 'iIP_E', 28, 50, 1000)
        esrn_topology_constructor.add_synapse(f'C{layer + 1}', 'iIP_E', 20, 50, 1000)

    esrn_topology_constructor.add_synapse('iIP_E', 'OM1_0F', 5, 50, -1)

    for layer in range(layers):
        esrn_topology_constructor.add_synapse('iIP_E', f'OM{layer + 1}_2F', 40, 50, -400)
        esrn_topology_constructor.add_synapse('iIP_F', f'OM{layer + 1}_2E', 40, 50, -500)

    esrn_topology_constructor.add_synapse('iIP_E', 'Ia_aff_F', 20, 50, -1200)
    esrn_topology_constructor.add_synapse('iIP_E', 'mns_F', 80, 50, -31.5)

    for layer in range(layers):
        esrn_topology_constructor.add_synapse('iIP_E', f'IP_F_{layer + 1}', 100, 50, -5)
        esrn_topology_constructor.add_synapse(f'IP_F_{layer + 1}', 'iIP_F', 20, 50, 0.1)
        esrn_topology_constructor.add_synapse('iIP_F', f'IP_E_{layer + 1}', 20, 50, -80)

    esrn_topology_constructor.add_synapse('iIP_F', 'iIP_E', 20, 50, -500)
    esrn_topology_constructor.add_synapse('iIP_F', 'Ia_aff_E', 20, 50, -3500)
    esrn_topology_constructor.add_synapse('iIP_F', 'mns_E', 20, 50, -350)

    for layer in range(step_number):
        esrn_topology_constructor.add_synapse(f'C_0_step_{layer}', 'iIP_F', 20, 50, 800)

    esrn_topology_constructor.add_synapse('iIP_E', 'Ia_E', 20, 50, 1)
    esrn_topology_constructor.add_synapse('Ia_aff_E', 'Ia_E', 20, 50, 8)
    esrn_topology_constructor.add_synapse('mns_E', 'R_E', 20, 50, 8)
    esrn_topology_constructor.add_synapse('Ia_E', 'mns_F', 20, 50, -2)
    esrn_topology_constructor.add_synapse('R_E', 'Ia_E', 20, 50, -1)

    esrn_topology_constructor.add_synapse('iIP_F', 'Ia_F', 20, 50, 1)
    esrn_topology_constructor.add_synapse('Ia_aff_F', 'Ia_F', 20, 50, 8)
    esrn_topology_constructor.add_synapse('mns_F', 'R_F', 20, 50, 0.15)

    esrn_topology_constructor.add_synapse('R_F', 'mns_F', 20, 50, -0.15)
    esrn_topology_constructor.add_synapse('R_F', 'Ia_F', 20, 50, -1)

    esrn_topology_constructor.add_synapse('R_E', 'R_F', 20, 50, -40)
    esrn_topology_constructor.add_synapse('R_F', 'R_E', 20, 50, -40)
    esrn_topology_constructor.add_synapse('Ia_E', 'Ia_F', 20, 50, -80)
    esrn_topology_constructor.add_synapse('Ia_F', 'Ia_E', 20, 50, -80)
    esrn_topology_constructor.add_synapse('iIP_E', 'iIP_F', 60, 50, -40)
    esrn_topology_constructor.add_synapse('iIP_F', 'iIP_E', 20, 50, -40)

    return esrn_topology_constructor.build()


if __name__ == '__main__':
    topology = create_reflect_arc()
    configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
               SshConfig('172.17.0.3', user='anatoly', password='')]

    clustering_algorithm = WeightedFluidClusteringAlgorithm()
    computing_power_calculator = DockerPowerCalculator()
    code_generator = EsrnCodeGenerator()
    core = Core(configs, clustering_algorithm, code_generator, computing_power_calculator)
    process = core.execute(topology)
    print('starting')
    start = time.time()
    stdout = process.stdout
    lines = []
    while True:
        line = stdout.readline()
        if not line:
            break
        lines.append(line.decode('utf-8').rstrip('\n'))
    finish = time.time()
    print(finish - start, ' sec.')
    data = to_data_set(lines, topology, core.cluster_info)
    name = 'iIP_E'
    draw_nuclei(data[name], name)
