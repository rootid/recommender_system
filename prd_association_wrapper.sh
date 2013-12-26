#!/bin/sh
#format <algo_file> <item_to_be_associated/movie_id>
#output format 
#ASSOCIATED MOVIE FOR   11  FORMAT = X_MOVIE,Y_MOVIE,RATING, SIMPLE
#11 , 1.0 , 603 , 0.96 , 1891 , 0.94 , 1892 , 0.94 , 120 , 0.93 , 
#ASSOCIATED MOVIE FOR   11  FORMAT = X_MOVIE,Y_MOVIE,RATING, ADV
#11 , 2219.0 , 1891 , 5.69 , 1892 , 5.65 , 243 , 4.94 , 1894 , 4.72 ,
./prd_association.py 11
