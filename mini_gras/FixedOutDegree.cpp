#include "Connect.cpp"

class FixedOutDegree : public Connect {
private:
    int outdegree;
    bool noDistr;

public:

    FixedOutDegree(int outdegree, bool noDistr) : outdegree(outdegree), noDistr(noDistr) {

    }

    void connect(Nucleus & pre_neurons, Nucleus & post_neurons,
                 float syn_delay, float syn_weight) {
        connect(pre_neurons, post_neurons, syn_delay, syn_weight, outdegree, noDistr);
    }

    void connect(Nucleus & pre_neurons, Nucleus & post_neurons,
                 float syn_delay, float syn_weight, int outdegree,
                 bool no_distr = false) {
        // seed with a real random value, if available
        random_device r;
        default_random_engine generator(r());
        uniform_int_distribution<int> id_distr(0, post_neurons.nucleus_size);
        normal_distribution<float> delay_distr(syn_delay, syn_delay / 5);
        normal_distribution<float> weight_distr(syn_weight, syn_weight / 20);

        for (unsigned int pre_id = 0; pre_id < pre_neurons.nucleus_size; pre_id++) {
            Neuron * pre_neuron = &nucleus[pre_neurons.id].neurons[pre_id];
            for (unsigned int post_id = 0; post_id < outdegree; post_id++) {
                int rand_post_id = id_distr(generator);
                Neuron * post_neuron = &nucleus[post_neurons.id].neurons[post_id];
                float delay = delay_distr(generator);
                float weight = weight_distr(generator);
                if (delay < SIM_STEP) {
                    delay = SIM_STEP;
                }
                Synapse synapse;
                if (no_distr) {
                    synapse = Synapse(post_neuron, syn_delay, syn_weight);
                }
                else {
                    synapse = Synapse(post_neuron, delay, weight);
                }
                pre_neuron->synapses->push_back(synapse);
            }
        }

        printf("Connect %s to %s [one_to_all] (1:%d). Total: %d W=%.2f, D=%.1f\n", pre_neurons.group_name.c_str(),
               post_neurons.group_name.c_str(), post_neurons.nucleus_size, pre_neurons.nucleus_size * post_neurons.nucleus_size,
               syn_weight, syn_delay);
    }
};

