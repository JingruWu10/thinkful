from scipy import stats
import collections

#Loads data
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

#cleans data
loansData.dropna(inplace=True)

#performs chi squared
chi, p = stats.chisquare(freq.values())

#prints
print chi, p
