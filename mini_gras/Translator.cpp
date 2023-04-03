#include "SOAContainer.cpp"
#include "StructsContainer.cpp"
#include <iterator>
#include <algorithm>
#include <mpi/mpi.h>

class Translator{
private:

    /*
     * +----------+
     * | NucleusV |
     * +----------+
     * | Nucleus  |
     * +----------+
     *
     * +---------------------------------+
     * |      Nucleus To Hosts Map       |
     * +-------------------+-------------+
     * | Order in NucleusV | Host Number |
     * +-------------------+-------------+
     *
     * +----------------------------------------------+
     * |            Neurons To Nucleus Map            |
     * +------------------+---------------------------+
     * | Order in Nucleus | Nucleus Order in NucleusV |
     * +------------------+---------------------------+
     *
     * Supposed, that Neuron/Nucleus id = order in arrays
     *
     */

    int hosts;
    int *nucleusToHostsMap;
    unsigned int nucleusNum;
    int *neuronsToNucleusMap;
    Neuron *neurons;
    unsigned int neuronsNum;
    SOAContainer* soaContainers;
    int *neuronsToContainerPosMap;
    int *nucleusToContainerPosMap;


    int* distributeToHosts(const vector<Nucleus>& nucleusV){
        nucleusToHostsMap = static_cast<int *>(malloc(sizeof(int) * nucleusV.size()));
        nucleusNum = nucleusV.size();
        for(int i = 0; i < nucleusV.size(); i++){
            nucleusToHostsMap[i] = i % hosts;
        }
        return nucleusToHostsMap;
    }

    Neuron* unpackNeurons(const vector<Nucleus>& nucleusV){
        int size = 0;
        for(const auto & i : nucleusV){
            size += i.nucleus_size;
        }
        cout << sizeof(Neuron) * size << endl;
        neuronsNum = size;
        neurons = (Neuron *)malloc(sizeof(Neuron) * (size + 1));
        neuronsToNucleusMap = static_cast<int *>(malloc(sizeof(int) * size));
        int index = 0;
        for(int i = 0; i < nucleusV.size(); i++){
            for(int j = 0; j < nucleusV[i].nucleus_size; j++){
                neuronsToNucleusMap[index] = i;
                neurons[index] = nucleusV[i].neurons[j];
                index++;
            }
        }
        return neurons;
    }

    static Neuron *addNeuronToContainer(SOAContainer *container, Neuron *neuron, int pos){
        container->V_m[pos] = neuron->V_m;
        container->L[pos] = neuron->L;
        container->V_th[pos] = neuron->V_th;
        container->has_spike[pos] = neuron->nrn_has_spike;
        container->nrnRefTime[pos] = neuron->nrn_ref_time;
        container->nrnRefTimeTimer[pos] = neuron->nrn_ref_time_timer;
        return neuron;
    }

    static Synapse *addSynapseToContainer(SOAContainer *container, Synapse *synapse, int pos){
        container->synDelay[pos] = synapse->syn_delay;
        container->synDelayTimer[pos] = synapse->syn_delay_timer;
        container->synWeight[pos] = synapse->syn_weight;
        return synapse;
    }

    static SOAContainer *initContainer(SOAContainer *container,
                                unsigned int nucleusInContainer,
                                unsigned int neuronsInContainer,
                                unsigned int synapsesInContainer){
        
        //neurons lists
        container -> id =
                static_cast<int *>(malloc(sizeof(int) * neuronsInContainer));
        container -> V_m =
                static_cast<unsigned short *>(malloc(sizeof(unsigned short) * neuronsInContainer));
        container -> L =
                static_cast<unsigned short *>(malloc(sizeof(unsigned short) * neuronsInContainer));
        container -> V_th =
                static_cast<unsigned short *>(malloc(sizeof(unsigned short) * neuronsInContainer));
        container -> has_spike =
                static_cast<bool *>(malloc(sizeof(bool) * neuronsInContainer));
        container -> nrnRefTime =
                static_cast<unsigned short *>(malloc(sizeof(unsigned short) * neuronsInContainer));
        container -> nrnRefTimeTimer =
                static_cast<unsigned short *>(malloc(sizeof(unsigned short) * neuronsInContainer));
        container -> synStartPos =
                static_cast<int *>(malloc(sizeof(int) * (neuronsInContainer + 1)));

        //synapses lists
        container -> preNrnPos =
                static_cast<int *>(malloc(sizeof(int) * synapsesInContainer));
        container -> postNrnPos =
                static_cast<int *>(malloc(sizeof(int) * synapsesInContainer));
        container -> synDelay =
                static_cast<int *>(malloc(sizeof(int) * synapsesInContainer));
        container -> synDelayTimer =
                static_cast<int *>(malloc(sizeof(int) * synapsesInContainer));
        container -> synWeight =
                static_cast<int *>(malloc(sizeof(int) * synapsesInContainer));

        //nucleus lists
        container -> nucleusId =
                static_cast<int *>(malloc(sizeof(int) * nucleusInContainer));
        container -> nrnStartPos =
                static_cast<int *>(malloc(sizeof(int) * (nucleusInContainer + 1)));

        container -> nucleusNum = nucleusInContainer;
        container -> neuronsNum = neuronsInContainer;
        container -> synapsesNum = synapsesInContainer;

        container->vPostNrnPos = static_cast<int *>(malloc(0));
        container->vSynDelayTimer = static_cast<int *>(malloc(0));
        container->vSynWeight = static_cast<int *>(malloc(0));

        container->virtualSynapseNum = 0;

        container->generatorPos = static_cast<int *>(malloc(0));
        container->generatorNum = 0;

        return container;
    }

