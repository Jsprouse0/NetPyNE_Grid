#!/bin/sh
cd /home/developer/
export SOCNAME="/home/developer/Code/NetPyNE_Grid/netpyne/netpyne/batchtools/examples/M1/grid_batch/grid_search_00000.s"
export JOBID=$$

export STRRUNTK0="sec=soma"
export FLOATRUNTK1="weight=0.001"
export STRRUNTK2="saveFolder=/home/developer/Code/NetPyNE_Grid/netpyne/netpyne/batchtools/examples/M1/grid_batch"
export STRRUNTK3="simLabel=grid_search_00000"
nohup python /home/developer/Code/NetPyNE_Grid/netpyne/netpyne/batchtools/examples/M1/init.py > /home/developer/Code/NetPyNE_Grid/netpyne/netpyne/batchtools/examples/M1/grid_batch/grid_search_00000.run 2>&1 &
pid=$!
echo $pid >&1
