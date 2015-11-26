import util
from keyword_anaylze import keyword_anaylze

date  = "2015-11-22"
topic_loc = "../Resources/topic/"

if __name__ == "__main__":
	global topic_loc
	global date

	topic = util.load_file(topic_loc+date+"/rank")

	ka = keyword_anaylze(date)
	senti, net, news = ka.anaylze("김영삼")

	print("{0} : {1}" .format(senti[1], senti[0]))
	print(news)
	for v in net:
		rt = v[1][2] / (v[1][1] + v[1][2])
		print("{0} : {1} {2}" .format(v[0], v[1][2], v[1][1]))


	# TODO
	# PMI, 트와이스, 새누리당 
	# 검색어 뭐로 할지 결정
