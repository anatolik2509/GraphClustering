#pragma once
#include "Nucleus.cpp"



class SOAContainer{
public:
    //nucleus
    int *nucleusId;
    int *nrnStartPos;

    unsigned int nucleusNum = 0;

    //nrns
    int *id;
    unsigned short *V_m;
    unsigned short *L;
    unsigned short *V_th;
    bool *has_spike;
    unsigned short *nrnRefTime;
    unsigned short *nrnRefTimeTimer;
    int *synStartPos;

    unsigned int neuronsNum = 0;

    //synapses
    int *preNrnPos;
    int *postNrnPos;
    int *synDelay;
    int *synDelayTimer;
    int *synWeight;

    unsigned int synapsesNum = 0;

    //proxy_neurons
    int *proxyId;
    int *proxyHost;

    unsigned int proxyNum = 0;

    //virtual synapses
    int *vPostNrnPos;
    int *vSynDelayTimer;
    int *vSynWeight;

    unsigned int virtualSynapseNum = 0;

    //generators
    int *generatorPos;
    unsigned int generatorNum = 0;


    short *toFlat(int & size) const{
            //count nucleus information size
        unsigned int nucleusBytes = sizeof(int) * 2 * nucleusNum;
        nucleusBytes += 4; //for size information
            //count neurons information size
        unsigned int nrnBytes = (sizeof(int) * 2 + sizeof(unsigned short) * 5 + 2) * neuronsNum;
            //2 for boolean
        nrnBytes += 4; //for size information
            //count synapses information size
        unsigned int synapsesBytes = (sizeof(int) * 5) * synapsesNum;
        synapsesBytes += 4; //for size information
            //count proxy information size
        unsigned int proxyBytes = sizeof(int) * 2 * proxyNum;
        proxyBytes += 4;
            //count virtual synapse information size
        unsigned int virtualSynapseBytes = sizeof(int) * 3 * virtualSynapseNum;
        virtualSynapseBytes += 4;
            //count generator information size
        unsigned int generatorBytes = sizeof(int) * generatorNum;
        generatorBytes += 4;

        size = (int)(nucleusBytes + nrnBytes + synapsesBytes
               + proxyBytes + virtualSynapseBytes + generatorBytes);

        auto *flatArray = static_cast<short *>
                (malloc(size));
        short *pointer = flatArray;


        *((unsigned int *) pointer) = nucleusNum;
        pointer += 2;
        for(int i = 0; i < nucleusNum; i++){
            *((unsigned int *) pointer) = nucleusId[i];
            pointer += 2;
            *((unsigned int *) pointer) = nrnStartPos[i];
            pointer += 2;
        }


        *((unsigned int *) pointer) = neuronsNum;
        pointer += 2;
        for(int i = 0; i < neuronsNum; i++){
            *((int *) pointer) = id[i];
            pointer += 2;
            *((unsigned short *) pointer) = V_m[i];
            pointer += 1;
            *((unsigned short *) pointer) = L[i];
            pointer += 1;
            *((unsigned short *) pointer) = V_th[i];
            pointer += 1;
            *((unsigned short *) pointer) = has_spike[i] ? 1 : 0;
            pointer += 1;
            *((unsigned short *) pointer) = nrnRefTime[i];
            pointer += 1;
            *((unsigned short *) pointer) = nrnRefTimeTimer[i];
            pointer += 1;
            *((int *) pointer) = synStartPos[i];
            pointer += 2;
        }


        *((unsigned int *) pointer) = synapsesNum;
        pointer += 2;
        for(int i = 0; i < synapsesNum; i++){
            *((int *) pointer) = preNrnPos[i];
            pointer += 2;
            *((int *) pointer) = postNrnPos[i];
            pointer += 2;
            *((int *) pointer) = synDelay[i];
            pointer += 2;
            *((int *) pointer) = synDelayTimer[i];
            pointer += 2;
            *((int *) pointer) = synWeight[i];
            pointer += 2;
        }


        *((unsigned int *) pointer) = proxyNum;
        pointer += 2;
        for(int i = 0; i < proxyNum; i++){
            *((int *) pointer) = proxyId[i];
            pointer += 2;
            *((int *) pointer) = proxyHost[i];
            pointer += 2;
        }

        *((unsigned int *) pointer) = virtualSynapseNum;
        pointer += 2;
        for(int i = 0; i < virtualSynapseNum; i++){
            *((int *) pointer) = vPostNrnPos[i];
            pointer += 2;
            *((int *) pointer) = vSynDelayTimer[i];
            pointer += 2;
            *((int *) pointer) = vSynWeight[i];
            pointer += 2;
        }

        *((unsigned int *) pointer) = generatorNum;
        pointer += 2;
        for(int i = 0; i < generatorNum; i++){
            *((int *) pointer) = generatorPos[i];
            pointer += 2;
        }

        return flatArray;
    }


