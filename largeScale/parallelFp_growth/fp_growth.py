import os,sys
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
import json

json_file = open('configuration.json')
data = json.load(json_file)

spark = SparkSession.builder.master("local").appName("fpGrowth").getOrCreate()
#
#
#
file= spark.sparkContext.textFile(data['input']) 
#
filedf=file.filter(lambda x: x != "").map(lambda k: Row(k.strip().split(","))).toDF(['items'])
#

fpGrowth = FPGrowth(itemsCol="items", minSupport=data['support'], minConfidence=data['confidence'])
##
##
model = fpGrowth.fit(filedf)

#
dfFinal=model.associationRules.toPandas() 
##
#
dfFinal.to_csv(data['output'], index=False)


spark.stop()


#