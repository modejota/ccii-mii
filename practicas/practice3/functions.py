# -*- coding: utf-8 -*-
import time

from pyspark.sql.types import StringType, StructType, StructField
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, GBTClassifier, NaiveBayes, MultilayerPerceptronClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


def bateria_tests(ss, data_train, data_test, labels, what_to_execute):
    """
    Functión para realizar una batería de tests de los modelos de clasificación.
    :param ss: SparkSession
    :param data_train: DataFrame de Spark con los datos de entrenamiento
    :param data_test: DataFrame de Spark con los datos de test
    :param labels: Lista con los nombres de las etiquetas. Utilizados para etiquetar los resultados de los modelos.
    :param what_to_execute: Lista con los nombres de los modelos a ejecutar. [logistic_regression, naive_bayes, decision_tree, random_forest]
    """

    # 1- Logistic Regression
    if "logistic_regression" in what_to_execute:
        print("\nLogistic Regression")
        timeIni = time.time()
        lr = LogisticRegression(featuresCol='features', labelCol='type', maxIter=10, elasticNetParam=0.8)
        grid = ParamGridBuilder().addGrid(lr.regParam, [0.1, 0.01, 0.001, 0.0001]).build()
        evaluator = BinaryClassificationEvaluator(labelCol="type", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
        cv = CrossValidator(estimator=lr, estimatorParamMaps=grid, evaluator=evaluator)
        cv_model = cv.fit(data_train)
        best_model = cv_model.bestModel
        best_lambda = best_model._java_obj.getRegParam()
        timeFin = time.time()

        print("Searching for best lambda: ", timeFin - timeIni, " seconds")
        print("Best lambda: ", best_lambda)

        timeIni = time.time()
        lr = LogisticRegression(featuresCol='features', labelCol='type', maxIter=10, regParam=best_lambda, elasticNetParam=0.8)
        lr_model = lr.fit(data_train)
        timeFin = time.time()
        predictions = lr_model.transform(data_test)
        lr_metrics = evaluate_model(predictions, ss, labels[0])
        print("ROC: ", lr_metrics[0])
        print("Precision: ", lr_metrics[1])
        print("Kappa: ", lr_metrics[2])
        print("Recall: ", lr_metrics[3])
        print("F1: ", lr_metrics[4])
        print("Training time: ", timeFin - timeIni, " seconds")

    # 2- Naive Bayes
    if "naive_bayes" in what_to_execute:
        print("\nNaive Bayes")
        timeIni = time.time()
        nb = NaiveBayes(featuresCol='features', labelCol='type', smoothing=1.0, modelType="multinomial")
        evaluator = BinaryClassificationEvaluator(labelCol="type", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
        grid = ParamGridBuilder().addGrid(nb.smoothing, [0.1, 0.5, 1.0, 2.0]).build()
        cv = CrossValidator(estimator=nb, estimatorParamMaps=grid, evaluator=evaluator)
        cv_model = cv.fit(data_train)
        best_model = cv_model.bestModel
        best_smoothing = best_model._java_obj.getSmoothing()
        timeFin = time.time()

        print("Searching for best smoothing: ", timeFin - timeIni, " seconds")
        print("Best smoothing: ", best_smoothing)
        
        timeIni = time.time()
        nb = NaiveBayes(featuresCol='features', labelCol='type', smoothing=best_smoothing, modelType="multinomial")
        nb_model = nb.fit(data_train)
        timeFin = time.time()
        predictions = nb_model.transform(data_test)
        nb_metrics = evaluate_model(predictions, ss, labels[1])
        print("ROC: ", nb_metrics[0])
        print("Precision: ", nb_metrics[1])
        print("Kappa: ", nb_metrics[2])
        print("Recall: ", nb_metrics[3])
        print("F1: ", nb_metrics[4])
        print("Training time: ", timeFin - timeIni, " seconds")

    # 3- Decision Tree
    if "decision_tree" in what_to_execute:
        print("\nDecision Tree")
        timeIni = time.time()
        dt = DecisionTreeClassifier(featuresCol='features', labelCol='type', maxDepth=5)
        evaluator = BinaryClassificationEvaluator(labelCol="type", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
        grid = ParamGridBuilder().addGrid(dt.maxDepth, [5, 10, 15]).build()
        cv = CrossValidator(estimator=dt, estimatorParamMaps=grid, evaluator=evaluator)
        cv_model = cv.fit(data_train)
        best_model = cv_model.bestModel
        best_max_depth = best_model._java_obj.getMaxDepth()
        timeFin = time.time()

        print("Searching for best max depth: ", timeFin - timeIni, " seconds")
        print("Best max depth: ", best_max_depth)
        
        timeIni = time.time()
        dt = DecisionTreeClassifier(featuresCol='features', labelCol='type', maxDepth=best_max_depth)
        dt_model = dt.fit(data_train)
        timeFin = time.time()
        predictions = dt_model.transform(data_test)
        dt_metrics = evaluate_model(predictions, ss, labels[2])
        print("ROC: ", dt_metrics[0])
        print("Precision: ", dt_metrics[1])
        print("Kappa: ", dt_metrics[2])
        print("Recall: ", dt_metrics[3])
        print("F1: ", dt_metrics[4])
        print("Training time: ", timeFin - timeIni, " seconds")

    # 4- Random Forest
    if "random_forest" in what_to_execute:
        print("\nRandom Forest")
        timeIni = time.time()
        rf = RandomForestClassifier(featuresCol='features', labelCol='type', numTrees=10, maxDepth=5)
        evaluator = BinaryClassificationEvaluator(labelCol="type", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
        grid = ParamGridBuilder().addGrid(rf.maxDepth, [5, 10]).addGrid(rf.numTrees, [5, 10, 15]).build()
        cv = CrossValidator(estimator=rf, estimatorParamMaps=grid, evaluator=evaluator)
        cv_model = cv.fit(data_train)
        best_model = cv_model.bestModel
        best_max_depth = best_model._java_obj.getMaxDepth()
        best_num_trees = best_model._java_obj.getNumTrees()
        timeFin = time.time()

        print("Searching for best max depth and number of trees: ", timeFin - timeIni, " seconds")
        print("Best max depth: ", best_max_depth)
        print("Best number of trees: ", best_num_trees)

        timeIni = time.time()
        rf = RandomForestClassifier(featuresCol='features', labelCol='type', numTrees=best_num_trees, maxDepth=best_max_depth)
        rf_model = rf.fit(data_train)
        timeFin = time.time()
        predictions = rf_model.transform(data_test)
        rf_metrics = evaluate_model(predictions, ss, labels[3])
        print("ROC: ", rf_metrics[0])
        print("Precision: ", rf_metrics[1])
        print("Kappa: ", rf_metrics[2])
        print("Recall: ", rf_metrics[3])
        print("F1: ", rf_metrics[4])
        print("Training time: ", timeFin - timeIni, " seconds")

def evaluate_model(predictions, spark_session, method):
    """
    Función que evalúa el modelo de clasificación y devuelve las métricas obtenidas
    :param predictions: predicciones del modelo
    :param spark_session: sesión de Spark
    :param method: método de clasificación
    :return: métricas obtenidas. [ROC, Precision, Kappa, Recall, F1]
    """

    # ROC
    evaluator = BinaryClassificationEvaluator(labelCol="type", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
    roc = round(evaluator.evaluate(predictions) * 100, 3)
    # Matriz de confusión
    predicciones = predictions.select("prediction", "type").rdd
    metricas = MulticlassMetrics(predicciones)
    valores = metricas.confusionMatrix()
    valores_listado = valores.toArray().tolist()
    negativos_aciertos = int(valores_listado[0][0])
    negativos_error = int(valores_listado[1][0])
    positivos_aciertos = int(valores_listado[1][1])
    positivos_error = int(valores_listado[0][1])
    total = negativos_aciertos + negativos_error + positivos_aciertos + positivos_error

    # Precision
    precision = round(metricas.accuracy * 100, 3)
    # Coeficiente Kappa
    probabilidad_observada = float(positivos_aciertos + negativos_aciertos) / total
    probabilidad_esperada = float(((negativos_aciertos + positivos_error) * (negativos_aciertos + negativos_error)) + ((negativos_error + positivos_aciertos) * (positivos_error + positivos_aciertos))) / (total * total)
    kappa = (float(probabilidad_observada - probabilidad_esperada) / (1 - probabilidad_esperada))
    kappa = round(kappa * 100, 3)
    # Recall
    recall = round(metricas.recall(1.0) * 100, 3)
    # F1
    f1 = round(metricas.fMeasure(1.0) * 100, 3)

    # Guardamos los resultados en un fichero CSV
    resultados = [(str(roc), str(precision), str(kappa), str(recall), str(f1))]
    schema = StructType([
        StructField('ROC', StringType(), False),
        StructField('Precision', StringType(), False),
        StructField('Kappa', StringType(), False),
        StructField('Recall', StringType(), False),
        StructField('F-Score', StringType(), False)
    ])
    resultados_dataframe = spark_session.createDataFrame(resultados, schema)
    resultados_dataframe.write.mode('overwrite').csv(method+'.csv', header=True)    # It creates a folder with multiple files, we will need to merge the CSV files.
    return  [str(roc), str(precision), str(kappa), str(recall), str(f1)]    # Return the metrics. Differente data structure than the one required by writing to file method.