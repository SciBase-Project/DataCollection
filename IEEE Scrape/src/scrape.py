from bs4 import BeautifulSoup
import sys,urllib2
import json
import os

# getting the parseable object for an url

def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	areq = urllib2.Request(aurl,headers=hdr)
	apage = urllib2.urlopen(areq).read()
	asoup = BeautifulSoup(apage,'html.parser')
	return asoup

# Creates directories for all the volumes,all the issues of a volume

def get_issues(aurl):
	soup = get_soup(aurl)

	try:
		volumes = soup.find("div",{"class":'volumes'})
		years = volumes.find_all('ul')

	except AttributeError:
		volumes = soup.find("div",{'id':'past-issues'}).find('div',{'class':'oa_years'})
		for volume in volumes.find_all('li'):
			print(volume.get_text())
			print(volume.find('a')['href'])
		return

	for year in years:
		issues = year.find_all('a')
		print(year['id'])
		for issue in issues:
			print(issue['href'])	

# loading journal links from data file

with open('../data/Journal_data.json','r') as infile:
	Jounrnals_data = json.load(infile)
for record in Jounrnals_data['records']:
	if record['vj'] != True:
		print(record['title'])
		full_url = 'http://ieeexplore.ieee.org' + str(record['publicationLink'])
		get_issues(full_url) 

# baseurl = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6336544&punumber=6287639'
# hdr = {'User-Agent':'Mozilla/5.0'}
# req = urllib2.Request(baseurl,headers=hdr)
# page = urllib2.urlopen(req)	
# soup = BeautifulSoup(page, 'html.parser')

# link1 = soup.find('input',{'id':'oqs'})
# link0 = soup.find('input',{'id':'submitUrl'})
# total_number = soup.find('div',{'class':'results-display'}).find_all('b')[1].get_text()

# newurl = eurl + link0['value'] + link1['value'] + '&rowsPerPage=' + total_number

# req = urllib2.Request(newurl,headers=hdr)
# page = urllib2.urlopen(req).read()
# fsoup = BeautifulSoup(page, 'html.parser')
# articles = fsoup.find('ul',{'class':'results'}).find_all('li')
# for article in articles:
# 	if article.find('h3').find('a') != None:
# 		print(article.find('span').find('input')['id'])