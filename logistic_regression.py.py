import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from IPython import embed as ip
import statsmodels.api as sm


df = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
df['IR_TF'] = 0 + (df['Interest.Rate'] <= 0.12)
df['Intercept'] = 1
ind_vars = ['Intercept', 'FICO.Score', 'Amount.Requested']

# Spot checks
df["IR_TF"][df['Interest.Rate'] < 0.10].head() # should all be True
df["IR_TF"][df['Interest.Rate'] > 0.13].head() # should all be False

logit = sm.Logit(df['IR_TF'], df[ind_vars])
result = logit.fit()
coeffs = result.params
print coeffs

def logistic_function(fico_score, loan_amount, coefficients):
    b, a1, a2 = coefficients   
    x = b + a1*fico_score + a2*loan_amount
    p = 1./(1.+np.exp(-x))
    return p

p1 = logistic_function(720, 10000, coeffs)
p2 = logistic_function2(720, 10000, result)
print p1
print p2
print p1>0.70

def prep(fico_score, loan_amount, coefficients):
    return logistic_function(fico_score, loan_amount, coefficients) > 0.70
print prep(400, 100000, coeffs)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = ["r" if bool(ib12) else "b" for ib12 in df['IR_TF'] ]
ax.scatter(df['FICO.Score'], df['Amount.Requested'],  df['IR_TF'], 
           c=colors)
ax.set_xlabel('FICO SCORE')
ax.set_ylabel('Amount Requested')
ax.set_zlabel('Interest Below 0.12?')
plt.show()

xmin = df['FICO.Score'].min()
xmax = df['FICO.Score'].max()
ymin = df['Amount.Requested'].min()
ymax = df['Amount.Requested'].max()
N = 10
x = np.linspace(xmin, xmax, 20)
y = np.linspace(ymin, ymax, 20)
X, Y = np.meshgrid(x,y)
Z = logistic_function(X,Y,coeffs)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = ["r" if bool(ib12) else "b" for ib12 in df['IR_TF'] ]
ax.scatter(df['FICO.Score'], df['Amount.Requested'],  df['IR_TF'], 
           c=colors)
preds = result.predict(df[ind_vars])
ax.scatter(df['FICO.Score'], df['Amount.Requested'],  preds, c="y")
ax.plot_wireframe(X,Y,Z,alpha=0.5)
ax.set_xlabel('FICO SCORE')
ax.set_ylabel('Amount Requested')
ax.set_zlabel('Interest Below 0.12?')
plt.show()

