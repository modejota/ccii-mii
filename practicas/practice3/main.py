# -*- coding: utf-8 -*-
from functions import bateria_tests 

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnan, when, count, col
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler, StandardScaler, MinMaxScaler


CALCULATE_CORRELATION = False   # If True, remove variables with high correlation. Also save the correlation matrix into a file.

# Create the Spark Context and the Spark Session. 
name = "practice3_JoseAlbertoGomezGarcia"
sc = SparkContext(master='local[*]', appName=name)
sc.setLogLevel("WARN")  # Avoid showing unnecessary information in the console.
ss = SparkSession.builder.appName(name).getOrCreate()

# Read the data stored in HDFS. Despite the name, there is no test.csv file.
df = ss.read.csv("hdfs://ulises.imuds.es:8020/user/CCSA2223/ccano/train.csv", header=True, sep=",", inferSchema=True)

# Show the first 5 rows of the data.
# df.show(5)

# Show the schema of the data.
df.printSchema()

# Show the number of rows and columns of the data.
print("Number of rows: ", df.count())
print("Number of columns: ", len(df.columns))

# Check if the dataset have imbalanced classes. This is not the case (1999996 galaxies vs 2000004 stars), no further processing required in this sense.
df.groupby("type").count().show()

##### Data preprocessing and normalization #####

# 1- Change the type of the column "type" from string to double (so instead of classes "galaxy"/"star" we have classes "0.0/1.0")
df = df.withColumn("type", when(col("type") == "galaxy", 0.0).otherwise(1.0).cast("double"))
print("Column type changed to double. New schema: ")
df.printSchema()

# 2- Do we have missing values? 
# According to the documentation, missing values are represented by -9999 and are present in the columns "rowv" and "colv".
# 492 rows with missing values. Compared to 4 million rows, it is a very small percentage, so we can drop them.
print("Number of rows with missing values for column romw: ", df.filter(col("rowv") == -9999).count())
print("Number of rows with missing values for column colv: ", df.filter(col("colv") == -9999).count())

df = df.filter(col("rowv") != -9999)
df = df.filter(col("colv") != -9999)

# There are no missing values (NaN) in the rest of the columns, but we can check it with the following command:
df.select([count(when(isnan(c), c)).alias(c) for c in df.columns]).head()
# We don't have missing values. Output row has all zeros.
# If we had few missing values, we could use df.na.drop() to drop rows with missing values, or df.na.fill() to fill missing values with a specific value.

print("Missing values treated.")

# 3- Create a feature vector with a selected subset of the attributes.

# We remove the classification column and the columns that we consider are not interesting.
non_interesting = ['type', 'objID', 'run', 'camcol', 'field']
selected_features = [col for col in df.columns if col != 'type']
assembler = VectorAssembler(inputCols=selected_features, outputCol="features")
df = assembler.transform(df)

# It overwrites the column "features" with the new feature vector.
if CALCULATE_CORRELATION:
    # Gonna check correlation between features to see if we can remove some features.
    correlation_matrix = Correlation.corr(df, "features").head()
    correlation_array = correlation_matrix[0].toArray()

    # Save the correlation matrix in a file.
    correlation_list = correlation_array.tolist()
    correlation_list.insert(0, df.columns)
    rdd = sc.parallelize(correlation_list)
    rdd.saveAsTextFile("correlation_matrix.txt")
    # This will create a folder. It could be directly save in HDFS, but I prefer to manage it manually. Will need to merge.
    
    threshold = 0.7  # Threshold to consider two features correlated
    correlated_features = []

    for i in range(len(correlation_array)):
        for j in range(i + 1, len(correlation_array)):
            if abs(correlation_array[i][j]) >= threshold:
                correlated_features.append((i, j))
    # Remove one of the features from the correlated pair.
    selected_features = list(range(len(df.columns) - 1))
    for pair in correlated_features:
        feature1 = pair[0]
        feature2 = pair[1]
        if feature1 in selected_features:
            selected_features.remove(feature1)
        elif feature2 in selected_features:
            selected_features.remove(feature2)

    selected_columns = [df.columns[int(i)] for i in selected_features] + [df.columns[-1]]

    print("Number of features before removing correlated features: ", len(df.columns))
    print("Number of features after removing correlated features: ", len(selected_columns))
    
    # Check which features have been removed.
    set_original_columns, set_new_columns = set(df.columns), set(selected_columns)
    print("Features removed: ", list(set_original_columns - set_new_columns))
    # Rebuid the feature vector with the new selected features.
    inputCols = [col for col in selected_columns if col != 'type' and col != 'features']
    df = df.drop("features")
    assembler = VectorAssembler(inputCols=inputCols, outputCol="features")
    df = assembler.transform(df)
    
print("Feature vector created.")

# 4- Normalization 
# scaler = MinMaxScaler(inputCol="features", outputCol="scaledFeatures")    # Use only when Naive Bayes is used, for the rest of methods Standard works quite better.
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=True)
scalerModel = scaler.fit(df)
df = scalerModel.transform(df)
df = df.drop("features")
df = df.withColumnRenamed("scaledFeatures", "features")

print("Normalization done.")

# 5- Split the data set into training and test (80%/20%)
data_train, data_test = df.randomSplit([0.8, 0.2], seed=1701)

print("Data splitted into training and test.")

#####  Create ML models and train them. Evaluate the performance of the model on the test dataset. #####  
print("\nFinished preprocessing. Starting to train models. \n")

# flags = ["logistic_regression", "naive_bayes", "decision_tree", "random_forest"]      # Which methods to execute. Only when MinMaxScaler is used.
flags = ["logistic_regression", "decision_tree", "random_forest"]                       # Which methods to execute. NaiveBayes is not used because it doesn't work with negative values (StandardScaler keeps them).
methods = ["logistic_regression", "naive_bayes", "decision_tree", "random_forest"]      # Strings to identify the methods when saving the results. DO NOT MODIFY THIS LIST.
bateria_tests(ss, data_train, data_test, methods, flags)

print("\nFinished training models. \n")

# Stop the Spark Context
sc.stop()