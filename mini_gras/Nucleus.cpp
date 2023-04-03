#pragma once


#include "Neuron.cpp"


class Nucleus {
public:
    int type;
    string group_name;
    int nucleus_size;
    int id;
    vector<Neuron> neurons;

    Nucleus() {

    }

    Nucleus(string group_name, int nucleus_size, int type = NORMAL) {
        this->group_name = std::move(group_name);
        this->nucleus_size = nucleus_size;
        this->type = type;
        for (int i = 0; i < nucleus_size; i++) {
            neurons.emplace_back(type);
        }
    }
};

int globalNucleiId = 0;
vector<Nucleus> nucleus {};

Nucleus form_nuclei(string group_name, int neurons_number, int type = NORMAL) {
    Nucleus nuclei = Nucleus(std::move(group_name), neurons_number, type);
    nuclei.id = globalNucleiId;
    nucleus.push_back(nuclei);
    return nucleus[globalNucleiId++];
}

