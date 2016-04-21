# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np 
import statsmodels.api as sm

##### Same as before we did for linear regression

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
print loansData

#print the first 5 rows of each of the column to see what needs to be cleaned
print loansData['Interest.Rate'][0:5]
print loansData['Monthly.Income'][0:5]
print loansData['Home.Ownership'][0:5]

#cleaning up the columns
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)

##### Now the logistic part
intrate = loansData['Interest.Rate']
intrate[np.isnan(intrate)] = 0
monthly_income = loansData['Monthly.Income']
monthly_income[np.isnan(monthly_income)] = 0
## It is not a value, so you need to convert it into we weigh them based on their importance
house_ownership = loansData['Home.Ownership']
house_ownership = [4 if x == 'OWN' else 3 if x == 'MORTGAGE' else 2 if x == 'RENT' else 1 if x == 'OTHER' else 0 for x in house_ownership]

# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns

x3 = np.matrix(monthly_income).transpose()
x4 = np.matrix(house_ownership).transpose()


x = np.column_stack([x3, x4])
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared
