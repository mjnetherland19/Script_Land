#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate ragtag

ref=$1
query=$2

mkdir ragtag_out

ragtag.py scaffold -o ragtag_out $ref $query
