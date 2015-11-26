import os
from crawl_community import crawl_community

base_loc = "../Resources/community/"

if __name__ == "__main__":
	global base_loc, section

	topic = "인분 교수"
	
	cc = crawl_community()
	context = cc.crawl(topic, scroll = 1)

	loc = base_loc + topic
	if not os.path.exists(loc): os.mkdir(loc)

	for i, c in enumerate(context):
		with open(loc+"/"+str(i), "w") as f:
			f.write("{0}\n{1}\n{2}\n{3}" .format(c[0], c[1], c[2], c[3]))
