import urllib.request
import datetime
import os
#
# This module gives us raw bar data
#
#  the bar data format is simple, its an array where the first element is a list of the field names
#
#





#
# Date formaty functions
#
# because the API is weird with its start end dates,
def gettoday():
    today = datetime.date.today()
    return '%d%02d%02d' % (today.year,today.month,today.day)
# get i day   +1 for future,  -1 for past
def getdayfromnow(i):
    day = datetime.date.today() + datetime.timedelta(days=i)
    return '%d%02d%02d' % (day.year,day.month,day.day)



#
#  raw bar retrieval
#
#

#for intraday min = 1-60 mins
def getintrabarsraw(symbol,min,start,end):
    url = 'http://localhost:5000/barData?symbol=%s&historyType=0&intradayMinutes=%s&beginTime=%s000000&endTime=%s000000' % (symbol,min,start,end)
    return urllib.request.urlopen(url).read().decode('utf-8').strip()
#print (getdailybarsraw('SPY',15,'20160407','20160408'))


def getbarsraw(symbol,mtype,start,end):
    url = 'http://localhost:5000/barData?symbol=%s&historyType=%d&beginTime=%s000000&endTime=%s000000' % (symbol,mtype,start,end)
    return urllib.request.urlopen(url).read().decode('utf-8').strip()
#print (getbarsraw('SPY',1,'20160301','20160408'))
#print (getbarsraw('SPY',2,'20160301','20160408'))

def parserawbytes(rawdata, fieldarray, delimiter):
    output =[]
    for line in rawdata.split('\r\n'):
        output.append([float(i) for i in line.split(delimiter)])
    output.append(fieldarray)
    #output.reverse()
    return output
#print(parserawbytes(getintrabarsraw('SPY',15,'20160407','20160408'),['time','open','high','low','close','volume'],','))


#
#  intraday bar retrieval
#
#

def getintradaybars(symbol,min,days):
    start=getdayfromnow(days*-1)
    end =getdayfromnow(1)
    rdata =getintrabarsraw(symbol,min,start,end)
    return parserawbytes(rdata,['datetime','open','high','low','close','volume'],',')


#
#  daily bar retrieval
#
#



def getbarsraw(symbol,mtype,start,end):
    url = 'http://localhost:5000/barData?symbol=%s&historyType=%d&beginTime=%s000000&endTime=%s000000' % (symbol,mtype,start,end)
    return urllib.request.urlopen(url).read().decode('utf-8').strip()
#print (getbarsraw('SPY',1,'20160301','20160408'))
#print (getbarsraw('SPY',2,'20160301','20160408'))

def getdailybars(symbol,days):
    start=getdayfromnow(days*-1)
    end =getdayfromnow(1)
    rdata =getbarsraw(symbol,1,start,end)
    return parserawbytes(rdata,['datetime','open','high','low','close','volume'],',')
#print(getdailybars('SPY',20))

#
#  weekly bar retrieval
#
#
def getweeklybars(symbol,days):
    start=getdayfromnow(days*-1)
    end =getdayfromnow(1)
    rdata =getbarsraw(symbol,2,start,end)
    return parserawbytes(rdata,['datetime','open','high','low','close','volume'],',')
#print(getweeklybars('SPY',20))


#
#  convert to printable string to file /w headers
#
#

def printrawdata(rdata,delimiter):
    s = ''
    for row in rdata:
        s += '%s\n' % (delimiter.join(
            [str(i) for i in row]
        ))
    s = s.strip()
    return s
#s= getweeklybars('SPY',20)
#print(printrawdata(s,','))



#
#  convert to to file /w headers
#
#

def writeintrafile(symbol,min,days,filepath):

    filename = '%s_i_%sm_%sd.csv' % (symbol,min,days)
    fp = os.path.join(filepath, filename)
    f = open(fp,'w')
    d = printrawdata(getintradaybars(symbol,min,days),',')
    f.write(d)
    f.close()

def writedailyfile(symbol,days,filepath):
    filename = '%s_1d_%sd.csv' % (symbol,days)
    fp = os.path.join(filepath, filename)
    f = open(fp,'w')
    d = printrawdata(getdailybars(symbol,days),',')
    f.write(d)
    f.close()

def writeweeklyfile(symbol,days,filepath):
    filename = '%s_1w_%sd.csv' % (symbol,days)
    fp = os.path.join(filepath, filename)
    f = open(fp,'w')
    d = printrawdata(getweeklybars(symbol,days),',')
    f.write(d)
    f.close()

#writeintrafile('SPY',15,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeintrafile('SPY',30,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeintrafile('SPY',60,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeintrafile('SPY',120,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeintrafile('SPY',180,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeintrafile('SPY',240,1000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
writedailyfile('SPY',5000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
writeweeklyfile('SPY',5000,'/Users/matthewharrison/DOCUMENTS/MATLAB')

