import util
from keyword_anaylze import keyword_anaylze

date  = "2015-11-28"
topic_loc = "../Resources/topic/"

if __name__ == "__main__":
	global topic_loc
	global date

	topic = util.load_file("topic.txt")

	ka = keyword_anaylze(date)
	senti, news, network = ka.anaylze(topic[0])

	print("{0:.1f}% ({1})" .format(senti[1]/(senti[1]+senti[0])*100, (senti[1]+senti[0])))
	
	for n in news:
		print(n[1])
		print(n[2])

	print("[word, senti, frequency, PMI]")
	for n in network:
		print("[{0}, {1:.1f}%, {2}, {3:.4f}]" .format(n[0], n[1]*100, n[2], n[3]))
