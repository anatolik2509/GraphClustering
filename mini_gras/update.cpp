#pragma once

#include "Neuron.cpp"

void update_neuron(Neuron * neuron, int id, bool flag) {
    // reset spike flag of the current neuron before calculations
    neuron->nrn_has_spike = false;

    if(neuron->type == GENERATOR){
        neuron->nrn_has_spike = true;
    }

    // (threshold && not in refractory period) >= -55mV
    if ((neuron->V_m >= neuron->V_th) && (neuron->nrn_ref_time_timer == 0)) {
        neuron->V_m = 20000;
        neuron->nrn_has_spike = true;
        neuron->nrn_ref_time_timer = neuron->nrn_ref_time;
    }
    if (neuron->V_m < 27500)
        neuron->V_m += neuron->L;
    if (neuron->V_m > 28500)
        neuron->V_m -= neuron->L;
    if (neuron->nrn_ref_time_timer > 0)
        neuron->nrn_ref_time_timer--;

}

void update_synapse(Neuron * neuron) {
    // add synaptic delay if neuron has spike
    if (neuron->nrn_has_spike) {
        // for by post neurons by neuron
        for (int post_id = 0; post_id < neuron->synapses->size(); post_id++) {
            if (neuron->synapses->at(post_id).syn_delay_timer == -1) {
                neuron->synapses->at(post_id).syn_delay_timer = neuron->synapses->at(post_id).syn_delay;
                // increase count of post neurons which waits signal from pre neuron
                neuron->nrn_spike_waits++;
            }
        }
    }

    // only for neurons which have post neurons that "waits" signal from them
    if (neuron->nrn_spike_waits > 0) {
        // stride by post neurons by neuron
        for (int post_id = 0; post_id < neuron->synapses->size(); post_id++) {
            // if synaptic delay is zero it means the time when synapse increase I by synaptic weight
            if (neuron->synapses->at(post_id).syn_delay_timer == 0) {
                neuron->synapses->at(post_id).post_neuron->V_m += neuron->synapses->at(post_id).syn_weight;
                if (neuron->synapses->at(post_id).post_neuron->V_m < 20000) {
                    neuron->synapses->at(post_id).post_neuron->V_m = 20000;
                }
                if (neuron->synapses->at(post_id).post_neuron->V_m > 50000) {
                    neuron->synapses->at(post_id).post_neuron->V_m = 50000;
                }
                // decrease count of post neurons which waits signal from pre neuron
                neuron->nrn_spike_waits--;
                // make synapse timer a "free" for next spikes
                neuron->synapses->at(post_id).syn_delay_timer = -1;
            }
                // update synapse delay timer
            else if (neuron->synapses->at(post_id).syn_delay_timer > 0) {
                neuron->synapses->at(post_id).syn_delay_timer--;
            }
        }
    }
}

