#!/usr/bin/python
import sys
import numpy as np
import math
#
#./content.py 

#1.Create user profile vector
#2.
# read movies ratings
# extract all the terms
# create and initilize vector


MOVIE_TAG_FILE = "movie-tags.csv"
MOVIE_TITLE_FILE = "movie-titles.csv"
USER_FILE = "users.csv"
RATING_FILE = "ratings.csv"

def init_vector(row_size=0, col_size=0):
    tf_v = np.zeros((row_size, col_size))
    return tf_v


def print_all_map_info(ip_map):
    # print ip_map
    for k, v in ip_map.iteritems():
        print "Key : " + str(k) + " value: " + str(v)


def inc_map_cnt(k, ip_map):
    if (k in ip_map):
        cnt = ip_map[k]
        cnt += 1
        ip_map[k] = cnt
    else:
        ip_map[k] = 1


#def get_movie_lookup(file_name, delim=','):
#    look_up_map = {}
#    fd = open(file_name, 'r')
#    movie_id = -1
#    prev_movie_id = -2
#    index = -1
#    for line in fd:
#        fs = line.split(delim)
#        movie_id = int(fs[0])
#        if (prev_movie_id != movie_id):
#            prev_movie_id = movie_id
#            index += 1
#            look_up_map[movie_id] = index
#    return look_up_map

def get_movie_lookup (file_name, delim=',') :
    look_up_map = {}
    fd = open(file_name, 'r')
    index = 0
    for line in fd :
        fs = line.split(',')
        movie_id = int(fs[0])
        look_up_map[movie_id] = (index,fs[1])
        index += 1
    return look_up_map 



def get_lookup_map(file_name, tag_index=1, delim=','):
    fd = open(file_name, 'r')
    index = -1
    look_up_map = {}
    for line in fd:
        fs = line.split(',')
        key = fs[tag_index]
        if key not in look_up_map:
            index += 1
            look_up_map[key] = index
    return look_up_map


def compute_tf_v(file_name, tf_v, movie_lookup_map, tag_lookup_map, delim=','):
    fd = open(file_name, 'r')
    for line in fd:
        fs = line.split(",")
        doc_key = int(fs[0])
        tag_key = fs[1]
        doc_id = movie_lookup_map[doc_key]
        tag_id = tag_lookup_map[tag_key]
        cnt = tf_v[doc_id][tag_id]
        cnt += 1
        # print str(doc_id) + "," + str(tag_id) + "=" + str(cnt)
        tf_v[doc_id][tag_id] = cnt
    return tf_v

#returns TF_vector 4209X100
def t_compute_tf_v(tag_file,movie_lookup_map, tag_lookup_map, delim=','):
    no_row = len(tag_lookup_map)  # 4209
    no_col = len(movie_lookup_map)  # 100
    tf_v = np.zeros((no_row, no_col))
    fd = open(tag_file, 'r')
    cnt = 0
    for line in fd:
        fs = line.split(",")
        doc_key = int(fs[0])
        tag_key = fs[1]
        tag_id = tag_lookup_map[tag_key]
        doc_id = movie_lookup_map[doc_key][0]
        cnt = tf_v[tag_id][doc_id]
        cnt += 1
        tf_v[tag_id][doc_id] = cnt
    return tf_v

def compute_idf(tf_v):
    (row, col) = tf_v.shape
    D = row
    idf_v = np.zeros((col, col))
    for i in range(0, col):
        arr = np.nonzero(tf_v[:, i])[0]
        d_len = len(arr)
        idf = math.log(D / (1 + d_len))
        idf_v[i][i] = idf
        #print idf
        # print str(arr) + "= " +str(len(arr))
    return idf_v

#4209X100
def t_compute_tf_idf_unit_from_tf(tf_v,t_id=0,m_id=0):
    (row, col) = tf_v.shape #4209X100
    tf_idf = np.zeros((row,col))
    print "t_compute_idf row = ",row, "col = ",col
    total_no_documents = col
    for i in range(0, row):
        non_zero_ele_x_indices = np.nonzero(tf_v[i,:])[0]
        doc_freq = len(non_zero_ele_x_indices)
        temp_ = float(total_no_documents) / float(doc_freq)
        idf = math.log(temp_)
        tf_idf[i,:] = tf_v[i,:] * idf 
    print "ANS = " , tf_idf[t_id][m_id] #should be 151.577822105
    return tf_idf
