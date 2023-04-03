#pragma once
#include <mpi/mpi.h> //WARNING: may not work on other systems
#define DEFAULT_TAG 0

MPI_Datatype spikeEventType {};

class NetworkAdapter {
public:
    NetworkAdapter(){
        MPI_Type_contiguous(2, MPI_INT, &spikeEventType);
        MPI_Type_commit(&spikeEventType);
    }

    void sendSoaContainer(SOAContainer *container, int host){
        int size{};//size in bytes
        short *flat = container->toFlat(size);
        MPI_Send(&size, 1, MPI_INT, host, DEFAULT_TAG, MPI_COMM_WORLD);
        MPI_Send(flat, size / 2, MPI_SHORT, host, DEFAULT_TAG, MPI_COMM_WORLD);
    }

    SOAContainer* receiveSoaContainer(int host){
        int size{};//size in bytes
        MPI_Recv(&size, 1, MPI_INT, host, DEFAULT_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        size /= 2;//now it is size in shorts
        auto *flat = static_cast<short *>(calloc(sizeof(short), size));
        MPI_Recv(flat, size, MPI_SHORT, host, DEFAULT_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        return SOAContainer::fromFlat(flat);
    }

    void sendSpikeEvents(MPISpikeEvent *events, int size, int host){
        int rank {};
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        printf("Sending %d to %d from %d\n", size, host, rank);
        if(size == 0){
            int buf = -1;
            MPI_Send(&buf, 1, MPI_INT, host,
                     DEFAULT_TAG, MPI_COMM_WORLD);
        }
        else {
            MPI_Send(events, size, spikeEventType, host,
                     DEFAULT_TAG, MPI_COMM_WORLD);
        }
    }

    MPISpikeEvent *receiveSpikeEvents(int *size, int host){
        int rank {};
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Status status;
        MPI_Probe(host, DEFAULT_TAG, MPI_COMM_WORLD, &status);
        MPI_Get_count(&status, spikeEventType, size);
        printf("%d messages from %d to %d\n", *size, host, rank);
        if(*size <= 0){
            int buf;
            MPI_Recv(&buf, 1, MPI_INT, host, DEFAULT_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            return nullptr;
        }
        auto *events = static_cast<MPISpikeEvent *>(calloc(*size, sizeof(MPISpikeEvent)));
        MPI_Recv(events, *size, spikeEventType, host, DEFAULT_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        return events;
    }
};


