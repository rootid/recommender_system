#!/usr/bin/python 
import sys
import numpy as np
import math
from scipy import stats

pearson_correlation_ip_file = 'pearson_conv.csv'
pearson_rating_ip = 'data_sample_u_u_pearson.csv'
FMT = "%.3f" 
class UserWt:
    def __init__(self,user,wt):
        self.user = user
        self.wt = wt
    def __repr__(self):
        return repr((self.user, self.wt))
    def __getitem__(self, item):
        return (self.user, self.wt)[item]



def create_user_lookup(lookup_map,line,delim=',',start_f=1):
    fs = line.split(delim)
    index = 0
    size_ = len(fs)
    for i in range(start_f,size_) :
        lookup_map[index] = fs[i]
        index += 1

def pearson_def(x, y):
    np.set_printoptions(precision=4)
    #Remove Nan entries
    x_ = x[~np.isnan(x)]
    y_ = y[~np.isnan(y)]
    avg_x = np.mean(x_)
    avg_y = np.mean(y_)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    n = max(len(x),len(y))
    cnt_ = 0
    for idx in range(0,n):
        if (math.isnan(x[idx]) == True)  or (math.isnan(y[idx]) == True)  :
            #print "NAN",
                continue
        else :
            cnt_ += 1
            xdiff = x[idx] - avg_x
            ydiff = y[idx] - avg_y
            diffprod += xdiff * ydiff
            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff
    #print cnt_
    return diffprod / math.sqrt(xdiff2 * ydiff2)

def create_movie_lookup(lookup_map,line,delim=':',start_fs=1):
    pass

def init_rating_map(rating_map,user_lookup,number_of_movies) :
    for k,v in user_lookup.iteritems():
        arr = np.zeros( (number_of_movies ) )
        rating_map [k] = arr

def create_user_matrix (user_rating_map,fs,start=1,tuple_cnt=0):
    tlen = len(fs)
    #print str(tlen) + " " + str(tuple_cnt)
    for i in range(start,tlen):
        arr = user_rating_map[i-1]
        if fs[i] == '':
            #arr[tuple_cnt] = 0
            arr[tuple_cnt] = None
        else :
            arr[tuple_cnt] = float(fs[i])

fd = open(pearson_rating_ip,'r')
all_users = fd.readline().rstrip('\n')
user_lookup_map = {}
#user_lookup_map = 
create_user_lookup(user_lookup_map,all_users)
movie_lookup = {}
user_rating_map = {}
#print user_lookup_map 
number_of_movies = 100
number_of_users = len(user_lookup_map.keys())
m_index = 0

for line in fd :
    line = line.rstrip('\n')
    #print str(m_index)
    fs = line.split(',')
    movie_lookup [m_index] = fs[0]
    if user_rating_map == {} :
        init_rating_map(user_rating_map,user_lookup_map,100)
    create_user_matrix(user_rating_map,fs,1,m_index)
    m_index += 1


#print user_rating_map[0]
#print user_rating_map[1]
#print user_lookup_map
#print movie_lookup  

#len_ = len(user_rating_map.keys())
#print len_
#for i in range(0,len_):
#    for j in range(0,len_):
#        ans_ = pearson_def(user_rating_map[i],user_rating_map[j])
#        print format(ans_ , '.5f') ,
#    print " "



USER_ = 6
MOVIE = 55
conv_mat  = np.loadtxt(pearson_correlation_ip_file,delimiter=',')
#print conv_mat.shape
#print  movie_lookup.get(MOVIE)
#print user_lookup_map.get(USER_)