    static unsigned int addVirtualSynapse(SOAContainer &container, int postNrnPos, int synWeight){
        container.virtualSynapseNum++;
        container.vPostNrnPos =
                static_cast<int *>(realloc(container.vPostNrnPos, sizeof(int) * container.virtualSynapseNum));
        container.vSynDelayTimer =
                static_cast<int *>(realloc(container.vSynDelayTimer, sizeof(int) * container.virtualSynapseNum));
        container.vSynWeight =
                static_cast<int *>(realloc(container.vSynWeight, sizeof(int) * container.virtualSynapseNum));
        container.vPostNrnPos[container.virtualSynapseNum - 1] = postNrnPos;
        container.vSynDelayTimer[container.virtualSynapseNum - 1] = -1;
        container.vSynWeight[container.virtualSynapseNum - 1] = synWeight;
        return container.virtualSynapseNum - 1;
    }

    static unsigned int addGenerator(SOAContainer &container, int generatorPos){
        container.generatorNum++;
        int rank{};
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        container.generatorPos =
                static_cast<int *>(realloc(container.generatorPos, sizeof(int) * container.generatorNum));
        container.generatorPos[container.generatorNum - 1] = generatorPos;
        return container.generatorNum - 1;
    }

    SOAContainer *parseNucleus(const vector<Nucleus>& nucleusV){
        printf("%lu\n", sizeof(vector<Nucleus>) * hosts);
        auto **nucleusListByContainer = static_cast<vector<struct Nucleus> **>(malloc(
                sizeof(vector<Nucleus>*) * hosts));
        for(int i = 0; i < hosts; i++){
            auto *vec = new vector<Nucleus>;
            nucleusListByContainer[i] = vec;
        }
        for(int i = 0; i < nucleusV.size(); i++){
            auto *vec = nucleusListByContainer[nucleusToHostsMap[i]];
            vec->push_back(nucleusV[i]);
        }
        neuronsToContainerPosMap = static_cast<int *>(malloc(sizeof(int) * neuronsNum));
        nucleusToContainerPosMap = static_cast<int *>(malloc(sizeof(int) * nucleusNum));
        int pushedNeurons;
        int pushedSynapses;
        unsigned int neuronsInContainer;
        unsigned int synapsesInContainer;
        for(int i = 0; i < hosts; i++){
            neuronsInContainer = 0;
            synapsesInContainer = 0;
            pushedNeurons = 0;
            SOAContainer *currentContainer = &soaContainers[i];

            countNeuronsAndSynapses(nucleusListByContainer[i], neuronsInContainer, synapsesInContainer);

            initContainer(&soaContainers[i],
                          nucleusListByContainer[i]->size(),
                          neuronsInContainer,
                          synapsesInContainer);

            parseNeurons(nucleusListByContainer[i], pushedNeurons, currentContainer);
        }
        for(int i = 0; i < hosts; i++){
            vector<int> proxyList = *(new vector<int>);
            vector<unsigned int> virtualSynapseList = *(new vector<unsigned int>);
            pushedSynapses = 0;
            int processedNeurons = 0;
            SOAContainer *currentContainer = &soaContainers[i];
            for(int j = 0; j < nucleusListByContainer[i]->size(); j++){
                Nucleus *currentNucleus = &(*nucleusListByContainer[i])[j];
                for(int n = 0; n < currentNucleus -> nucleus_size; n++) {
                    Neuron *currentNeuron = &currentNucleus->neurons[n];
                    currentContainer->synStartPos[processedNeurons++] = pushedSynapses;
                    if(currentNeuron->type == GENERATOR){
                        addGenerator(*currentContainer,
                                     neuronsToContainerPosMap[currentNeuron->id]);
                    }
                    for(int s = 0; s < currentNeuron->synapses->size(); s++){
                        Synapse *currentSynapse = &currentNeuron->synapses->at(s);
                        addSynapseToContainer(currentContainer, currentSynapse, pushedSynapses);
                        currentContainer->preNrnPos[pushedSynapses] =
                                neuronsToContainerPosMap[currentNeuron->id];

                        int preNrnHostId = nucleusToHostsMap[neuronsToNucleusMap[currentNeuron->id]];
                        int postNrnHostId = nucleusToHostsMap[neuronsToNucleusMap[currentSynapse->post_neuron->id]];
                        if(preNrnHostId == postNrnHostId){
                            currentContainer->postNrnPos[pushedSynapses] =
                                    neuronsToContainerPosMap[currentSynapse->post_neuron->id];
                        } else{
                            unsigned int virtualSynapsePos = addVirtualSynapse(soaContainers[postNrnHostId],
                                              neuronsToContainerPosMap[currentSynapse->post_neuron->id],
                                              currentSynapse->syn_weight);
                            currentContainer->postNrnPos[pushedSynapses] = -(int)proxyList.size() - 1;
                            proxyList.push_back(currentSynapse->post_neuron->id);
                            virtualSynapseList.push_back(virtualSynapsePos);
                        }
                        pushedSynapses++;
                    }
                }
            }
            currentContainer -> proxyId =
                    static_cast<int *>(malloc(proxyList.size() * sizeof(int)));
            currentContainer -> proxyHost =
                    static_cast<int *>(malloc(proxyList.size() * sizeof(int)));
            currentContainer -> proxyNum = proxyList.size();
            for(int j = 0; j < proxyList.size(); j++){
                currentContainer->proxyId[j] = (int) virtualSynapseList[j];
                currentContainer->proxyHost[j] = nucleusToHostsMap[neuronsToNucleusMap[proxyList[j]]];
            }
        }

        //free(nucleusListByContainer);
        //TODO free arrays
        return soaContainers;
    }

