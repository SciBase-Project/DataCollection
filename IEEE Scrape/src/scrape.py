from bs4 import BeautifulSoup
import sys,urllib2
import json

# loading journal links from data file

# with open('../data/Journal_data.json','r') as infile:
# 	Jounrnals_data = json.load(infile)
# print(str(Jounrnals_data['records'][0]['publicationLink']))


# printing data of the journal

# baseurl = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=85'
# hdr = {'User-Agent':'Mozilla/5.0'}
# req = urllib2.Request(baseurl,headers=hdr)
# page = urllib2.urlopen(req)	
# soup = BeautifulSoup(page, 'html.parser')
# volumes = soup.find("div",{"class":'volumes'})
# years = volumes.find_all('ul')
# for year in years:
# 	issues = year.find_all('a')
# 	print(year['id'])
# 	for issue in issues:
# 		print(issue['href'])