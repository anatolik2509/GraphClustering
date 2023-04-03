#include "SOAContainer.cpp"
#include "MPISpikeEventBuffer.cpp"
#include "MPISpikeEventReceiver.cpp"
#include "NeuronUpdater.cpp"
#include <mpi/mpi.h>

class SOASimulator{
private:
    SOAContainer container;
    vector<MPISpikeEventBuffer> *buffers;
    vector<MPISpikeEventReceiver> *receivers;

    NeuronUpdater updater;

    int host;
    int hostCount;

    int step = 0;
    int msInStep = 25;
    int synchronizeIterations = 5;

public:
    SOASimulator(SOAContainer & soaContainer, int host, int hostCount){
        container = soaContainer;
        this->host = host;
        this->hostCount = hostCount;
        buffers = new vector<MPISpikeEventBuffer>();
        receivers = new vector<MPISpikeEventReceiver>();
        for(int i = 0; i < hostCount; i++){
            buffers->push_back(*(new MPISpikeEventBuffer(i)));
            receivers->push_back(*(new MPISpikeEventReceiver(i)));
        }
        updater = *(new NeuronUpdater(&container));
    }

    SOASimulator(SOAContainer soaContainer, int host, int hostCount, int msInSteps, int synchronizeIterations){
        container = soaContainer;
        this->msInStep = msInSteps;
        this->synchronizeIterations = synchronizeIterations;
        this->host = host;
        this->hostCount = hostCount;
        buffers = new vector<MPISpikeEventBuffer>();
        receivers = new vector<MPISpikeEventReceiver>();
        for(int i = 0; i < hostCount; i++){
            buffers->push_back(*(new MPISpikeEventBuffer(i)));
            receivers->push_back(*(new MPISpikeEventReceiver(i)));
        }
        updater = *(new NeuronUpdater(&container));
    }

    void simulateStep(){
        updater.updateNeurons();
        updater.updateGenerators();
        updater.updateSynapses(buffers, step % synchronizeIterations);
    }

    void synchronize(){
        for(int i = 0; i < buffers->size(); i++){
            if(i == host) continue;
            (*buffers)[i].flush();
        }
        MPI_Barrier(MPI_COMM_WORLD);
        printf("{%d} Barrier overcomed\n", host);
        for(int i = 0; i < receivers->size(); i++){
            if((*receivers)[i].getHost() == host) continue;
            (*receivers)[i].loadSpikeEvents();
            updater.activateVirtualSynapses(*(*receivers)[i].getEvents());
        }
    }

    void run(int steps){
        for(int i = 1; i <= steps; i++){
            step++;
            simulateStep();
            if(step % synchronizeIterations == 0){
                synchronize();
            }
        }
    }

    int getStep() const{
        return step;
    }

    int getMsInStep() const{
        return msInStep;
    }

    int getSynchronizeIteration() const{
        return synchronizeIterations;
    }

    int getHost() const{
        return host;
    }

    vector<MPISpikeEventBuffer> *getBuffer(){
        return buffers;
    }

    vector<MPISpikeEventReceiver> *getReceiver(){
        return receivers;
    }

    SOAContainer *getContainer(){
        return &container;
    }
};
