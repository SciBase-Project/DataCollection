# Author : Aditya Agarwal
# Script to scrape IEEE explore website for journal,issues and artiles data

import json
from bs4 import BeautifulSoup
import urllib.request


# The prefix of updated link to get JSON object inserted in the website using AngularJS
JSON_Data_link 		= "http://ieeexplore.ieee.org/rest/document/"


# Procedure to return a parseable BeautifulSoup object of a given url
def get_soup(aurl):
	hdr				= {'User-Agent':'Mozilla/5.0'}
	req				= urllib.request.Request(aurl,headers=hdr)
	html			= urllib.request.urlopen(req)
	soup 			= BeautifulSoup(html,'html.parser')
	return soup


# Getting the major details provided in the abstract tab of an article
def get_details(arnumber):
	details = {}

	try:
		details_link	= JSON_Data_link + arnumber + "/abstract"
		soup = get_soup(details_link)
		details = json.loads(str(soup))
	except Exception:
		pass

	return details


# Getting the references JSON structure provided under the References tab of an article
def get_references(arnumber):
	references = {}

	try:
		references_link	= JSON_Data_link + arnumber + "/references"
		soup = get_soup(references_link)
		references = json.loads(str(soup))
	except Exception:
		pass

	return references

# Getting the citations JSON structure provided under the References tab of an article
def get_citations(arnumber):
	citations = {}

	try:
		citations_link	= JSON_Data_link + arnumber + "/citations"
		soup = get_soup(citations_link)
		citations = json.loads(str(soup))
	except Exception:
		pass

	return citations

# Returning the article dictionary consisting of all the required details
def get_article(arnumber):
	article = {}

	article["arnumber"] = arnumber
	article["details"] = get_details(arnumber)
	article["references"] = get_references(arnumber)['references']
	article["citations"] = get_citations(arnumber)

	return article

if __name__ == '__main__':
	arnumber = "6656866"
	print('Getting main article')
	article_dict = get_article(arnumber)

	""" Uncomment the following two lines if only the article structure is required"""
	# with open('./output.json','w') as outfile:
	# 	json.dump(article_dict,outfile)

	""" Comment the following lines if next two level of reference article details are not required"""
	article_dict['referenced_articles'] = []
	for reference in article_dict['references']:
		try:
			if len(reference['links']) >= 5:
				print('Getting next referred article.')
				reference_link = reference['links']['documentLink']
				reference_number = reference_link.split('/').pop()
				referred_article = get_article(reference_number)

				referred_article['referenced_articles'] = []
				for reference2 in referred_article['references']:
					try:
						if len(reference2['links']) >= 5:
							print('Getting next level 2 referred article.')
							reference_link2 = reference2['links']['documentLink']
							reference_number2 = reference_link2.split('/').pop()
							referred_article2 = get_article(reference_number2)

							referred_article['referenced_articles'].append(referred_article2)
					except KeyError:
						pass

				article_dict['referenced_articles'].append(referred_article)
		except KeyError:
			pass

	with open('./output.json','w') as outfile:
		json.dump(article_dict,outfile)