#
def t_compute_idf(tf_v,t_id=0):
    (row, col) = tf_v.shape #4209X100
    print "t_compute_idf row = ",row, "col = ",col
    total_no_documents = col
    idf_v = np.zeros((row,))
    for i in range(0, row):
        non_zero_ele_x_indices = np.nonzero(tf_v[i,:])[0]
        doc_freq = len(non_zero_ele_x_indices)
        if (t_id == i) :
            print "DOC FREQ = ",doc_freq 
            temp_ = float(total_no_documents) / float(doc_freq)
            idf = math.log(temp_)
            ans = idf * 57.0
            ans = "%.4f"%(ans)
            print "ANS = ",ans
        idf = math.log(float(total_no_documents) / float(doc_freq))
        idf_v[i] = idf
    return idf_v




def compute_tf_idf_unit(tf, idf):
    tf_idf = np.dot(tf, idf)
    (row, col) = tf_idf.shape
    print "B4" ,tf_idf[0][5], "|" ,tf_idf[99][1242]
    # print row
    # print col
    #ans = 0.0
    norm_lst = []
    # Get L2-norm
    for i in range(0, row):
        ans = 0.0
        for j in range(0, col):
            if (tf_idf[i][j] != 0.0):
                ans += math.pow(tf_idf[i][j], 2)
        ans = math.sqrt(ans)
        norm_lst.append(ans)
    # Apply L2 norm to get the unit vector
    for i in range(0, row):
        for j in range(0, col):
            if (tf_idf[i][j] != 0.0):
                prev_val = tf_idf[i][j]
                tf_idf[i][j] = prev_val / norm_lst[i]

    print "After",tf_idf[0][5],"|",tf_idf[99][1242]

def compute_tf_idf_unit_across_doc(tf_idf,t_id=0,m_id=0) :
    (row, col) = tf_idf.shape
    tf_idf_unit = np.zeros((row,col))
    for i in range(0, col):
        tf_idf_row_unit = np.linalg.norm(tf_idf[:,i],ord=2)
        if (tf_idf_row_unit != 0) :
            tf_idf_unit[:,i] = tf_idf[:,i]/tf_idf_row_unit 
    print "ANS = " ,tf_idf_unit[t_id][m_id] #should be 0.533148195882
    return tf_idf_unit

#This acts as classifer for which value >= 3.5 = 1 else 0
THERSHOLD_RATING = 3.5
#weighted means classifier (over all ratings) for the second part.

#100X5564
def compute_rating_profile_non_weighted(rating_file, user_lookup_map, movie_lookup_map, delim=','):
    fd = open(rating_file, 'r')
    row = len(movie_lookup_map)
    col = len(user_lookup_map)
    user_profile = np.zeros((row, col))
    for line in fd:
        fs = line.split(delim)
        user = fs[0]
        movie_id = int(fs[1])
        rating = float(fs[2])
        d_id = movie_lookup_map[movie_id][0]
        u_id = user_lookup_map[user]
        if (rating >= THERSHOLD_RATING):
            user_profile[d_id][u_id] = 1
        else:
            user_profile[d_id][u_id] = 0
    return user_profile

#100X5564
def compute_weighted_rating(file_name, user_lookup_map, movie_lookup_map, delim=','):
    fd = open(file_name, 'r')
    row = len(movie_lookup_map)
    col = len(user_lookup_map)
    user_profile = np.zeros((row, col))
    for line in fd:
        fs = line.split(delim)
        user = fs[0]
        movie_id = int(fs[1])
        rating = float(fs[2])
        d_id = movie_lookup_map[movie_id][0]
        u_id = user_lookup_map[user]
        user_profile[d_id][u_id] = rating 
    return user_profile

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    t_len = v1.size
    for i in range(t_len):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    print sumyy 
    return sumxy/math.sqrt(sumxx*sumyy)


def t_cosine_sim (u,item) :
    dot_prd = u * item
    len_ = dot_prd.size
    dot_ans = 0
    for i in range (len_) :
        dot_ans += dot_prd [i]
    u_bar = np.linalg.norm(u,ord=2)
    i_bar = np.linalg.norm(item,ord=2)
    #print "i bar ",i_bar  #value is 1 when we use tf_idf
    den = u_bar * i_bar 
    ans_ = dot_ans / den
    return ans_ 

#Retruns 4209X5564
def compute_user_profile(rating_profile, tf_idf_u):
                        #100X5564        4209X100
    print "RATING profile shape = ",rating_profile.shape , " TF_IDF_u = ",tf_idf_u.shape
    user_profile =  np.dot(tf_idf_u,rating_profile)
    #user_profile =  tf_idf_u * rating_profile
    return user_profile



def compute_weighted_user_profile(rating_profile, tf_idf_u):
                                    #100X5564        4209X100
    # req user_profile = 5564x4209
    print "RATING profile shape = ",rating_profile.shape , " TF_IDF_u = ",tf_idf_u.shape
    (row,col) = rating_profile.shape
    for uid in range(col) :
        user_instance = rating_profile[:,uid]
        user_mean = np.mean(user_instance[user_instance.nonzero()])
        rating_profile[:,uid] = rating_profile[:,uid] - user_mean #100
    user_profile =  np.dot(tf_idf_u,rating_profile)
    return user_profile

