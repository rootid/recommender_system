#!/bin/sh
#.user_user_cf_wrapper.sh user_user_cf_input.txt
user_user_cf_op="user_user_cf.out"
while read line
do
    ./user_user_cf.py ${line} >> ${user_user_cf_op}
done <${1}
