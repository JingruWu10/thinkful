# -*- coding: utf-8 -*-
"""
Created on Mon May 02 14:06:58 2016

@author: v-wujin
"""

import requests
import sqlite3 as lite
import datetime

api_key = "<2a5cc1558ea67e1d0d4b6287ff30c9ae>"
url = 'https://api.forecast.io/forecast/' + api_key

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }

end_date = datetime.datetime.now()
con = lite.connect('weather.db')
cur = con.cursor()
cities.keys()
with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp;')    
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Atlanta REAL, Austin REAL, Boston REAL, Chicago REAL, Cleveland REAL);') 
#use your own city names instead of city1...
query_date = end_date - datetime.timedelta(days=30) #the current value being processed
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (query_date.strftime('%Y-%m-%dT%H:%M:%S'),))
        query_date += datetime.timedelta(days=1)

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
  #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT%H:%M:%S'))
        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%Y-%m-%dT%H:%M:%S'))
        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day
con.close() # a good practice to close connection to database