def get_dot_product(first_v, second_v):
    rlen = first_v.shape[0]
    ans = 0.0
    for i in range(0, rlen):
        if (first_v[i] != 0.0 and second_v[i] != 0):
            mult_ans = first_v[i] * second_v[i]
            ans += mult_ans
    return ans


def print_top_tags_from_movie(tf_idf_unit,m_id,tag_lookup_map) :
    print "print_top_tags_from_movie"
    rev_lookup = {}
    for k,v in tag_lookup_map.iteritems():
        rev_lookup [v] = k
    single_col = tf_idf_unit[:,m_id]
    temp_list = []
    t_len = single_col.size
    for t in range(t_len) :
        temp_list.append((t,single_col[t]))
    srted_tuple = sorted(temp_list, key=lambda score: float(score[1]),reverse=True)
    #inplace sort
    #temp_list.sort(reverse=True)
    #sorted(temp_list,reverse=True) 
    for top in range (10) :
        (id_,val) = srted_tuple [top]
        print id_,"value= " ,val," TAg " ,rev_lookup[id_]

#4209X5564
def print_top_tags_from_user_profile(user_profile,u_id,tag_lookup_map) :
    print "print_top_tags_from_user_profile"
    rev_lookup = {}
    for k,v in tag_lookup_map.iteritems():
        rev_lookup [v] = k
    single_col = user_profile[:,u_id]
    temp_list = []
    t_len = single_col.size
    print " nonzero elemets = "np.nonzero(single_col)[0] 
    for t in range(t_len) :
        temp_list.append((t,single_col[t]))
    srted_tuple = sorted(temp_list, key=lambda score: float(score[1]),reverse=True)
    for top in range (10) :
        (id_,val) = srted_tuple [top]
        print id_,"value= " ,val," TAg " ,rev_lookup[id_]

def main():
    # Create lookups
    # <tag string with\n,row#>
    # get total number of unique tags
    tag_lookup_map = get_lookup_map(MOVIE_TAG_FILE)
    # <movie_id,(row#,movie_name)>
    movie_lookup_map = get_movie_lookup(MOVIE_TITLE_FILE)
    # <user_id,row#>
    user_lookup_map = get_lookup_map(USER_FILE, 0)
    # Compute term frequency vector
    tf_v = t_compute_tf_v(MOVIE_TAG_FILE,movie_lookup_map,tag_lookup_map)
    print tf_v.shape
    # Compute idf vector unit vector using L2-norm
    t_id = tag_lookup_map["space\n"]
    (m_id,m_name) = movie_lookup_map [11]
    tf_idf = t_compute_tf_idf_unit_from_tf(tf_v,t_id,m_id)
    tf_idf_unit = compute_tf_idf_unit_across_doc(tf_idf,t_id,m_id)
    
    # Compute Rating vector
    user_id = sys.argv[1]
    
    #rating_profile = compute_weighted_rating(RATING_FILE, user_lookup_map, movie_lookup_map)
    #user_profile = compute_weighted_user_profile (rating_profile, tf_idf_unit)
    
    # Compute user profile vector
    rating_profile = compute_rating_profile_non_weighted (RATING_FILE,user_lookup_map,movie_lookup_map)
    user_profile = compute_user_profile(rating_profile, tf_idf_unit)
    
    print "Rating profile shape = " ,rating_profile.shape
    print  "user profile size = ",user_profile.shape
    
    #print_top_tags_from_movie(tf_idf_unit,m_id,tag_lookup_map)
    u_id = user_lookup_map["144"]
    print_top_tags_from_user_profile(user_profile,u_id,tag_lookup_map)

    score_tuple = []
    #Get single user
    user = user_lookup_map["4045"]
    ## Get single user profile
    user_profile_instance = user_profile[:,user]  # 1 x 4209 <--#100X4209
    for k in movie_lookup_map.keys():
        col = (int)(movie_lookup_map.get(k)[0])
        #tf_v_instance = tf_v[:,col]  # 4209
        tf_idf_instance = tf_idf_unit[:,col]  # 4209
        ans_ = t_cosine_sim (user_profile_instance,tf_idf_instance)
        #ans_ = cosine_similarity (user_profile_instance,tf_idf_instance)
        score_tuple.append((k, ans_))
    srted_tuple = sorted(score_tuple, key=lambda score: float(score[1]),reverse=True)
    for i in range (5) :
        (movie,rating) = srted_tuple[i]
        rating = "%.4f" % (rating)
        print movie ,":",rating

if __name__ == "__main__":
    main()
