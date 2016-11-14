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



def getbarsraw(symbol,mtype,start,end):
    url = 'http://localhost:5000/barData?symbol=%s&historyType=%d&beginTime=%s000000&endTime=%s000000' % (symbol,mtype,start,end)
    return urllib.request.urlopen(url).read().decode('utf-8').strip()


def parserawbytes(rawdata, fieldarray, delimiter):
    output =[]
    for line in rawdata.split('\r\n'):
        output.append([float(i) for i in line.split(delimiter)])
    output.append(fieldarray)
    #output.reverse()
    return output

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


def getdailybars(symbol,days):
    start=getdayfromnow(days*-1)
    end =getdayfromnow(1)
    rdata =getbarsraw(symbol,1,start,end)
    return parserawbytes(rdata,['datetime','open','high','low','close','volume'],',')


#
#  weekly bar retrieval
#
#
def getweeklybars(symbol,days):
    start=getdayfromnow(days*-1)
    end =getdayfromnow(1)
    rdata =getbarsraw(symbol,2,start,end)
    return parserawbytes(rdata,['datetime','open','high','low','close','volume'],',')


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



#writedailyfile('SPY',5000,'/Users/matthewharrison/DOCUMENTS/MATLAB')
#writeweeklyfile('SPY',5000,'/Users/matthewharrison/DOCUMENTS/MATLAB')

