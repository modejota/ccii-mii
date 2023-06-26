execute:
	/opt/spark-3.0.1-bin-hadoop2.7/bin/spark-submit --master spark://ulises:7077 --total-executor-cores 8 --executor-memory 8g main.py

move_correlation_matrix:
	hdfs dfs -put correlation_matrix.txt/ /user/xxmodej/

merge_correltaion_matrix:
	hdfs dfs -getmerge /user/xxmodej/correlation_matrix.txt/ correlation_matrix_merged.txt