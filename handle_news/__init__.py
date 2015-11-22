import os

import classifier as cf

if __name__ == "__main__":
	base_loc = "../Resources/news/2015-11-19/"
	classifier = cf.classifier()

	# load section list
	section_list = []
	with open("section.txt", "r") as f:
		while True:
			line = f.readline()
			if not line: break
			
			line = line.replace('\n', '')
			section_list.append(line)
	
	# classify each article in sections
	for section in section_list:
		idx = 0
		loc = os.path.abspath(base_loc + section)

		f = open(base_loc+"/senti_"+section, "w")

		while True:
			fname = loc+"/"+str(idx)
			# check if file exist or not
			if not os.path.isfile(fname): break
			
			article = open(fname, "r")
			dummy = article.readline()
			dummy = article.readline()
			context = article.read()
			article.close()

			vector  = classifier.features(context)
			predict = classifier.predict(vector).tolist()[0]
			
			f.write("{!s:s}\n" .format(predict))
			idx += 1

		f.close()
