import os
import urllib.request

def get_quotes(t, location):
    url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&g=d&a=0&b=29&c=1993&ignore=.csv' % (t)
    urldata = urllib.request.urlopen(url).read()
    f=open(os.path.join(location,'%s_current.csv' % t ), 'wb' )
    f.write(urldata)
    f.close()












