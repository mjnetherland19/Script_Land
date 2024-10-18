#!/bin/bash

assembly=$1
reference=$2

eval "$(conda shell.bash hook)"
conda activate ntjoin

ntJoin assemble target=$assembly references=$reference reference_weights=2
