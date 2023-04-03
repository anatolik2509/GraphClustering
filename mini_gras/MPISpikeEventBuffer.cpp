#pragma once
#include "MPISpikeEvent.cpp"
#include "NetworkAdapter.cpp"

class MPISpikeEventBuffer{
private:
    vector<MPISpikeEvent> events;
    int destinationHost{};
    NetworkAdapter adapter;
public:
    explicit MPISpikeEventBuffer(int destinationHost){
        events = *(new vector<MPISpikeEvent>);
        this->destinationHost = destinationHost;
        adapter = *(new NetworkAdapter());
    }

    MPISpikeEventBuffer() = default;

    void addSpikeEvent(int virtualSynapsePos, int currentDelayTimer, int timeBeforeNextSync){
        events.push_back(MPISpikeEvent{virtualSynapsePos, currentDelayTimer - timeBeforeNextSync});
    }

    void flush(){
        adapter.sendSpikeEvents(events.data(), (int)events.size(), destinationHost);
        events.clear();
    }

};
