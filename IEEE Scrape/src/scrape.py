from bs4 import BeautifulSoup
import sys,urllib2
import json

# loading journal links from data file

# with open('../data/Journal_data.json','r') as infile:
# 	Jounrnals_data = json.load(infile)
# print(str(Jounrnals_data['records'][0]['publicationLink']))


# printing data of the journal

eurl = 'http://ieeexplore.ieee.org'
# url = ''
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

baseurl = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6336544&punumber=6287639'
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib2.Request(baseurl,headers=hdr)
page = urllib2.urlopen(req)	
soup = BeautifulSoup(page, 'html.parser')

link1 = soup.find('input',{'id':'oqs'})
link0 = soup.find('input',{'id':'submitUrl'})
total_number = soup.find('div',{'class':'results-display'}).find_all('b')[1].get_text()

newurl = eurl + link0['value'] + link1['value'] + '&rowsPerPage=' + total_number

req = urllib2.Request(newurl,headers=hdr)
page = urllib2.urlopen(req).read()
fsoup = BeautifulSoup(page, 'html.parser')
articles = fsoup.find('ul',{'class':'results'}).find_all('li')
for article in articles:
	if article.find('h3').find('a') != None:
		print(article.find('span').find('input')['id'])