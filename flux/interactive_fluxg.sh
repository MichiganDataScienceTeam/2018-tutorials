#!/bin/bash
qsub \
-I \
-N interactive_job \
-M uniqname@umich.edu \
-m abe \
-A mdstproject_fluxg \
-q fluxg \
-l qos=flux,nodes=1:ppn=2,pmem=8gb,gpus=1,walltime=00:02:00:00 \
-j oe \
-V \
-d "/scratch/mdstproject_fluxg/uniqname/"
