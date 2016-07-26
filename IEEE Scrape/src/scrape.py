from bs4 import BeautifulSoup
import sys,urllib2
import json
import os
import re

DETAILS_LINK = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber='
AUTHORS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='
REFERENCE_LINK = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber='
CITATIONS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber='
KEYWORDS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber='
METRICS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractMetrics.jsp?arnumber='

# Creating existence of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

# getting the parseable object for an url
def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	areq = urllib2.Request(aurl,headers=hdr)
	apage = urllib2.urlopen(areq).read()
	asoup = BeautifulSoup(apage,'html.parser')
	return asoup


# Article numbers of each article in the issue link
def get_articles(aurl):
	soup = get_soup(aurl)
	link1 = soup.find('input',{'id':'oqs'})
	link0 = soup.find('input',{'id':'submitUrl'})
	total_number = soup.find('div',{'class':'results-display'}).find_all('b')[1].get_text()
	newurl = 'http://ieeexplore.ieee.org' + link0['value'] + link1['value'] + '&rowsPerPage=' + total_number

	fsoup = get_soup(newurl)
	articles = fsoup.find('ul',{'class':'results'}).find_all('li')
	for article in articles:
		if article.find('h3').find('a') != None:
			print(article.find('span').find('input')['id'])


# Creates directories for all the volumes,all the issues of a volume
def get_issues(aurl,adir):
	soup = get_soup(aurl)

	volumes_dir = adir + '/Volumes'
	ckdir(volumes_dir)
	METRICS_dict = {}
	metrics = soup.find('div',{'class':'jrnl-metrics cf'}).find_all('span')
	if metrics == []:
		METRICS_dict['Imfact Factor'] = '0'
		METRICS_dict['Eigenfactor'] = '0'
		METRICS_dict['Article Influence Score'] = '0'
	else:
		METRICS_dict['Imfact Factor'] = str(metrics[0].get_text())
		METRICS_dict['Eigenfactor'] = str(metrics[2].get_text())
		METRICS_dict['Article Influence Score'] = str(metrics[4].get_text())

	with open(adir+'metrics.json','w') as outfile:
		json.dump(METRICS_dict,outfile)

	try:
		volumes = soup.find("div",{"class":'volumes'})
		years = volumes.find_all('ul')

	except AttributeError:
		volumes = soup.find("div",{'id':'past-issues'}).find('div',{'class':'oa_years'})
		for volume in volumes.find_all('li'):
			print(volume.get_text())
			volume_dir = volumes_dir + '/' + str(volume.get_text())
			ckdir(volume_dir)
			issue_dir = volume_dir + '/Issue 1' 
			ckdir(issue_dir)
			# print(volume.find('a')['href'])
			issue_url = 'http://ieeexplore.ieee.org' + str(volume.find('a')['href'])
			# get_articles(issue_url)
		return

	for year in years:
		issues = year.find_all('a')
		print(year['id'].split('-')[1])
		volume_dir = volumes_dir + '/' + str(year['id'].split('-')[1])
		for issue in issues:
			issue_no = re.findall(r'Issue: [0-9]+',str(issue.get_text()))[0]
			issue_no = re.sub('[^a-zA-Z0-9 ]','',issue_no)
			print(issue_no)
			# print(issue['href'])
			# issue_url = 'http://ieeexplore.ieee.org' + str(issue['href'])
			# get_articles(issue_url)


# loading journal links from data file
with open('../data/Journal_data.json','r') as infile:
	Journals_data = json.load(infile)

base_dir = '../output/Journal Data'
ckdir(base_dir)

for record in Journals_data['records']:
	if record['vj'] != True:
		print(record['title'])
		journal_dir = base_dir + '/'+record['title']
		ckdir(journal_dir)
		full_url = 'http://ieeexplore.ieee.org' + str(record['publicationLink'])
		get_issues(full_url,journal_dir) 