    void parseNeurons(vector<struct Nucleus> *nucleusList, int pushedNeurons, SOAContainer *currentContainer) {
        for(int j = 0; j < nucleusList->size(); j++){
            Nucleus *currentNucleus = &(*nucleusList)[j];
            currentContainer -> nucleusId[j] = currentNucleus->id;
            currentContainer -> nrnStartPos[j] = pushedNeurons;
            nucleusToContainerPosMap[currentNucleus->id] = j;
            for(int n = 0; n < currentNucleus -> nucleus_size; n++){
                Neuron *currentNeuron = &currentNucleus -> neurons[n];
                addNeuronToContainer(currentContainer, currentNeuron, pushedNeurons);
                neuronsToContainerPosMap[currentNeuron->id] = pushedNeurons;
                pushedNeurons++;
            }
        }
    }

    static void countNeuronsAndSynapses(vector<struct Nucleus> *nucleusList, unsigned int &neuronsInContainer,
                                 unsigned int &synapsesInContainer) {
        for(Nucleus & currentNucleus : *nucleusList){
            neuronsInContainer += currentNucleus.nucleus_size;
            for(int n = 0; n < currentNucleus.nucleus_size; n++){
                Neuron *currentNeuron = &currentNucleus.neurons[n];
                synapsesInContainer += currentNeuron->synapses->size();
            }
        }
    }

public:
    explicit Translator(int hosts){
        this->hosts = hosts;
    }

    SOAContainer* translate(const vector<Nucleus>& nucleusV){
        soaContainers = static_cast<SOAContainer *>(malloc(sizeof(SOAContainer) * hosts));
        distributeToHosts(nucleusV);
        unpackNeurons(nucleusV);
        parseNucleus(nucleusV);
        return soaContainers;
    }

    int getHosts() const{
        return hosts;
    }

    SOAContainer* getContainers(){
        return soaContainers;
    }
};

