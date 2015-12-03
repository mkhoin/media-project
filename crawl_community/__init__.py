import os

import utils
from crawl_community import crawl_community

date = "2015-12-02"
base_loc = "../Resources/community/"
topic_loc = "../Resources/topic/"

if __name__ == "__main__":
	global base_loc, topic_loc, date

	topics = utils.load_file(topic_loc+date)

	for topic in topics:
		print(topic)
		cc = crawl_community()
		context = cc.crawl(topic, scroll = 20)

		loc = base_loc + topic
		if not os.path.exists(loc): os.mkdir(loc)

		for i, c in enumerate(context):
			with open(loc+"/"+str(i), "w") as f:
				f.write("{0}\n{1}\n{2}\n{3}" .format(c[0], c[1], c[2], c[3]))
