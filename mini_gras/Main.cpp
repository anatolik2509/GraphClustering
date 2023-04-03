
#include <iostream>
#include "update.cpp"
#include "Nucleus.cpp"
#include "SOAContainer.cpp"
#include "Translator.cpp"
#include "FixedOutDegree.cpp"
#include "NucleusListener.cpp"
#include "SOASimulator.cpp"
#include <mpi/mpi.h>
#include "NetworkAdapter.cpp"

void objectSimulation();
void networkAdapterTest(int argc, char** argv);
void containerSimulation();
void containerMpiSimulation(int argc, char** argv);

int main(int argc, char** argv){
    //networkAdapterTest(argc, argv);
    //containerSimulation();
    containerMpiSimulation(argc, argv);
    //objectSimulation();
}

void containerMpiSimulation(int argc, char** argv){
    MPI_Init(&argc, &argv);
    int rank{};
    int size{};
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    auto *networkAdapter = new NetworkAdapter();
    if(rank == 0) {
        FixedOutDegree fixedOutDegree(3, false);
        Nucleus nucleus1 = form_nuclei("1", 4);
        Nucleus nucleus2 = form_nuclei("2", 4);
        Nucleus nucleus3 = form_nuclei("g", 1, GENERATOR);
        fixedOutDegree.connect(nucleus1, nucleus2, 10, 100000);
        fixedOutDegree.connect(nucleus2, nucleus1, 10, 100000);
        fixedOutDegree.connect(nucleus3, nucleus2, 10, 100000);
        Translator translator = Translator(size);
        translator.translate(nucleus);
        SOAContainer *soaContainers = translator.getContainers();
        soaContainers[0].print();
        for(int i = 1; i < size; i++){
            networkAdapter->sendSoaContainer(&soaContainers[i], i);
        }
        auto *simulator = new SOASimulator(soaContainers[0], 0, size);
        simulator->run(100);
    } else{
        SOAContainer *container = networkAdapter->receiveSoaContainer(0);
        auto *simulator = new SOASimulator(*container, rank, size);
        simulator->run(100);
    }
    MPI_Finalize();
}

void containerSimulation(){
    MPI_Init(nullptr, nullptr);
    FixedOutDegree fixedOutDegree(3, false);
    Nucleus nucleus1 = form_nuclei("1", 4);
    Nucleus nucleus2 = form_nuclei("2", 4);
    Nucleus nucleus3 = form_nuclei("g", 1, GENERATOR);
    fixedOutDegree.connect(nucleus1, nucleus2, 10, 10);
    fixedOutDegree.connect(nucleus2, nucleus1, 10, 10);
    fixedOutDegree.connect(nucleus3, nucleus1, 10, 10);
    Translator translator = Translator(1);
    translator.translate(nucleus);
    cout << "translate ok" << endl;
    SOAContainer *soaContainers = translator.getContainers();
    auto *simulator = new SOASimulator(soaContainers[0], 0, 1);
    cout << "got container and simulator" << endl;
    simulator->run(100);
    MPI_Finalize();
}

void networkAdapterTest(int argc, char** argv){
    MPI_Init(&argc, &argv);
    int rank{};
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    auto *networkAdapter = new NetworkAdapter();
    if(rank == 0) {
        FixedOutDegree fixedOutDegree(3, false);
        Nucleus nucleus1 = form_nuclei("1", 4);
        Nucleus nucleus2 = form_nuclei("2", 4);
        Nucleus nucleus3 = form_nuclei("g", 1, GENERATOR);
        fixedOutDegree.connect(nucleus1, nucleus2, 10, 10);
        fixedOutDegree.connect(nucleus2, nucleus1, 10, 10);
        fixedOutDegree.connect(nucleus3, nucleus1, 10, 10);
        Translator translator = Translator(1);
        translator.translate(nucleus);
        SOAContainer *soaContainers = translator.getContainers();
        soaContainers[0].print();
        networkAdapter->sendSoaContainer(soaContainers, 1);
    } else{
        SOAContainer *container = networkAdapter->receiveSoaContainer(0);
        container->print();
    }
    MPI_Finalize();
}

void objectSimulation() {
    FixedOutDegree fixedOutDegree(10, false);
    Nucleus nucleus1 = form_nuclei("1", 10, GENERATOR);
    Nucleus nucleus2 = form_nuclei("2", 10);
    fixedOutDegree.connect(nucleus1, nucleus2, 5, 5000);
    NucleusListener listener(&nucleus[1]);
    for(int i = 0; i < 100; i++){
        Nucleus *current;
        for(int j = 0; j < nucleus.size(); j++) {
            current = &nucleus[j];
            for (int nrn = 0; nrn < current->neurons.size(); nrn++) {
                //printf("Im still alive %d, %d, %d\n", i, j, nrn);
                update_neuron(&current->neurons[nrn], 0, false);
                update_synapse(&current->neurons[nrn]);
            }
            listener.listen();
        }
    }
    for(auto & i : *listener.getV_m()){
        printf("%d\n", i);
    }
}

