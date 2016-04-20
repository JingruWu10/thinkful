import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import statsmodels.api as sm

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

## cleaning the file
loansData['Interest.Rate'] = loansData['Interest.Rate'].str.rstrip('%').astype(float).round(2) / 100.0

loanlength = loansData['Loan.Length'].str.strip('months')#.astype(int)  --> loanlength not used below

loansData['FICO.Score'] = loansData['FICO.Range'].str.split('-', expand=True)[0].astype(int)

#add interest rate less than column and populate
## we only care about interest rates less than 12%
loansData['IR_TF'] = loansData['Interest.Rate'] < 0.12

#create intercept column
loansData['Intercept'] = 1.0

# create list of ind var col names
ind_vars = ['FICO.Score', 'Amount.Requested', 'Intercept'] 

#define logistic regression
logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

#fit the model
result = logit.fit()

#get fitted coef
coeff = result.params

#print coeff
print result.summary() #result has more information
print coeff

def logistic_function(fico_score, loan_amount, coefficients):
    b, a1, a2 = coefficients   
    x = b + a1*fico_score + a2*loan_amount
    p = 1./(1.+np.exp(-x))
    return p

p1 = logistic_function(720, 10000, coeff)
print p1
print p1>0.70

def prep(fico_score, loan_amount, coefficients):
    return logistic_function(fico_score, loan_amount, coefficients) > 0.70
print prep(400, 100000, coeff)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = ["r" if bool(ib12) else "b" for ib12 in loansData['IR_TF'] ]
ax.scatter(loansData['FICO.Score'], loansData['Amount.Requested'],  loansData['IR_TF'], 
           c=colors)
ax.set_xlabel('FICO SCORE')
ax.set_ylabel('Amount Requested')
ax.set_zlabel('Interest Below 0.12?')
plt.show()

#plot your data and surface#
xmin = loansData['FICO.Score'].min()
xmax = loansData['FICO.Score'].max()
ymin = loansData['Amount.Requested'].min()
ymax = loansData['Amount.Requested'].max()
N = 10
x = np.linspace(xmin, xmax, 20)
y = np.linspace(ymin, ymax, 20)
X, Y = np.meshgrid(x,y)
Z = logistic_function(X,Y,coeff)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = ["r" if bool(ib12) else "b" for ib12 in loansData['IR_TF'] ]
ax.scatter(loansData['FICO.Score'], loansData['Amount.Requested'],  loansData['IR_TF'], 
           c=colors)
preds = result.predict(loansData[ind_vars])
ax.scatter(loansData['FICO.Score'], loansData['Amount.Requested'],  preds, c="y")
ax.plot_wireframe(X,Y,Z,alpha=0.5)
ax.set_xlabel('FICO SCORE')
ax.set_ylabel('Amount Requested')
ax.set_zlabel('Interest Below 0.12?')
plt.show()

