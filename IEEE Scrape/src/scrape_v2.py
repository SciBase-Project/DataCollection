# Author : Aditya Agarwal
# Script to scrape IEEE explore website for journal,issues and artiles data

import json
from bs4 import BeautifulSoup
import urllib.request
import os,sys
import time
import re

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)



# The prefix of updated link to get JSON object inserted in the website using AngularJS
JSON_Data_link 			= "http://ieeexplore.ieee.org/rest/document/"

# Checking existenc of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def get_response(aurl):
	hdr					= {'User-Agent':'Mozilla/5.0'}
	req					= urllib.request.Request(aurl,headers=hdr)
	# response			= urllib.request.urlopen(req)

	while True:
		try: 
			# Waiting 60 seconds to recieve a responser object
			with time_limit(30):
				response			= urllib.request.urlopen(req)
			break
		except Exception:
			print("Error opening url!!")
			continue


	return response

# Procedure to return a parseable BeautifulSoup object of a given url
def get_soup(aurl):
	print(aurl)
	response 			= get_response(aurl)
	soup 				= BeautifulSoup(response,'html.parser')
	return soup


# Getting the major details provided in the abstract tab of an article
def get_details(arnumber):
	details 	= {}

	try:
		details_link		= JSON_Data_link + arnumber + "/abstract"
		response 			= get_response(details_link)
		content				= response.read().decode()
		details 	= json.loads(content)
	except Exception:
		pass

	return details


# Getting the authors' details
def get_authors(arnumber):
	details 	= {}

	try:
		authors_link		= JSON_Data_link + arnumber + "/authors"
		response 			= get_response(authors_link)
		content				= response.read().decode()
		details 	= json.loads(content)
	except Exception:
		pass

	return details


# Getting the references JSON structure provided under the References tab of an article
def get_references(arnumber):
	references 	= {}

	try:
		references_link		= JSON_Data_link + arnumber + "/references"
		response 			= get_response(references_link)
		content				= response.read().decode()
		references 			= json.loads(content)
	except Exception:
		pass

	return references

# Getting the citations JSON structure provided under the References tab of an article
def get_citations(arnumber):
	citations 				= {}

	try:
		citations_link		= JSON_Data_link + arnumber + "/citations"
		response 			= get_response(citations_link)
		content				= response.read().decode()
		citations 			= json.loads(content)
	except Exception:
		pass

	return citations

# Returning the article dictionary consisting of all the required details
def get_article(arnumber):
	article 	= {}

	article["arnumber"] 		= arnumber
	article["details"] 			= get_details(arnumber)
	article["authors"]			= get_authors(arnumber)
	reference_data				= get_references(arnumber)
	try:
		article["references"]	= reference_data['references']
	except KeyError:
		article["references"]	= []
	article["citations"] 		= get_citations(arnumber)

	return article

# Article numbers of each article in the issue link
def get_articles(aurl,adir):
    soup 						= get_soup(aurl)
    link1 						= soup.find('input',{'id':'oqs'})
    link0					 	= soup.find('input',{'id':'submitUrl'})
    try:
        total_number 			= soup.find('div',{'class':'results-display'}).find_all('b')[1].get_text()
    except IndexError:
        total_number 			= "10"
    newurl 						= 'http://ieeexplore.ieee.org' + link0['value'] + link1['value'] + '&rowsPerPage=' + total_number
    fsoup 						= get_soup(newurl)
    try:
    	articles 					= fsoup.find('ul',{'class':'results'}).find_all('li')
    except AttributeError:
    	continue
    count 						= 0
    count_article 				= 0
    for article in articles:
        print('Accessing article index '+str(count_article))
        count_article 			+= 1
        try:
            if article.find('h3').find('a')!= None:
                count 			+= 1
                article_dir 	= adir + '/Article ' + str(count)
                ckdir(article_dir)
                article_no 		= article.find('span').find('input')['id']
                localtime 		= time.asctime(time.localtime(time.time()))
                print('Access time is : '+str(localtime))
                print(article_no)
                article 		= get_article(article_no)
                with open(article_dir+'/ArticleData.json','w') as outfile:
                    json.dump(article,outfile)
        except AttributeError:
            pass


