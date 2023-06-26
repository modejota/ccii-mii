import pyspark

if __name__ == "__main__":

  input_file = "hdfs://ulises.imuds.es:8020/user/xxmodej/james-joyce-ulysses.txt"
  output_folder = "hdfs://ulises.imuds.es:8020/user/xxmodej/wc_joyce/"

  # create Spark context with Spark configuration
  sc = pyspark.SparkContext(master='local[*]', appName="Word Count")

  # read in text file and split each document into words
  words = sc.textFile(input_file).flatMap(lambda line: line.split(" "))

  # count the occurrence of each word
  wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)

  wordCounts.saveAsTextFile(output_folder)

  sc.stop()