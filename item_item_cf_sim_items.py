#!/usr/bin/env python
import sys
import numpy as np
import math
from scipy import stats

#NOTE : 
#Case 1. Single movie/items
#Get top n ratings
#Case 2 : Multiple movie/items
#Arrange all nbrs in descending order add the total score and select the rating
#FOR computation purpose internally ids(user,movie) are presented sequentially
#Item-Item simillarity with cosine simillarity
#0.Compute normalized matrix
#1.Compute sim matrix
#2.Order sim matrix
#3.Compute rating based on rating,normalized rating and simillarity

FMT = "%.4f" 
MOVIE_TITLE_FILE = "movie-titles.csv"
RATING_FILE = "ratings.csv"
USER_FILE ="users.csv"
NBR_SIZE = 20


def compute_mean (x_) :
    t = x_[x_.nonzero()]
    #print t.shape
    return np.mean(t)

def get_normal  (x_) :
    tlen = np.size(x_)
    t = 0.0
    for i in range(tlen) :
        t += math.pow (x_[i] ,2)
    t_sq = math.sqrt(t)
    return t_sq 

def compute_cosine_sim(x_,y_,x_v=None,y_u=None):
    num = np.dot(x_,y_)
    #print num , np.linalg.norm(x_,ord=2) , np.linalg.norm(y_,ord=2)
    #print "X NORMAL = " , get_normal (x_) , "Y NORMAL = ",get_normal(y_)
    den = np.linalg.norm(x_v,ord=2) * np.linalg.norm(y_u,ord=2)
    if den != 0 :
        return (num/den)
    else :
        return 0

def create_lookup(lookup_map,fd,delim=','):
    index = 0
    for line in fd:
        f_line = line.rstrip('\n')
        fs = f_line.split(delim)
        size_ = len(fs)
        lookup_map[float(fs[0])] = (index,fs[1])
        index += 1

def create_rating_matrix(rating_fd,user_lookup_map,movie_lookup_map):
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
        user_id = user_lookup_map.get(user)[0]
        movie_id = movie_lookup_map.get(movie)[0]
        user_rating_mat[user_id][movie_id] = rating
        if movie == 77 :
            i+= 1
            m_ii = movie_id 
            uii_id = user_id

        elif movie == 38 :
            j += 1
            m1_ii = movie_id 
            uii1_id = user_id

    #print "77 Rating", i , m_ii, uii_id, "38 Ratings = ",j,m1_ii,uii1_id 
    #print "77 ", np.count_nonzero(user_rating_mat[:,m_ii]), "38 Rating" ,np.count_nonzero(user_rating_mat[:,m1_ii])
    return user_rating_mat

#matix 5564x100
def normalize_user_rating_mat (user_rating_mat) :
    norm_rating_mat = np.zeros((user_rating_mat.shape))
    for k,v in user_lookup_map.iteritems() :
        (u_id,u_name) = v
        temp_mat = user_rating_mat[u_id,:] 
        #print np.size(temp_mat)
        temp_mean = compute_mean (temp_mat)
        #print temp_mean
        norm_rating_mat [u_id,:] = user_rating_mat[u_id,:] 
        b = norm_rating_mat [u_id,:] - temp_mean
        norm_rating_mat [u_id,:] = b
    #print "user rating shape",user_rating_mat.shape
    return norm_rating_mat 


def get_co_rated_vector(u,u_id,v,v_id,user_rating_mat) :
    t_size = np.size(u)
    u1 = np.zeros((t_size))
    v1 = np.zeros((t_size))
    #print "Asize(U) = ", np.size(u1) ," Asize(V) = ",np.size(v1)
    for i in range(t_size) :
        if (user_rating_mat[i][u_id] > 0) and (user_rating_mat[i][v_id] > 0) :
            u1[i] = u[i]
            v1[i] = v[i]
    #print "size(U) = ", np.count_nonzero(u1) ," size(V) = ",np.count_nonzero(v1)
    return (u1,v1) 

def get_non_negative_vector(u,u_id,v,v_id,user_rating_mat) :
    t_size = np.size(u)
    u1 = np.zeros((t_size))
    v1 = np.zeros((t_size))
    #print "Asize(U) = ", np.size(u11) ," Asize(V) = ",np.size(v11)
    for i in range(t_size) :
        if (user_rating_mat[i][u_id] > 0)  :
            u1[i] = u[i]
        if (user_rating_mat[i][v_id] > 0) :
            v1[i] = v[i]
    #print "size(U) = ", np.count_nonzero(u11) ," size(V) = ",np.count_nonzero(v11)
    return (u1,v1) 


def compute_sim_matrix () :
    #print u_item_id 
    #print "NORM RATING VECTOR",norm_rating_mat[:,u_item_id]
    #print  "USER RATING VECTOR",user_rating_mat [:,u_item_id]
    for k,v in movie_lookup_map.iteritems() :
        (item_id,item_name) = v
        if item_id != u_item_id :
            u_i = norm_rating_mat[:,u_item_id]
            n_i = norm_rating_mat[:,item_id]
            (u,v) = get_co_rated_vector (n_i,item_id,u_i,u_item_id,user_rating_mat)
            (u1,v1) = get_non_negative_vector (n_i,item_id,u_i,u_item_id,user_rating_mat)
            item_sim = compute_cosine_sim (u,v,u1,v1)
            #sim_mat.append((rev_lookup_map.get(item_id),item_sim))
            sim_mat.append((item_id,item_sim))
    sim_matrx_srt = sorted(sim_mat, key=lambda ans_: ans_[1],reverse=True)  
    return sim_matrx_srt 



def get_top_n_sim (n,sim_mat) :
    for i in range(n) :
        (item_id,score) = sim_mat[i]
        movie_id = rev_lookup_map.get(item_id)
        (u_item_id ,item_name)= movie_lookup_map.get(movie_id)
        print "%d,%.4f,%s" % (movie_id,score,item_name)


user_lookup_map = {}
movie_lookup_map = {}
u_fd = open(USER_FILE,'r')
create_lookup(user_lookup_map,u_fd)
m_fd = open(MOVIE_TITLE_FILE,'r')
create_lookup(movie_lookup_map,m_fd)
rev_lookup_map = {}
for k,v in movie_lookup_map.iteritems() :
    rev_lookup_map [v[0]] = k


#print "MOVIE LOOKUP 77" ,movie_lookup_map.get(77)
#print "USER LOOKUP 2048" ,user_lookup_map.get(2048)
rating_fd = open(RATING_FILE,'r')
user_rating_mat = create_rating_matrix (rating_fd,user_lookup_map,movie_lookup_map)
#print "USER RATING MAT = ", user_rating_mat[1,:]
norm_rating_mat = normalize_user_rating_mat (user_rating_mat)
#print "NORM RATING MAT = ", norm_rating_mat [1,:]
#print "USER RATING MAT = ", user_rating_mat[1,:]

sim_mat = []
iid = int(sys.argv[1])
no_ = int (sys.argv[2])
(u_item_id ,item_name)= movie_lookup_map.get(iid)
sim_mat = compute_sim_matrix ()
get_top_n_sim (no_,sim_mat)
