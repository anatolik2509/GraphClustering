#pragma once

#include <random>
#include "Synapse.cpp"

using namespace std;

const int GENERATOR = 0;
const int NORMAL = 1;
const int PROXY = 2;

template<typename type>
type get_random_number(type mean, type stddev) {
    random_device r;
    default_random_engine generator(r());
    normal_distribution<float> distr(mean, stddev);
    return (type) distr(generator);
}

int global_id = 0;

class Neuron {
public:
    int id;
    int type;
    unsigned short V_m; //voltage
    unsigned short L; //idk
    unsigned short V_th; //threshold
    bool nrn_has_spike;
    int nrn_ref_time; //refractory period
    int nrn_ref_time_timer;
    int nrn_spike_waits;
    vector<Synapse> *synapses;

    Neuron(int type = NORMAL) {
        id = global_id++;
        nrn_spike_waits = 0;
        V_m = 28000;
        nrn_has_spike = false;
        nrn_ref_time_timer = 0;
        nrn_ref_time = get_random_number<int>((int) (3 / SIM_STEP), (int) (0.4 / SIM_STEP));
        L = get_random_number<unsigned short>(500, 500 / 20);
        V_th = get_random_number<unsigned short>(45000, 500);
        this->type = type;
        this->synapses = new vector<Synapse>();
    }

    Neuron(unsigned short V_m,
           unsigned short L,
           unsigned short V_th,
           bool nrn_has_spike,
           int nrn_ref_time,
           int nrn_ref_time_timer) {
        id = global_id++;
        this->V_m = V_m;
        this->L = L;
        this->V_th = V_th;
        this->nrn_has_spike = nrn_has_spike;
        this->nrn_ref_time = nrn_ref_time;
        this->nrn_ref_time_timer = nrn_ref_time_timer;
        this->nrn_spike_waits = 0;
        this->synapses = new vector<Synapse>();
    }
};

