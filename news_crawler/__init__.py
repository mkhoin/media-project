import os
import news_crawler as nc

# save articles to file
def to_file( date, section, URL, context ):
	# make directory if not founded
	base_loc = os.path.abspath("./data/" + date)
	if not os.path.exists(base_loc): 
		os.mkdir(base_loc)

	for i, v in enumerate(context):
		# make directory if not founded
		loc = base_loc + "/" + section[i]
		if not os.path.exists(loc): 
			os.mkdir(loc)

		# write title, article
		for j, w in enumerate(v[1]):
			with open(loc+"/"+str(j), "w") as writer:
				writer.write("{!s:s}\n" .format(URL[i][j]))
				writer.write("{!s:s}\n\n" .format(v[0][j]))
				writer.write(w)
		

if __name__ == "__main__":
	date = "2015-11-19"
	baseURL, readURL = nc.load_baseURL()
	
	# get section list
	section = []
	with open("./base/section.txt", "r") as f:
		while True:
			line = f.readline()
			if not line: break

			line = line.replace('\n', '')
			section.append(line)

	print("crawl {!s:s}" .format(date))
	
	# get URL
	news_URL = []	
	for i in range(len(section)):
		print("crawling URLs {!s:s}" .format(section[i]))
		if i == 0:   news_URL.append(nc.entertain_URL(baseURL[0], readURL[0], date))
		elif i == 1: news_URL.append(nc.sports_URL(baseURL[1], readURL[1], date))
		else:		 news_URL.append(nc.news_URL(baseURL[i], date))

	# get article context
	context = []
	for i, v in enumerate(news_URL):
		print("crawling article {!s:s}" .format(section[i]))
		if i == 0:   context.append(nc.entertain_context(v))
		elif i == 1: context.append(nc.sports_context(v))
		else:        context.append(nc.news_context(v))

	print("saving to file")
	to_file(date, section, news_URL, context)
