# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:01:41 2016

@author: v-wujin
"""

import pandas as pd
data= pd.read_csv("/Users/v-wujin/Desktop/ideal_weight.csv",names=['id','sex','actual','ideal','diff'],header=0)
print data
#remove quotes from sex col#
data['sex']=data['sex'].map(lambda x:x.replace("'",""))
print data
#plot disctribution#
import matplotlib.pyplot as plt
plt.hist(data['actual'],bins=20,alpha=0.5,label='actual')
plt.hist(data['ideal'],bins=20,alpha=0.5,label='ideal')
plt.legend(loc='upper right')
plt.show()
plt.hist(data['diff'],alpha=0.5,label='actual-ideal')
#map sex into categorical#
data['sex']=pd.Categorical(data['sex']).codes
print data['sex']
data.groupby('sex').describe()
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
data_new = data[['actual','ideal','diff']]
target = data['sex']
model = gnb.fit(data_new, target)
y_pred = model.predict(data_new)
print("Number of mislabeled points out of a total %d points: %d" %(data_new.shape[0], (target != y_pred).sum()))

d = {'actual': 145, 'ideal': 160, 'diff': -15}
data=pd.DataFrame(data=d,index=[1])
pred=model.predict(data)
print pred