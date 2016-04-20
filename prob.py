import collections
import matplotlib.pyplot as plt
import numpy as np 
import scipy.stats as stats

#frequency
testlist = [1, 2, 3, 3, 3, 4, 5, 6, 6, 6]
c = collections.Counter(testlist)
print c
count_sum=sum(c.values())
for k,v in c.iteritems():
	print "The frequency of the number " + str(k) + " is " + str(float(v) / count_sum)

#box plot
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
plt.boxplot(x)
plt.show()
plt.savefig("boxplot.png")

#histogram
y = [11, 11, 12, 12, 12, 12, 12, 13, 21, 21, 21, 33, 41, 41, 41, 41, 51, 61, 61, 61, 72, 72, 72, 72, 72, 72, 76, 76, 86, 86, 96, 96]
plt.hist(y, histtype='bar')
plt.show()
plt.savefig("histplot.png")

#qq plot
plt.figure()
test_data = np.random.normal(size=3000)   
graph1 = stats.probplot(test_data, dist="norm", plot=plt)
plt.show()
plt.savefig("qqplot.png")
