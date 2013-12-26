#!/bin/bash
#./SVD_wrapper.sh <input.txt> 
IFS=$'\n' 
ips=($(cat ${1})) 
global_mean_op="global_mean.out"
item_mean_op="item_mean.out"
user_mean_op="user_mean.out"
item_user_mean_op="item_user_mean.out"
for line in ${ips[@]}
do
    user=`echo ${line} | cut -d ':' -f1`
    movie=`echo ${line} | cut -d ':' -f2`
    ./SVD_global_mean.py ${user} ${movie} >> ${global_mean_op}
    ./SVD_item_mean.py ${user} ${movie} >> ${item_mean_op}
    ./SVD_user_mean.py ${user} ${movie} >> ${user_mean_op}
    ./SVD_item_user_mean.py ${user} ${movie} >> ${item_user_mean_op}
done