    static SOAContainer *fromFlat(short *flatArray){
        auto *container = new SOAContainer;
        short *pointer = flatArray;

        container->nucleusNum = *((unsigned int *)pointer);
        pointer += 2;
        container->nucleusId = static_cast<int *>(malloc(container->nucleusNum * sizeof(int)));
        container->nrnStartPos = static_cast<int *>(malloc(container->nucleusNum * sizeof(int)));
        for(int i = 0; i < container->nucleusNum; i++){
            container->nucleusId[i] = *((int *) pointer);
            pointer += 2;
            container->nrnStartPos[i] = *((int *) pointer);
            pointer += 2;
        }


        container->neuronsNum = *((unsigned int *) pointer);
        container->id = static_cast<int *>(malloc(container->neuronsNum * sizeof(int)));
        container->V_m = static_cast<unsigned short *>(malloc(container->neuronsNum * sizeof(short)));
        container->L = static_cast<unsigned short *>(malloc(container->neuronsNum * sizeof(short)));
        container->V_th = static_cast<unsigned short *>(malloc(container->neuronsNum * sizeof(short)));
        container->has_spike = static_cast<bool *>(malloc(container->neuronsNum * sizeof(bool)));
        container->nrnRefTime = static_cast<unsigned short *>(malloc(container->neuronsNum * sizeof(short)));
        container->nrnRefTimeTimer = static_cast<unsigned short *>(malloc(container->neuronsNum * sizeof(short)));
        container->synStartPos = static_cast<int *>(malloc(container->neuronsNum * sizeof(int)));
        pointer += 2;
        for(int i = 0; i < container->neuronsNum; i++){
            container->id[i] = *((int *) pointer);
            pointer += 2;
            container->V_m[i] = *((unsigned short *) pointer);
            pointer += 1;
            container->L[i] = *((unsigned short *) pointer);
            pointer += 1;
            container->V_th[i] = *((unsigned short *) pointer);
            pointer += 1;
            container->has_spike[i] = *((unsigned short *) pointer) == 1;
            pointer += 1;
            container->nrnRefTime[i] = *((unsigned short *) pointer);
            pointer += 1;
            container->nrnRefTimeTimer[i] = *((unsigned short *) pointer);
            pointer += 1;
            container->synStartPos[i] = *((unsigned short *) pointer);
            pointer += 2;
        }


        container->synapsesNum = *((unsigned int *) pointer);
        container->preNrnPos = static_cast<int *>(malloc(container->synapsesNum * sizeof(int)));
        container->postNrnPos = static_cast<int *>(malloc(container->synapsesNum * sizeof(int)));
        container->synDelay = static_cast<int *>(malloc(container->synapsesNum * sizeof(int)));
        container->synDelayTimer = static_cast<int *>(malloc(container->synapsesNum * sizeof(int)));
        container->synWeight = static_cast<int *>(malloc(container->synapsesNum * sizeof(int)));
        pointer += 2;
        for(int i = 0; i < container->synapsesNum; i++){
            container->preNrnPos[i] = *((int *) pointer);
            pointer += 2;
            container->postNrnPos[i] = *((int *) pointer);
            pointer += 2;
            container->synDelay[i] = *((int *) pointer);
            pointer += 2;
            container->synDelayTimer[i] = *((int *) pointer);
            pointer += 2;
            container->synWeight[i] = *((int *) pointer);
            pointer += 2;
        }


        container->proxyNum = *((unsigned int *) pointer);
        container->proxyId = static_cast<int *>(malloc(container->proxyNum * sizeof(int)));
        container->proxyHost = static_cast<int *>(malloc(container->proxyNum * sizeof(int)));
        pointer += 2;
        for(int i = 0; i < container->proxyNum; i++){
            container->proxyId[i] = *((int *) pointer);
            pointer += 2;
            container->proxyHost[i] = *((int *) pointer);
            pointer += 2;
        }

        container->virtualSynapseNum = *((unsigned int *) pointer);
        container->vPostNrnPos = static_cast<int *>(malloc(container->virtualSynapseNum * sizeof(int)));
        container->vSynDelayTimer = static_cast<int *>(malloc(container->virtualSynapseNum * sizeof(int)));
        container->vSynWeight = static_cast<int *>(malloc(container->virtualSynapseNum * sizeof(int)));
        pointer += 2;
        for(int i = 0; i < container->virtualSynapseNum; i++){
            container->vPostNrnPos[i] = *((int *) pointer);
            pointer += 2;
            container->vSynDelayTimer[i] = *((int *) pointer);
            pointer += 2;
            container->vSynWeight[i] = *((int *) pointer);
            pointer += 2;
        }

        container->generatorNum = *((unsigned int *) pointer);
        container->generatorPos = (int *)malloc(container->generatorNum * sizeof(int));
        pointer += 2;
        for(int i = 0; i < container->generatorNum; i++){
            container->generatorPos[i] = *((int *) pointer);
            pointer += 2;
        }

        return container;
    }


    void print() const{
        printf("Nucleus:\n");
        for(int i = 0; i < nucleusNum; i++){
            printf("[%d] nucleusId: %d, nrnStartPos: %d\n", i, nucleusId[i], nrnStartPos[i]);
        }

        printf("Neurons:\n");
        for(int i = 0; i < neuronsNum; i++){
            printf("[%d] V_m: %d, L: %d, V_th: %d, syn_start_pos: %d\n",
                   i, V_m[i], L[i], V_th[i], synStartPos[i]);
        }

        printf("Synapses:\n");
        for(int i = 0; i < synapsesNum; i++){
            printf("[%d] pre_nrn: %d, post_nrn: %d, syn_delay: %d, syn_weight: %d\n",
                   i, preNrnPos[i], postNrnPos[i], synDelay[i], synWeight[i]);
        }

        printf("Proxy:\n");
        printf("ProxyNum: %d\n", proxyNum);
        for(int i = 0; i < proxyNum; i++){
            printf("[%d] proxy_id: %d, proxyHost: %d\n",
                   i, proxyId[i], proxyHost[i]);
        }

        printf("Virtual synapses:\n");
        for(int i = 0; i < virtualSynapseNum; i++){
            printf("[%d] post_nrn: %d, synDelayTimer: %d, synWeight: %d\n",
                   i, vPostNrnPos[i], vSynDelayTimer[i], vSynWeight[i]);
        }

        printf("Generator:\n");
        for(int i = 0; i < generatorNum; i++){
            printf("[%d] generator pos: %d\n",
                   i, generatorPos[i]);
        }
    }


};
