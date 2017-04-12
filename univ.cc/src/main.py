from bs4 import BeautifulSoup
import urllib.request
import json

import unicodedata,ast
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


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('[_-]', ' ', text)
    return text


hdr 									= {'User-Agent':'Mozilla/5.0'}
institution_list						= []

def get_response(aurl):
	req 								= urllib.request.Request(aurl,headers=hdr)
	# response			= urllib.request.urlopen(req)

	while True:
		try: 
			# Waiting 60 seconds to recieve a responser object
			with time_limit(30):
				response				= urllib.request.urlopen(req)
			break
		except Exception:
			print("Error opening url!!")
			continue

	return response

def get_soup(aurl):
	html								= get_response(aurl)
	soup 								= BeautifulSoup(html,'html.parser')
	return soup


url 									= "http://univ.cc/world.php"
USA_url 								= "http://univ.cc/states.php"
search_country							= "http://univ.cc/search.php?dom="
search_town								= "http://univ.cc/search.php?town="


def get_institutes(city_url,country,city):
	town 								= get_soup(city_url)
	records								= town.find('ol').find_all('li')
	for record in records:
		# print(record.get_text())
		institution 				= text_to_id(record.get_text())
		temp						= {"institution":institution,"city":city,"country":country}
		print(temp)
		institution_list.append(temp)

def get_cities(country_url,country):
	country_soup						= get_soup(country_url)
	towns								= country_soup.find('select').find_all('option')
	for town in towns[1:]:
		code							= town['value']
		# print(city.get_text().split('(')[0][:-1])
		city							= text_to_id(town.get_text().split('(')[0][:-1])
		c_url 							= search_town+code
		get_institutes(c_url,country,city)


def get_countries(aurl):
	soup 								= get_soup(aurl)
	options								= soup.find('select').find_all('option')
	for option in options[1:]:
		code							= option['value']
		# print(option.get_text().split('(')[0])
		country 						= option.get_text().split('(')[0]
		if country[-1] == ' ':
			country 					= country[:-1]
		country 						= text_to_id(country)
		search_url						= search_country+code
		get_cities(search_url,country)


def get_USA(aurl):
	soup 								= get_soup(aurl)
	options								= soup.find('select').find_all('option')
	for option in options[1:]:
		code							= option['value']
		# print(option.get_text().split('(')[0])
		# country 							= option.get_text().split('(')[0]
		search_url						= search_country+code
		get_cities(search_url,"USA")


get_countries(url)
# get_USA(USA_url)


with open('../output/list.json','w') as outfile:
	json_object							= {'list':institution_list}
	json.dump(json_object,outfile)