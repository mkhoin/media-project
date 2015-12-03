import util
from keyword_anaylze import keyword_anaylze

date  = "2015-12-02"
topic_loc = "../Resources/topic/"
result_loc = "../Resources/result/"

if __name__ == "__main__":
	global topic_loc, result_loc
	global date

	topic = util.load_file(topic_loc+date)

	for tp in topic:
		print(tp)

		ka = keyword_anaylze(date)
		senti, news, network = ka.anaylze(tp)
		
		f = open(result_loc+tp, "w")
		f.write("{0:.1f}% (p:{1}, n:{2})\n\n" .format(senti[1]/(senti[1]+senti[0])*100, senti[1], senti[0]))
		for n in news:
			f.write("{0}\n{1}\n\n" .format(n[1], n[2]))

		f.write("[word, senti, frequency, PMI]\n")
		for n in network:
			f.write("[{0}, {1:.1f}%, {2}, {3:.4f}]\n" .format(n[0], n[1]*100, n[2], n[3]))

		f.close()
