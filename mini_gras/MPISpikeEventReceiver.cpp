#pragma once

class MPISpikeEventReceiver{
private:
    int host;
    vector<MPISpikeEvent> *receivedEvents;
    NetworkAdapter adapter;
public:

    explicit MPISpikeEventReceiver(int host){
        this->host = host;
        receivedEvents = new vector<MPISpikeEvent>();
        adapter = *(new NetworkAdapter);
    }

    MPISpikeEventReceiver() = default;

    void loadSpikeEvents(){
        receivedEvents->clear();
        int size = 0;
        MPISpikeEvent *events = adapter.receiveSpikeEvents(&size, host);
        if (size < 0) {
            return;
        }
        printf("Loaded %d events from %d\n", size, host);
        receivedEvents->insert(receivedEvents->end(), events, events + size);
        free(events);
    }

    vector<MPISpikeEvent> *getEvents(){
        return receivedEvents;
    }

    int getHost(){
        return host;
    }
};
