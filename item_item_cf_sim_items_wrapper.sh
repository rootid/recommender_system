#!/bin/bash
IFS=$'\n' 
ips=($(cat ${1})) 
NBR_SIZE="5"
op="item_item_cf_sim_items.out"
for line in ${ips[@]}
do
    movie=`echo ${line}`
    ./item_item_cf_sim_items.py ${movie} ${NBR_SIZE} >> ${op}
done
