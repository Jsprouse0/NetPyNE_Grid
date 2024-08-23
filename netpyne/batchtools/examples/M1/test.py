from neuron import h

# Load the compiled mechanisms
h.nrn_load_dll('/home/developer/Code/NetPyNE_Grid/netpyne/netpyne/batchtools/examples/M1/mod/x86_64/.libs/libnrnmech.so')

# Create a section and insert the mechanism
NMDA = h.Section(name='NMDA')
syn = h.MyExp2SynNMDABB(NMDA(0.5))

print('Mechanism inserted successfully')