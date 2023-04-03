#pragma once

#include "SOAContainer.cpp"

class NeuronUpdater {
private:
    SOAContainer *container;
public:
    explicit NeuronUpdater(SOAContainer *soaContainer) {
        container = soaContainer;
    }

    NeuronUpdater() = default;

    void updateNeurons() {
        for (int i = 0; i < container->neuronsNum; i++) {
            container->has_spike[i] = false;
            // (threshold && not in refractory period) >= -55mV
            if ((container->V_m[i] >= container->V_th[i]) && (container->nrnRefTimeTimer[i] == 0)) {
                container->V_m[i] = 20000;
                container->has_spike[i] = true;
                container->nrnRefTimeTimer[i] = container->nrnRefTime[i];
            }
            if (container->V_m[i] < 27500)
                container->V_m[i] += container->L[i];
            if (container->V_m[i] > 28500)
                container->V_m[i] -= container->L[i];
            if (container->nrnRefTimeTimer[i] > 0)
                container->nrnRefTimeTimer[i]--;
        }
    }

    void updateGenerators() {
        for (int i = 0; i < container->generatorNum; i++) {
            container->has_spike[container->generatorPos[i]] = true;
        }
    }

    void updateSynapses(vector<MPISpikeEventBuffer> *buffers, int timeBeforeSync) {
        for (int n = 0; n < container->neuronsNum; n++) {
            int startSyn = container->synStartPos[n];
            int endSyn = n >= container->neuronsNum - 1 ?
                         (int) container->synapsesNum : (int) container->synStartPos[n + 1];
            // add synaptic delay if neuron has spike
            if (container->has_spike[n]) {
                // for by post neurons by neuron
                for (int post_id = startSyn; post_id < endSyn; post_id++) {
                    if (container->synDelayTimer[post_id] == -1) {
                        if(container->postNrnPos[post_id] >= 0){
                            container->synDelayTimer[post_id] = container->synDelay[post_id];
                        } else{
                            int proxyPos = -(container->postNrnPos[post_id]) - 1;
                            (*buffers)[container->proxyHost[proxyPos]]
                                .addSpikeEvent(proxyPos,
                                               container->synDelay[post_id],
                                               timeBeforeSync);
                        }
                    }
                }
            }

            // only for neurons which have post neurons that "waits" signal from them

            // stride by post neurons by neuron
            for (int post_id = startSyn; post_id < endSyn; post_id++) {
                // if synaptic delay is zero it means the time when synapse increase I by synaptic weight
                if (container->synDelayTimer[post_id] == 0) {
                    container->V_m[container->postNrnPos[post_id]]
                        += container->synWeight[container->postNrnPos[post_id]];
                    if (container->V_m[container->postNrnPos[post_id]] < 20000) {
                        container->V_m[container->postNrnPos[post_id]] = 20000;
                    }
                    if (container->V_m[container->postNrnPos[post_id]] > 50000) {
                        container->V_m[container->postNrnPos[post_id]] = 50000;
                    }
                    // make synapse timer a "free" for next spikes
                    container->synDelayTimer[post_id] = -1;
                }
                    // update synapse delay timer
                else if (container->synDelayTimer[post_id] > 0) {
                    container->synDelayTimer[post_id]--;
                }
            }

        }
        for(int syn = 0; syn < container->virtualSynapseNum; syn++){
            if (container->vSynDelayTimer[syn] == 0) {
                container->V_m[container->vPostNrnPos[syn]]
                        += container->synWeight[container->vPostNrnPos[syn]];
                if (container->V_m[container->vPostNrnPos[syn]] < 20000) {
                    container->V_m[container->vPostNrnPos[syn]] = 20000;
                }
                if (container->V_m[container->vPostNrnPos[syn]] > 50000) {
                    container->V_m[container->vPostNrnPos[syn]] = 50000;
                }
                // make synapse timer a "free" for next spikes
                container->vSynDelayTimer[syn] = -1;
            }
                // update synapse delay timer
            else if (container->vSynDelayTimer[syn] > 0) {
                container->vSynDelayTimer[syn]--;
            }
        }

    }

    void activateVirtualSynapses(const vector<MPISpikeEvent> &events){
        for(MPISpikeEvent e : events){
            //printf("Received event pos=%d, delay=%d\n", e.virtualSynapsePos, e.delayTimer);
            if (container->vSynDelayTimer[e.virtualSynapsePos] == -1) {
                container->vSynDelayTimer[e.virtualSynapsePos] = e.delayTimer;
            }
        }
    }
};



