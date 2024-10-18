#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate mlst_check

mlst $1
