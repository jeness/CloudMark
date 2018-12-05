import pyspark
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import matplotlib.image as mpimg
import numpy as np
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform
import pickle
import time
from pyspark.sql import SQLContext
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('my_first_app_name').getOrCreate()
conf=SparkConf().setAppName("miniProject").setMaster("local[2]")
sc=SparkContext.getOrCreate(conf)
sqlContext = SQLContext(sc)
file1 = open('feature.txt','rb')
results_dict = pickle.load(file1)
file2 = open('input.txt','rb')
input_dict = pickle.load(file2)
data_list = list(results_dict.keys())
stored_data = list(results_dict.values())
image_input_path = list(input_dict.keys())
input_data = list(input_dict.values())

test=pd.DataFrame(input_dict)
data=pd.DataFrame(results_dict)

#schema = StructType([
#StructField("localizations", ArrayType(),True),
#StructField("descriptors", FloatType(), True)
#])

#print(input_dict)
rdd = sc.parallelize(input_dict)
print(rdd.collect())


#print(test)
sdf1 = spark.createDataFrame(test, ArrayType(FloatType()))
#sdf2 = spark.createDataFrame(data, schema)
sdf1.show()

#print(data)
#print(test)

i = len(image_input_path)
j = len(data_list)

a=[1,2,3,4,5,6,7,8,9,0]
b=[0,9,8,7,6,5,4,3,2,1]
c=[2,3,4,5,6,7,8,9,0,1]
d=[9,8,7,6,5,4,3,2,1,0]

#locationsRDD= sc.parallelize(a)
#print(locationsRDD.glom().collect())
#descriptorsRDD = sc.parallelize(b)
#print(descriptorsRDD.glom().collect())


def toDate(s):
    return str(s)+'-'

def match_images(a,b):
	x = a + b
	
	return x

#test = (lambda locationsRDD,descriptorsRDD:match_images(locationsRDD,descriptorsRDD))
#print(test.collect())


# 2.???????
#from pyspark.sql.functions import udf
#from pyspark.sql.types import StringType

# ??python?????????spark???????
# python???????string,???pyspark?StringType
#toDateUDF=udf(toDate, StringType())  
#UDF = toDateUDF('aoigaod')
#print(UDF.show())




#numbersRDD = []
#numbersRDD.append(sc.parallelize(range(1,10+1)))
#print(numbersRDD[0].glom().collect())


