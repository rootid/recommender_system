#!/usr/bin/env python
import sys
import numpy as np
import math
from scipy import stats


'''
Simple: (x and y) / x
Advanced: ((x and y) / x) / ((!x and y) / !x)
For above advanced formula add padding of 1 to each item. TO avoid DBZ
'''

FMT = "%.2f" 
PADD = 1
MOVIE_TITLE_FILE = "movie-titles.csv"
RATING_FILE = "ratings.csv"
USER_FILE ="users.csv"

def init () :
    rating_fd = open(RATING_FILE,'r')
    uniq_user_map = {}
    uniq_movie_map = {}
    rating_map = {} ;
    total_user_lst = []
    for line in rating_fd :
        fs = line.split(',')
        user_id = int(fs[0])
        movie_id = int(fs[1])
        uniq_user_map [user_id] = 1
        uniq_movie_map [movie_id] = 1
        if movie_id not in rating_map:
            lst = []
            lst.append(user_id)
            rating_map[movie_id] = lst
        else :
            lst = rating_map[movie_id]
        lst.append(user_id)
    for key in rating_map.keys() :
        lst = rating_map[key]
        sorted_lst = sorted(lst)
        rating_map[key] = sorted_lst 
    for user_id in uniq_user_map.keys():
        total_user_lst.append(user_id)
    total_user_lst.sort()
    return (rating_map,uniq_movie_map,total_user_lst)

def get_all_x (rating_map,item_x) :
    return len(rating_map[item_x])

def get_intersection_x_y (rating_map,item_x,item_y):
    total_items = 0
    if len(rating_map[item_x]) < len(rating_map[item_y]) :
        min_lst = rating_map[item_x]
        max_lst = rating_map[item_y]
    else :
        min_lst = rating_map[item_y]
        max_lst = rating_map[item_x]
    for item in min_lst :
        for item_2 in max_lst:
            if item == item_2 :
                total_items += 1
                break
            elif item_2 > item:
                break
    return total_items 

def get_not_item_x (item_x,rating_map,total_user_lst):
    x_user_lst = rating_map[item_x]
    not_x_user_lst = []
    for total_user in total_user_lst :
        is_count = True
        for x_user in x_user_lst :
            if (total_user == x_user) :
                #print x_user
                is_count = False
                break
            elif x_user > total_user :
                break
        if (is_count == True) :
            not_x_user_lst.append(total_user)
    #print " list len = ", len(not_x_user_lst)
    return not_x_user_lst

def get_not_item_x_and_y (item_y,rating_map,not_x_users_lst) :
    total_items = 0
    if len(rating_map[item_y]) < len(not_x_users_lst) :
        min_lst = rating_map[item_y]
        max_lst = not_x_users_lst
    else :
        min_lst = not_x_users_lst
        max_lst = rating_map[item_y]
    for item in min_lst :
        for item_2 in max_lst:
            if item == item_2 :
                total_items += 1
                break
            elif item_2 > item:
                break
    return total_items 

def apply_simple_formula (total_x_y,total_x) :
    result = float(total_x_y + PADD)/float(total_x + PADD)
    ans_ = "%.2f" % result 
    return float(ans_)


def apply_advanced_formula (total_x_y,total_x,total_not_in_x_and_y,total_not_x) :
    result = float(total_x_y + PADD)/float(total_x + PADD)
    result_2 = float(total_not_in_x_and_y + PADD)/float(total_not_x + PADD)
    result_3 = float(result) / float(result_2)
    ans_ = "%.2f" % result_3 
    return float(ans_)

def print_top_entries(lst,algo_type,item_x,TOP=5) :
    print "ASSOCIATED MOVIE FOR  ",item_x," FORMAT = X_MOVIE,Y_MOVIE,RATING,",algo_type
    for i in range(0,TOP):
        (movie,rating) = lst[i]
        print movie,",",rating,",",
    print "\n"


item_x = int(sys.argv[1])
option_list = ['SIMPLE','ADV']
(rating_map,uniq_movie_map,total_user_lst ) = init()
not_x_users_lst = get_not_item_x(item_x,rating_map,total_user_lst)
not_x_users_lst.sort()
simple_result_tuple = []
adv_result_tuple = []
for item_y in uniq_movie_map.keys () :
    total_x = get_all_x (rating_map,item_x) 
    total_x_y = get_intersection_x_y(rating_map,item_x,item_y)
    res = apply_simple_formula (total_x_y,total_x)
    simple_result_tuple.append((item_y,res))
    #print "simple result = "res 
    total_not_x = len(not_x_users_lst)
    total_not_in_x_and_y = get_not_item_x_and_y(item_y,rating_map,not_x_users_lst)
    res = apply_advanced_formula (total_x_y,total_x,total_not_in_x_and_y,total_not_x)
    adv_result_tuple.append((item_y,res))
    #print "total not x = ",total_not_x ," total not x and y = " , total_not_in_x_and_y 

simple_result_tuple_sorted = sorted(simple_result_tuple, key=lambda tup: tup[1],reverse=True)
adv_result_tuple_sorted = sorted(adv_result_tuple, key=lambda tup: tup[1],reverse=True)

print_top_entries(simple_result_tuple_sorted,"SIMPLE",item_x)
print_top_entries(adv_result_tuple_sorted,"ADV",item_x)
