import json

with open('../output/Article Data/Article 4v2.json','r') as infile:
	article_dict = json.load(infile)

count = 0
for article in article_dict['referenced_articles']:
	count += len(article['details']['keywords'][0]['kwd'])
	for lvl1 in article['referenced_articles']:
		# count += 1
		count += len(article['details']['keywords'][0]['kwd'])
		for lvl2 in lvl1['referenced_articles']:
			# count += 1
			count += len(article['details']['keywords'][0]['kwd'])
			for lvl3 in lvl2['referenced_articles']:
				# count += 1
				count += len(article['details']['keywords'][0]['kwd'])

print(str(count))