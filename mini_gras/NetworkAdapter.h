
#ifndef TEST_NETWORKADAPTER_H
#define TEST_NETWORKADAPTER_H
#include "MPISpikeEvent.cpp"
#include "SOAContainer.cpp"
#include <mpi/mpi.h>

class NetworkAdapter {
public:
    NetworkAdapter();

    void sendSoaContainer(SOAContainer *container, int host);

    SOAContainer* receiveSoaContainer(int host);

    void sendSpikeEvents(MPISpikeEvent *events, int size, int host);

    int receiveSpikeEvents(MPISpikeEvent *events, int host);
};


#endif //TEST_NETWORKADAPTER_H
