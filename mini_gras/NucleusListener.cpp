#include "Nucleus.cpp"

class NucleusListener{
private:
    Nucleus *nucleus;
    vector<unsigned short> V_m;

public:
    explicit NucleusListener(Nucleus *nucleus): nucleus(nucleus), V_m(){

    }

    void listen(){
        vector<Neuron> neurons = nucleus->neurons;
        int sum = 0;
        for(auto & neuron : neurons){
            sum += neuron.V_m;
        }
        V_m.push_back(sum / neurons.size());
    }

    vector<unsigned short> *getV_m(){
        return &V_m;
    }
};