def with_normalization() :
    user_len = len(user_lookup_map.keys())
    movies_len = len(movie_lookup.keys())
    for u_id in range(user_len) :
        q_user = user_rating_map[u_id]
        q_user_= q_user[~np.isnan(q_user)]
        r_u_bar = np.mean(q_user_)
        m_tuple = []
        user_lst = conv_mat[u_id,:]
        for m_id in range(movies_len) :
            len_ = len (user_lst)
            user_obj  = []
            for i in range(len_) :
                user_obj.append(UserWt (i,user_lst[i]))
            user_obj = sorted(user_obj, key=lambda user_wt: user_wt.wt,reverse=True)
            #Get the simillar test user
            sim_user_lst = []
            for i in range(6):
                if float(user_obj[i][1]) == 1.0 :
                    pass
                else :
                    sim_user_lst.append( (user_obj[i]))
            len_ = len(sim_user_lst)
            total_wt = 0.0
            total_rating = 0.0
            for i in range(len_):
                u_obj = sim_user_lst[i]
                user = u_obj[0]
                r_user = user_rating_map[user]
                r_user_= r_user[~np.isnan(r_user)]
                r_n_bar = np.mean(r_user_)
                #print user
                rn = user_rating_map.get(user)[m_id] #rating for movie 55
                #wn = conv_mat[4][i] #weightage
                wn = u_obj[1]
                #print str(wn) + " " + str(rn)
                if math.isnan(user_rating_map.get(user)[m_id]):
                    #print "NAN"
                    wn = 0.0
                    rn = 0.0
                rn = rn - r_n_bar 
                total_wt += wn
                temp = wn * rn
                total_rating += temp
            if total_wt != 0.0 :
                ans = (total_rating/total_wt)
                ans += r_u_bar
                t_ans = FMT % (ans)
                m_tuple.append( (t_ans,m_id) )
            #print t_ans 
        
        m_sort = sorted(m_tuple, key=lambda ans_: ans_[0],reverse=True)  
        #print m_sort
    
        print user_lookup_map.get(u_id).strip('"')
        for i in range(4) :
            m_tuple = m_sort[i]
            m_name = movie_lookup.get(m_tuple[1])
            print m_name.split(':')[0][1:]  + " " + m_tuple[0]


def w_o_normalization() :
    user_len = len(user_lookup_map.keys())
    movies_len = len(movie_lookup.keys())
    for u_id in range(user_len) :
        m_tuple = []
        user_lst = conv_mat[u_id,:]
        for m_id in range(movies_len) :
            len_ = len (user_lst)
            user_obj  = []
            for i in range(len_) :
                user_obj.append(UserWt (i,user_lst[i]))
            user_obj = sorted(user_obj, key=lambda user_wt: user_wt.wt,reverse=True)
            #print user_obj
            
            #Get the simillar test user
            sim_user_lst = []
            for i in range(6):
                if float(user_obj[i][1]) == 1.0 :
                    #print "Found "+ str(i) + " " + str (user_obj[i])
                    pass
                else :
                    #print str(i) + " " + str(user_obj[i])
                    #print user_lookup_map.get(user_obj[i][0])
                    sim_user_lst.append( (user_obj[i]))
                    #print user_obj[i][1]
            #now predict rating for each movie
            #predict rating for movie 55 for user 4
            len_ = len(sim_user_lst)
            total_wt = 0.0
            total_rating = 0.0
            for i in range(len_):
                u_obj = sim_user_lst[i]
                user = u_obj[0]
                #print user
                rn = user_rating_map.get(user)[m_id] #rating for movie 55
                #wn = conv_mat[4][i] #weightage
                wn = u_obj[1]
                #print str(wn) + " " + str(rn)
                if math.isnan(user_rating_map.get(user)[m_id]):
                    #print "NAN"
                    wn = 0.0
                    rn = 0.0
                total_wt += wn
                temp = wn * rn
                total_rating += temp
            if total_wt != 0.0 :
                ans = (total_rating/total_wt)
                t_ans = FMT % (ans)
                m_tuple.append( (t_ans,m_id) )
            #print t_ans 
        
        m_sort = sorted(m_tuple, key=lambda ans_: ans_[0],reverse=True)  
        #print m_sort
    
        print user_lookup_map.get(u_id).strip('"')
        for i in range(4) :
            m_tuple = m_sort[i]
            m_name = movie_lookup.get(m_tuple[1])
            print m_name.split(':')[0][1:]  + " " + m_tuple[0]

with_normalization()
#w_o_normalization()
