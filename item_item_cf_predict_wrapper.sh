#!/bin/bash
IFS=$'\n' 
ips=($(cat ${1})) 
op="item_item_cf_predict.out"
for line in ${ips[@]}
do
    user=`echo ${line} | cut -d ':' -f1`
    movie=`echo ${line} | cut -d ':' -f2`
    ./item_item_cf_prediction.py ${user} ${movie} >> ${op}
done
