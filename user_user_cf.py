#!/usr/bin/python
import sys
import numpy as np
import math
from scipy import stats

#movie is item 
FMT = "%.4f" 
NBR_THRESHOLD = 30
MOVIE_TITLE_FILE = "movie-titles.csv"
RATING_FILE = "ratings.csv"
USER_FILE ="users.csv"


def create_lookup(lookup_map,fd,delim=','):
    index = 0
    for line in fd:
        f_line = line.rstrip('\n')
        fs = f_line.split(delim)
        size_ = len(fs)
        lookup_map[float(fs[0])] = (index,fs[1])
        index += 1



#user X item matrix
def create_rating_matrix(rating_fd,user_lookup_map,movie_lookup_map):
    row = len(user_lookup_map.keys())
    col = len(movie_lookup_map.keys())
    #user_rating_mat = np.empty((row,col))
    #user_rating_mat[:] = np.NAN
    user_rating_mat = np.zeros((row,col))
    for line in rating_fd:
        line = line.rstrip('\n')
        fs = line.split(',')
        user = float(fs[0])
        movie = float(fs[1])
        rating = float(fs[2])
        user_id = user_lookup_map.get(user)[0]
        movie_id = movie_lookup_map.get(movie)[0]
        user_rating_mat[user_id][movie_id] = rating
    return user_rating_mat

def compute_mean (x_) :
    t = x_[x_.nonzero()]
    return np.mean(t)


def compute_mean_centerd_matrix (x):
    avg_x = compute_mean (x)
    x_len = len(x)
    t = np.zeros((x_len))
    for i in range(x_len):
        if (x[i] != 0) :
            t[i] = x[i] - avg_x
    return t 

def compute_cosine_sim(x_,y_,x_v=None,y_u=None):
    num = np.dot(x_,y_)
    den = np.linalg.norm(x_,ord=2) * np.linalg.norm(y_,ord=2)
    if den != 0 :
        return (num/den)
    else :
        return 0
    #else :
    #    print den
    #    return den
#if den != 0.0 :
#        tmp = num/den
#    else :
#        tmp = 0.0
#       # print "Y VALUE ",
#       # print y_
#       # print "VV ",
#       # print x_v
#    return tmp

def predict_item_rating(user_u_,sim_uv,rating_v,user_lookup_map,m_id):
    mu_u = compute_mean(user_u_)
    #print user_u_
    #print mu_u 
    t_len = len(sim_uv)
    den = 0.0
    num = 0.0
    tmp = 0.0
    for i in range (t_len):
        (v_uid,sim_score) = sim_uv[i]
        v_id = user_lookup_map.get(v_uid) [0]
        norm_rating_v = rating_v[v_id][m_id]
        if (norm_rating_v != 0) :
            mu_v = compute_mean(rating_v[v_id,:])
            norm_rating_v = norm_rating_v - mu_v
            num += (sim_score * norm_rating_v)
            den += abs(sim_score)
        else :
            print "Found " + str(user_lookup_map.get(v_uid)) +" " + str(v_id)
    tmp = (num / den)
    tmp += mu_u
    return tmp


#get user and item as input
predict_ip = sys.argv[1]
ip_ = predict_ip.split(':')
ip_user = float(ip_[0])
ip_item = float(ip_[1])
sim_tuple = []
user_lookup_map = {}
movie_lookup_map= {}
u_fd = open(USER_FILE,'r')
create_lookup(user_lookup_map,u_fd)
m_fd = open(MOVIE_TITLE_FILE,'r')
create_lookup(movie_lookup_map,m_fd)
rating_fd = open(RATING_FILE,'r')
user_rating_mat = create_rating_matrix (rating_fd,user_lookup_map,movie_lookup_map)
m_id = movie_lookup_map.get(ip_item)[0]
user_id_u = user_lookup_map.get(ip_user)[0]
user_u_nc = user_rating_mat[user_id_u,:] 
user_u = compute_mean_centerd_matrix( user_u_nc )

for k,v in user_lookup_map.iteritems():
    user_id_v = user_lookup_map.get(k)[0]
    if (user_id_u != user_id_v):
        user_v = compute_mean_centerd_matrix( user_rating_mat[user_id_v,:] )
        cos_sim = compute_cosine_sim(user_u,user_v,user_lookup_map.get(k)[1])
        sim_tuple.append( (k,cos_sim) )

sim_sort = sorted(sim_tuple, key=lambda ans_: ans_[1],reverse=True)  

sim_mat = []
r_index_ = 0
for i in range(1000):
    (v_uid,sim_score) = sim_sort[i]
    v_id = user_lookup_map.get(v_uid) [0]
    rating_v = user_rating_mat[v_id][m_id]
    if (r_index_  == NBR_THRESHOLD) :
        break
    if (rating_v != 0 ) :
        sim_mat.append(sim_sort[i])
        r_index_ += 1
       
ans = predict_item_rating(user_u_nc,sim_mat,user_rating_mat,user_lookup_map,m_id)
t_ans = FMT % (ans)
print str(ip_[0]) +","+ str(ip_[1]) + "," +str(t_ans) +","  + str(movie_lookup_map.get(ip_item)[1])[:-1]
          
