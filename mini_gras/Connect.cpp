#pragma once

class Connect {
public:

    Connect() {

    }

    virtual void connect(Nucleus & pre_neurons, Nucleus & post_neurons,
                         float syn_delay, float syn_weight) = 0;
};
