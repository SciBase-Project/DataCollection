from bs4 import BeautifulSoup
import sys,urllib2


baseurl = 'http://ieeexplore.ieee.org/xpl/aboutJournal.jsp?punumber=6287639'
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib2.Request(baseurl,headers=hdr)
page = urllib2.urlopen(req)	
soup = BeautifulSoup(page, 'html.parser')
print(soup)