#pragma once

const float SIM_STEP = 1.0;

class Neuron;

class Synapse {
public:
    int syn_delay{};
    int syn_delay_timer;
    short syn_weight{};
    Neuron * post_neuron{};

    Synapse() {
        syn_delay_timer = -1;
    }

    Synapse(Neuron * post_neuron, float syn_delay, short syn_weight) {
        syn_delay_timer = -1;
        this->post_neuron = post_neuron;
        this->syn_delay = lround(syn_delay * (1 / SIM_STEP) + 0.5);
        this->syn_weight = syn_weight;
    }

};

