import os
import news_crawler as nc
import classifier as cf

# save articles to file
def to_file( date, section, URL, context, predict ):
	# make directory if not founded
	base_loc = os.path.abspath("../Resources/news/" + date)
	if not os.path.exists(base_loc): 
		os.mkdir(base_loc)

	# make directory if not founded
	loc = base_loc + "/" + section
	if not os.path.exists(loc): 
		os.mkdir(loc)

	# write title, article
	for i, v in enumerate(context[1]):
		with open(loc+"/"+str(i), "w") as writer:
			writer.write("{!s:s}\n" .format(predict[i]))
			writer.write("{!s:s}\n" .format(URL[i]))
			writer.write("{!s:s}\n" .format(context[0][i]))
			writer.write("{!s:s}\n\n" .format(context[1][i]))


# load section list
def load_section():
	section_list = []
	with open("./base/section.txt", "r") as f:
		while True:
			line = f.readline()
			if not line: break
			
			line = line.replace('\n', '')
			section_list.append(line)

	return section_list


# classify each article in sections
def classify( classifier, article ):
	predict = []
	for i, v in enumerate(article):
		vector  = classifier.features(v)
		predict.append(classifier.predict(vector).tolist()[0])
		
	return predict
		

if __name__ == "__main__":
	date = "2015-11-28"
	baseURL, readURL = nc.load_baseURL()
	section = load_section()

	print("crawl {!s:s}" .format(date))
	
	# get URL
	news_URL = []	
	for i in range(len(section)):
		print("crawling URLs {!s:s}" .format(section[i]))
		if i == 0:   news_URL.append(nc.entertain_URL(baseURL[0], readURL[0], date))
		elif i == 1: news_URL.append(nc.sports_URL(baseURL[1], readURL[1], date))
		else:		 news_URL.append(nc.news_URL(baseURL[i], date))
	
	classifier = cf.classifier()
	
	# get article context
	for i, v in enumerate(news_URL):
		context = []
		print("crawling article {!s:s}" .format(section[i]))
		if i == 0:   context = nc.entertain_context(v)
		elif i == 1: context = nc.sports_context(v)
		else:        context = nc.news_context(v)

		# classify article
		predict = classify(classifier, context[1])
		
		# save to file
		to_file(date, section[i], v, context, predict)
