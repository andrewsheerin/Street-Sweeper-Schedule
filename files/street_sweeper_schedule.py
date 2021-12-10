#install these libraries
from mip import *
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#read NOAA weather data from 2020 in PVD to DataFrame
df = pd.read_csv('rain_noaa.csv')
df.drop(index=df.index[0],axis=0, inplace=True)
df['DATE'] = pd.to_datetime(df['DATE'])

#convert rain data in NOAA dataframe to list
rain = df['PRCP'].tolist()

I = range(len(rain))


#Define Model M
m = Model()
m = Model(sense=MAXIMIZE, solver_name=CBC)

#Add binary decision variable: to sweep or not to sweep
x = [m.add_var(var_type=BINARY) for i in I]


#Variable to track accumulation
acc = []
acc_i = 0 #pounds
acc_rate = 50 #pounds/day

for i in I:
    
    #Accumulation rate function
    acc_i = acc_i + acc_rate*(np.log10(i+1))
    
    #Sensitivity for intensity of rainfall
    if rain[i] >= 0.2:
        acc_i = 0

    #Append into accumulation list
    acc.append(acc_i)



sw_eff = 0.89 #Street sweeper pollution removal efficiency (%)
op_cost = 100 #operational cost ($)

#Define Objective
m.objective = maximize(xsum(sw_eff*acc[i] * x[i] for i in I))

######Constraints#######

#Budget Constraint
m += xsum(op_cost*x[i] for i in I) <= 1000

#No sweeping between January 1 and March 1
m += xsum(x[i] for i in range(0,59)) == 0

#No sweeping between November 1 and Decemeber 31
m += xsum(x[i] for i in range (305, 365)) == 0

# Must sweep at least once a month
m += xsum(x[i] for i in range(60,90)) >= 2       #March
m += xsum(x[i] for i in range(91,120)) >= 1      #April
m += xsum(x[i] for i in range(121,151)) >= 1     #May
m += xsum(x[i] for i in range(152,181)) >= 1     #June
m += xsum(x[i] for i in range(182, 212)) >= 1    #July
m += xsum(x[i] for i in range(213, 242)) >= 1    #August
m += xsum(x[i] for i in range(243, 273)) >= 1    #Septemeber
m += xsum(x[i] for i in range(274, 304)) >= 2    #October

#Cannot sweep more than once in a 10 day span
low = 0
high = 10
for k in range(355):
    K = range(low, high)
    m += xsum(x[i] for i in K) <= 1
    low = low + 1
    high = high + 1


#Start optimization
m.optimize()

days = [i for i in I if x[i].x == True]
pollremoved = [acc[i] for i in I if x[i].x == True]

print("On days: {}".format(days))
print("Pollution removed: {}".format(pollremoved))

total_poll = 0
for i in pollremoved:
    total_poll = total_poll + i
print('Total Pollution Removed:', total_poll)


fig, ax1 = plt.subplots(figsize = (15,10))

ax1.set_title('Acccumulation and Precipitation Tracker',fontweight='bold',fontsize=15)
color = 'tab:green'
ax1.set_xlabel('DATE',fontsize=12)
dtFmt = mdates.DateFormatter('%M/%D')
ax1.xaxis.set_major_formatter(dtFmt)
ax1.set_ylabel('Accumulation (pounds)', color=color, fontsize=12)
ax1.plot(df['DATE'], acc, label = 'Accumulation', color=color, linewidth = 4)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Precipitation (inches)', color=color, fontsize=12)  # we already handled the x-label with ax1
ax2.bar(df['DATE'], rain, label = 'Precipitation', color=color, width = 1)
ax2.tick_params(axis='y', labelcolor=color)


dtFmt = mdates.DateFormatter('%m/%Y')
plt.gca().xaxis.set_major_formatter(dtFmt)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
fig.autofmt_xdate()
fig.legend(loc = 'upper left')
fig.tight_layout()  

plt.savefig('acc_rain.jpg')

