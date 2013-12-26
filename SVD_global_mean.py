#!/usr/bin/env python
import sys
import numpy as np
import math
from scipy import stats

FMT = "%.4f" 
MOVIE_TITLE_FILE = "movie-titles.csv"
RATING_FILE = "ratings.csv"
USER_FILE ="users.csv"
NBR_SIZE = 20
FEATURE_SIZE = 10


def compute_mean (x_) :
    t = x_[x_.nonzero()]
    #print t.shape
    return np.mean(t)

def create_lookup(lookup_map,fd,delim=','):
    index = 0
    for line in fd:
        f_line = line.rstrip('\n')
        fs = f_line.split(delim)
        lookup_map[float(fs[0])] = (index,fs[1])
        index += 1

def create_rating_matrix(rating_fd,user_lookup_map,movie_lookup_map):
    total_sum = 0
    total_no_of_rating = 0
    row = len(user_lookup_map.keys())
    col = len(movie_lookup_map.keys())
    user_rating_mat = np.zeros((row,col))
    i = 0
    j = 0
    for line in rating_fd:
        line = line.rstrip('\n')
        fs = line.split(',')
        user = float(fs[0])
        movie = float(fs[1])
        rating = float(fs[2])
        total_no_of_rating += 1
        total_sum += rating 
        user_id = user_lookup_map.get(user)[0]
        movie_id = movie_lookup_map.get(movie)[0]
        user_rating_mat[user_id][movie_id] = rating
    mean = total_sum / total_no_of_rating 
    #print "Mean = ",mean
    return user_rating_mat

def get_norm_matrix (user_mat,mean) :
   #print "get_norm_matrix user_mat[4][5]",user_mat[4][5]
   (row,col) =  user_mat.shape
   user_norm_rating_mat = np.zeros((row,col))
   for i in range(row) :
       for j in range(col):
           #DO NOT CONSIDER rating matrix with zero
           if (user_mat[i][j] != 0) :
               user_norm_rating_mat[i][j] = user_mat[i][j] - mean
   return user_norm_rating_mat 


#Algorithm
#1.create all necessary lookups
#2.Compute global mean
#3.Get input matrix for SVD after original_matrix - global mean.
#4.Transpose SVD item matrix 
#4.Reduce the matrix w.r.t. feature size parameter.
#5.Compute the simillarity /dot product among svd matrix and select the entry from svd with given user and item.
#6.Compute global mean (bias)
#7. Ans = sim + bias
user_lookup_map = {}
movie_lookup_map = {}
u_fd = open(USER_FILE,'r')
create_lookup(user_lookup_map,u_fd)
m_fd = open(MOVIE_TITLE_FILE,'r')
create_lookup(movie_lookup_map,m_fd)
rating_fd = open(RATING_FILE,'r')

#create rating matrix (5563x100)
user_rating_mat = create_rating_matrix (rating_fd,user_lookup_map,movie_lookup_map)
global_mean  = compute_mean(user_rating_mat)
non_z = np.nonzero(user_rating_mat)
norm_global_rating_mat = get_norm_matrix (user_rating_mat,global_mean)
U,s,V = np.linalg.svd(norm_global_rating_mat, full_matrices=False)
Vt = np.transpose (V)
U_red = U[:,0:FEATURE_SIZE]
s_red = s [0:FEATURE_SIZE]
S_red = np.diag(s_red)
V_red_t = Vt [:,0:FEATURE_SIZE]

uid = user_lookup_map.get(int(sys.argv[1])) [0]
iid,item_name = movie_lookup_map.get(int(sys.argv[2]))

m1 = U_red[uid,:]
m2 = s_red
m3 = V_red_t [iid,:]

sim_ = m1*(m2)*(m3)
t_sim = sum(sim_)
ans = global_mean + t_sim
print "%d,%d,%.4f,%s" % (int(sys.argv[1]),int(sys.argv[2]),ans,item_name)

