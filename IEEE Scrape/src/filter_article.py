import json
import glob
import os

def filter_article(article_dict,article):
	result = {}

	try:
		result["arnumber"] = article_dict["arnumber"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["references"] = article_dict["references"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["citations"] = article_dict["citations"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e

	result["details"] = {}

	try:
		result["details"]["title"] = article_dict["details"]["title"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["authors"] = article_dict["details"]["authors"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["keywords"] = article_dict["details"]["keywords"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["publisher"] = article_dict["details"]["publisher"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["abstract"] = article_dict["details"]["abstract"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["doi"] = article_dict["details"]["doi"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["volume"] = article_dict["details"]["volume"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["issue"] = article_dict["details"]["issue"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e
	try:
		result["details"]["link"] = article_dict["details"]["persistentLink"]
	except Exception as e:
		pass
		print(article + " : " + str(e))
		# raise e

	return result


if __name__ == "__main__":
	base_dir = "../output/Journal Data/raw_data/"
	journals = glob.glob(base_dir+"/*")
	for journal in journals:
		print(journal)
		volumes = glob.glob(journal+'/Volumes/*')
		for volume in volumes[:]:
			print(volume)
			issues = glob.glob(volume+"/*")
			for issue in issues[:]:
				# print(issue)
				articles = glob.glob(issue+"/*")
				for article in articles[:]:
					# print(article)
					try:
						with open(article+"/ArticleData.json","r") as infile:
							article_dict = json.load(infile)
							new_article_dict = filter_article(article_dict,article)
							with open(article+"/FilteredArticle.json","w") as outfile:
								json.dump(new_article_dict,outfile)
					except FileNotFoundError:
						pass