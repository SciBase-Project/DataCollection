import json
import glob
import pprint

input_dir	= "../output/Journal Data/raw_data"
output_dir	= "../output/Journal Data/journal_files/"
journal_dir = glob.glob(input_dir+'/*')
# print(journal_dir)


def structute_article(data):
	required = {}
	try:
		required["doi"]			= data["details"]["doi"]
	except KeyError:
		return None
	try:
		required["title"]		= data["details"]["title"]
	except KeyError:
		required["title"]		= None
	try:
		required["keywords"]	= data["details"]["keywords"]
	except KeyError:
		required["keywords"]	= None
	try:
		required["publisher"]	= data["details"]["publisher"]
	except KeyError:
		required["publisher"]	= None
	try:
		required["abstract"]	= data["details"]["abstract"]
	except KeyError:
		required["abstract"]	= None

	required["Metrics"]			= {}
	required["Metrics"]["Citation Count"]			= None
	required["Metrics"]["Downloads (6 weeks) "] 	= None
	required["Metrics"]["Downloads (12 months)"]	= None
	required["Metrics"]["Downloads (cumulative)"]	= None

	required["authors"]			= []
	if "authors" in data["details"]:
		for author in data["details"]["authors"]:
			temp = {}
			try:
				temp["name"]		= author["name"]
			except KeyError:
				continue
			try:
				temp["affiliation"] = author["affiliation"]
			except KeyError:
				temp["affiliation"] = None
			temp["city"]			= None
			temp["country"]			= None
			temp["university"]		= None

			required["authors"].append(temp)

	try:
		required["arnumber"]	= data["arnumber"]
	except KeyError:
		required["arnumber"]	= None

	required["references"] 		= []
	for reference in data["references"]:
		temp					= {}
		try:
			temp["text"]		= reference["text"]
		except KeyError:
			continue
		try:
			temp["title"] 		= reference["title"]
		except KeyError:
			temp["title"] 		= None
		try:
			temp["link"]		= reference["links"]["crossRefLink"]
		except KeyError:
			temp["link"]		= None
		
		required["references"].append(temp)

	required["citations"]		= []
	try:
		if "paperCitations" in data["citations"]:
			if "ieee" in data["citations"]["paperCitations"]:
				for citation in data["citations"]["paperCitations"]["ieee"]:
					temp = {}
					try:
						temp["text"] = citation["text"]
					except KeyError:
						continue
					try:
						temp["title"] = citation["title"]
					except KeyError:
						temp["title"] = None

					temp["link"] = None
					if "links" in citation:
						if "documentLink" in citation["links"]:
							temp["link"] = "http://ieeexplore.ieee.org" + citation["links"]["documentLink"]

					temp["authors"] 				= {}
					temp["authors"]["country"]		= None
					temp["authors"]["city"]			= None
					temp["authors"]["affiliation"]	= None
					required["citations"].append(temp)
	except Exception:
		pass

	return required


for journal in journal_dir:
	print(journal)
	journal_dict = {"ISSN":None}
	with open(journal+"/metrics.json",'r') as infile:
		journal_dict["metrics"] = json.load(infile)

	Volumes = {}	# Dictionary to store all volumes

	volumes = glob.glob(journal+"/Volumes/*")
	for volume in volumes:
		print(volume)
		volume_index= volume.split('/').pop()
		issue_dirs  = glob.glob(volume+"/Issue*")

		for issue in issue_dirs:
			print(issue)
			issue_index  = issue.split('/').pop()
			article_dirs = glob.glob(issue+"/Article*")

			for article in article_dirs:
				print(article)
				article_index = article.split('/').pop()
				try:
					with open(article+"/FilteredArticle.json",'r') as infile:
						article_data	= json.load(infile)
				except FileNotFoundError:
					pass

				volume_no 		= article_data["details"]["volume"]
				issue_no 		= article_data["details"]["issue"]

				if "volume "+volume_no not in Volumes:
					Volumes["volume "+volume_no] = {}

				if "issue "+issue_no not in Volumes["volume "+volume_no]:
					Volumes["volume "+volume_no]["issue "+issue_no] = {}

				article_dict = structute_article(article_data)
				if article_dict:
					Volumes["volume "+volume_no]["issue "+issue_no][article_index] = article_dict



		journal_dict["volumes"] = Volumes

	# pprint.pprint(journal_dict)

	journal_name = journal.split('/').pop()
	with open(output_dir+journal_name,'w') as outfile:
		json.dump({"Data":journal_dict},outfile)