# -*- coding: utf-8 -*-
"""
Created on Mon May 02 11:46:46 2016

@author: v-wujin
"""

import time
import requests
from dateutil.parser import parse
import collections
import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
import collections
r = requests.get('http://www.citibikenyc.com/stations/json')
from pandas.io.json import json_normalize
df = json_normalize(r.json()['stationBeanList'])
station_ids = df['id'].tolist() 
station_ids = ['_' + str(x) + ' INT' for x in station_ids]
con = lite.connect('citibike.db')
cur = con.cursor()
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")
for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%c'),))
    con.commit()
    
    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = '" + exec_time.strftime('%c') + "';")
    con.commit()

    time.sleep(60)
con.close()

#Analyze#
import pandas as pd
import sqlite3 as lite
import datetime

con = lite.connect('citi_bike.db')
cur = con.cursor()
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer
def keywithmaxval(d):
    """Find the key with the greatest value"""
    return max(d, key=lambda k: d[k])

# assign the max key to max_station
max_station = keywithmaxval(hour_change)
#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
))
import matplotlib.pyplot as plt

plt.bar(hour_change.keys(), hour_change.values())
plt.show()
