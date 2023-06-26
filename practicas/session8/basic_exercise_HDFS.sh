#!bin/bash

# Create 5 files in yout local account
touch part1.dat part2.dat part3.dat part4.dat part5.dat
# Copy files to HDFS
hdfs dfs -put part*.dat /user/CCSA2223/xxmodej/.

# Create the following HDFS folder structure:
#   /test/p1/
#   /train/p1/
#   /train/p2/
hdfs dfs -mkdir /user/CCSA2223/xxmodej/test
hdfs dfs -mkdir /user/CCSA2223/xxmodej/test/p1
hdfs dfs -mkdir /user/CCSA2223/xxmodej/train
hdfs dfs -mkdir /user/CCSA2223/xxmodej/train/p1
hdfs dfs -mkdir /user/CCSA2223/xxmodej/train/p2

# Copy part1 in /test/p1/ and part2 in /train/p2/
hdfs dfs -cp /user/CCSA2223/xxmodej/part1.dat /user/CCSA2223/xxmodej/test/p1/
hdfs dfs -cp /user/CCSA2223/xxmodej/part2.dat /user/CCSA2223/xxmodej/train/p2/

# Move part3, and part4 to /train/p1/
hdfs dfs -mv /user/CCSA2223/xxmodej/part3.dat /user/CCSA2223/xxmodej/train/p1/
hdfs dfs -mv /user/CCSA2223/xxmodej/part4.dat /user/CCSA2223/xxmodej/train/p1/

# Finally merge folder /train/p2 and store as data_merged.txt
hdfs dfs -getmerge /user/CCSA2223/xxmodej/train/p2 data_merged.txt