# Creates directories for all the volumes,all the issues of a volume
def get_issues(aurl,adir):
    global i
    global j
    soup 	= get_soup(aurl)
    volumes_dir 	= adir + '/Volumes'
    ckdir(volumes_dir)
    METRICS_dict 	= {}
    metrics 	= soup.find('div',{'class':'jrnl-metrics cf'}).find_all('span')
    if metrics 	== []:
        METRICS_dict['Imfact Factor'] 	= '0'
        METRICS_dict['Eigenfactor'] 	= '0'
        METRICS_dict['Article Influence Score'] 	= '0'
    else:
        try:
            METRICS_dict['Imfact Factor'] 	= str(metrics[0].get_text())
        except IndexError:
            METRICS_dict['Imfact Factor'] 	= '0'
        try:
            METRICS_dict['Eigenfactor'] 	= str(metrics[2].get_text())
        except IndexError:
            METRICS_dict['Eigenfactor'] 	= '0'
        try:
            METRICS_dict['Article Influence Score'] 	= str(metrics[4].get_text())
        except IndexError:
            METRICS_dict['Article Influence Score'] 	= '0'

    with open(adir+'/metrics.json','w') as outfile:
        json.dump(METRICS_dict,outfile)

    try:
        volumes 	= soup.find("div",{"class":'volumes'})
        years 	= volumes.find_all('ul')

    except AttributeError:
        volumes 	= soup.find("div",{'id':'past-issues'}).find('div',{'class':'oa_years'})
        for volume in volumes.find_all('li')[i::]:
            volume_dir 	= volumes_dir + '/' + str(volume.get_text())
            ckdir(volume_dir)
            issue_dir 	= volume_dir + '/Issue 1' 
            ckdir(issue_dir)
            issue_url 	= 'http://ieeexplore.ieee.org' + str(volume.find('a')['href'])
            get_articles(issue_url,issue_dir)
        return

    count_volume 	= i
    for year in years[i:]:
    	count_volume += 1
    	print('Accessing Volume '+str(count_volume))
    	issues 	= year.find_all('a')
    	volume_dir 	= volumes_dir + '/' + str(year['id'].split('-')[1])
    	ckdir(volume_dir)
    	print('Volume dir : '+str(volume_dir))
    	count_issue 	= j
    	for issue in issues[j:]:
    		count_issue += 1
    		print("Accessing issue "+str(count_issue))
    		try:
    			issue_no 	= re.findall(r'Issue: [0-9]+',str(issue.get_text()))[0]
    		except IndexError:
    			issue_no 	= re.findall(r'Issue: [A-Z][0-9]+',str(issue.get_text()))[0]
    		print("Issue Name : "+str(issue_no))
    		issue_no 	= re.sub('[^a-zA-Z0-9 ]','',issue_no)
    		issue_dir 	= volume_dir + '/' + issue_no
    		ckdir(issue_dir)
    		issue_url 	= 'http://ieeexplore.ieee.org' + str(issue['href'])
    		# print('Issue Url : ' + issue_url)
    		get_articles(issue_url,issue_dir)
    	j = 0


if __name__ 	== "__main__":
	if len(sys.argv) != 3 and len(sys.argv) != 4 and len(sys.argv) != 5:
	    print('Illegal number of arguments!! Exiting...')
	    sys.exit(1)

	x 	= int(sys.argv[1])
	y 	= int(sys.argv[2])

	i 	= 0
	j 	= 0

	if len(sys.argv) == 4:
		i 	= int(sys.argv[3]) - 1
		if i < 0 :
			print('Invalid volume number...!! Exiting...')
			sys.exit()


	if len(sys.argv) == 5:
		i 	= int(sys.argv[3]) - 1
		if i < 0 :
			print('Invalid volume number...!! Exiting...')
			sys.exit()

		j 	= int(sys.argv[4]) - 1
		if j < 0 :
			print('Invalid volume number...!! Exiting...')
			sys.exit()

	if x>=y :
	    print('Invalid journal indices..!! Exiting...')
	    sys.exit()

	print('Accessing journals from '+ str(x)+' to ' + str(y))
	# loading journal links from data file
	with open('../data/Journal_data.json','r') as infile:
		Journals_data 	= json.load(infile)

	base_dir 	= '../output/Journal Data'
	ckdir(base_dir)

	count_journal 	= x - 1
	for record in Journals_data['records'][x:y:]:
	    count_journal += 1
	    if record['vj'] != True:
	        print('Accessing journal '+str(count_journal))
	        print(record['title'])
	        journal_dir 	= base_dir + '/'+record['title']
	        ckdir(journal_dir)
	        full_url 	= 'http://ieeexplore.ieee.org' + str(record['publicationLink'])
	        get_issues(full_url,journal_dir)
	        i 	= 0