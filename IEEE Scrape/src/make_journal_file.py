import json
import glob
import pprint

output_dir	= "../output/Journal Data"
journal_dir = glob.glob(output_dir+'/*')

for journal in journal_dir[1:8]:

	journal_dict = {}
	with open(journal+"/metrics.json",'r') as infile:
		journal_dict["metrics"] = json.load(infile)

	volumes = glob.glob(journal+"/Volumes/*")
	for volume in volumes:
		volume_index= volume.split('/').pop()
		issue_dirs  = glob.glob(volume+"/Issue*")

		volume_dict = {}
		for issue in issue_dirs:
			issue_index  = issue.split('/').pop()
			article_dirs = glob.glob(issue+"/Article*")

			issue_dict = {}
			for article in article_dirs:
				article_index = article.split('/').pop()
				with open(article+"/ArticleData.json",'r') as infile:
					issue_dict[article_index] = json.load(infile)

			volume_dict[issue_index] = issue_dict

		journal_dict[volume_index] = volume_dict

	pprint.pprint(journal_dict)

	journal_name = journal.split('/').pop()
	with open("../output/Combined data/"+journal_name,'w') as outfile:
		json.dump(journal_dict,outfile)