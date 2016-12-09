# Author : Aditya Agarwal
# Script to scrape IEEE explore website for journal,issues and artiles data

import json
from bs4 import BeautifulSoup
import urllib.request


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
JSON_Data_link 		= "http://ieeexplore.ieee.org/rest/document/"

def get_response(aurl):
	hdr				= {'User-Agent':'Mozilla/5.0'}
	req				= urllib.request.Request(aurl,headers=hdr)
	# response		= urllib.request.urlopen(req)

	while True:
		try: 
			# Waiting 60 seconds to recieve a responser object
			with time_limit(30):
				response		= urllib.request.urlopen(req)
			break
		except Exception:
			print("Error opening url!!")
			continue


	return response

# Procedure to return a parseable BeautifulSoup object of a given url
def get_soup(aurl):
	response 		= get_response(aurl)
	soup 			= BeautifulSoup(response,'html.parser')
	return soup


# Getting the major details provided in the abstract tab of an article
def get_details(arnumber):
	details = {}

	try:
		details_link	= JSON_Data_link + arnumber + "/abstract"
		response 		= get_response(details_link)
		content			= response.read().decode()
		details = json.loads(content)
	except Exception:
		pass

	return details


# Getting the references JSON structure provided under the References tab of an article
def get_references(arnumber):
	references = {}

	try:
		references_link	= JSON_Data_link + arnumber + "/references"
		response 		= get_response(references_link)
		content			= response.read().decode()
		references = json.loads(content)
	except Exception:
		pass

	return references

# Getting the citations JSON structure provided under the References tab of an article
def get_citations(arnumber):
	citations = {}

	try:
		citations_link	= JSON_Data_link + arnumber + "/citations"
		response 		= get_response(citations_link)
		content			= response.read().decode()
		citations = json.loads(content)
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

def get_nested_references(article_dict,n):

	article_dict['referenced_articles'] = []

	for reference in article_dict['references']:
		try:
			if len(reference['links']) >= 5:
				print('Getting next referred article. n='+str(n))
				reference_link = reference['links']['documentLink']
				reference_number = reference_link.split('/').pop()

				referred_article = get_article(reference_number)

				if n > 1:
					get_nested_references(referred_article,(n-1))

				# referred_article['referenced_articles'] = []
				# for reference2 in referred_article['references']:
				# 	try:
				# 		if len(reference2['links']) >= 5:
				# 			print('Getting next level 2 referred article.')
				# 			reference_link2 = reference2['links']['documentLink']
				# 			reference_number2 = reference_link2.split('/').pop()
				# 			referred_article2 = get_article(reference_number2)

				# 			referred_article['referenced_articles'].append(referred_article2)
				# 	except KeyError:
				# 		pass

				article_dict['referenced_articles'].append(referred_article)
		except KeyError:
			pass

if __name__ == '__main__':
	# arnumber = "1104315"
	arnumbers = ["4399115","4069507","752023"]
	count = 1
	for arnumber in arnumbers:
		count += 1
		print('Getting main article. Article count : '+str(count))
		article_dict = get_article(arnumber)

		# """ Uncomment the following two lines if only the article structure is required"""
		# # with open('./output.json','w') as outfile:
		# # 	json.dump(article_dict,outfile)

		# """ Comment the following lines if next two level of reference article dnetails are not required"""
		get_nested_references(article_dict,3)
		# # article_dict['referenced_articles'] = []
		# # for reference in article_dict['references']:
		# # 	try:
		# # 		if len(reference['links']) >= 5:
		# # 			print('Getting next referred article.')
		# # 			reference_link = reference['links']['documentLink']
		# # 			reference_number = reference_link.split('/').pop()
		# # 			referred_article = get_article(reference_number)

		# # 			referred_article['referenced_articles'] = []
		# # 			for reference2 in referred_article['references']:
		# # 				try:
		# # 					if len(reference2['links']) >= 5:
		# # 						print('Getting next level 2 referred article.')
		# # 						reference_link2 = reference2['links']['documentLink']
		# # 						reference_number2 = reference_link2.split('/').pop()
		# # 						referred_article2 = get_article(reference_number2)

		# # 						referred_article['referenced_articles'].append(referred_article2)
		# # 				except KeyError:
		# # 					pass

		# # 			article_dict['referenced_articles'].append(referred_article)
		# # 	except KeyError:
		# # 		pass

		with open('./mitchell'+str(count)+'.json','w') as outfile:
			json.dump(article_dict,outfile)