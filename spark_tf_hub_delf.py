# from pyspark import SparkContext 
# sc = SparkContext("local", "Broadcast app") 
# words_new = sc.broadcast(["scala", "java", "hadoop", "spark", "akka"]) 
# data = words_new.value 
# print "Stored data -> %s" % (data) 
# elem = words_new.value[2] 
# print "Printing a particular element in RDD -> %s" % (elem)

import matplotlib.pyplot as plt
import numpy as np

# Simple data to display in various forms
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

plt.close('all')
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')
# fig.show()
fig.savefig('gs://ufcloudcomputing/cloudComputingProject/outputImage/save.png')
plt.close(fig)