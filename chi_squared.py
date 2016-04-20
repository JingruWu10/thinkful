from scipy import stats
import collections
import pandas as pd

#Loads data
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

#cleans data
loansData.dropna(inplace=True)
freq=collections.Counter(loansData['Open.CREDIT.Lines'])
#performs chi squared
chi, p = stats.chisquare(freq.values())

#prints
print chi, p

