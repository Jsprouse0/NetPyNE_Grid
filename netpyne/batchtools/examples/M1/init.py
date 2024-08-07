from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from netParams import netParams, cfg
from neuron import h
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
hoc_file_path = os.path.join(script_dir, 'mod/x86_64/.libs/libnrnmech.so')
h.nrn_load_dll(hoc_file_path)

comm.initialize()

sim.createSimulate(netParams=netParams, simConfig=cfg)
print('completed simulation...')

if comm.is_host():
    netParams.save("{}/{}_params.json".format(cfg.saveFolder, cfg.simLabel))
    print('transmitting data...')
    inputs = specs.get_mappings()
    results = sim.analysis.popAvgRates(show=False)

    results['PT5B_loss'] = (results['PT5B'] - 5.0)**2 # example target value
    results['loss'] = (results['PT5B_loss'])
    out_json = json.dumps({**inputs, **results})

    print(out_json)
    
#TODO put all of this in a single function.
    comm.send(out_json)
    comm.close()

#TODO print out config values we want to send, and ensure they are transferred into netParams
# print(netparams.stimTargetParams['NetStim1->PT5B'] : sec)

print(netParams.stimTargetParams['NetStim1->PT5B']['sec'])
print(netParams.stimTargetParams['NetStim1->PT5B']['weight'])
