# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
data= pd.read_csv('C:/Users/v-wujin/Desktop/un.csv')
#check number of rows and columns#
data.shape
data.notnull().sum()
data.dtypes
data.country.nunique()
df1=data[['GDPperCapita','lifeMale']]
#deal with missing values#
from sklearn.preprocessing import Imputer
imp=Imputer(missing_values='NaN',strategy='mean',axis=0)
imp.fit(df1)
df2=imp.transform(df1)

df3=pd.DataFrame(df2)
cluster1=df3.values 
from scipy.cluster.vq import kmeans, vq, whiten
cluster1=whiten(cluster1)
centroids1,dist1=kmeans(cluster1,2)
idx1,idxdist1=vq(cluster1,centroids1)
from pylab import plot, show
import numpy as np
plot(cluster1[idx1==0,0],cluster1[idx1==0,1],'ob',cluster1[idx1==1,0],cluster1[idx1==1,0],'or')
plot(centroids1[:,0], centroids1[:,1], 'sg', markersize = 8)
show()

cluster1 = whiten(cluster1)
average_distance = []
for k in range(1,11):
    centroids1,dist1 = kmeans(cluster1,k) 
    idx1,idxdist1 = vq(cluster1,centroids1)
    avg_dist = np.mean(idxdist1)
    average_distance.append(avg_dist)

plot(range(1,11), average_distance)