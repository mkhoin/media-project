import os.path
import re
from konlpy.tag import Mecab
from operator import itemgetter

import util

news_loc = "../Resources/news/"

class keyword_anaylze():
	word_net = []	   # relative word and its frequency
	word_list = []	   # total word and its frequency (using for PMI)
	news = []		   # top # of news
	sentiment = [0, 0] # [neg, pos]

	def __init__( self, date, news_limit = 5, net_limit = 50 ):
		self.section = util.load_file("section.txt")
		self.date = date
		self.news_limit = news_limit
		self.net_limit = net_limit
		self.refer = 0

		self.mecab = Mecab()
		self.exp = re.compile("NN|XR|VA|VV|MAG|VX")

		
	def _add_news( self, context, url, title ):
		if len(self.news) < self.news_limit:
			self.news.append([len(context), url, title])
			self.news.sort()
		else:
			self.news[0] = [len(context), url, title]
			self.news.sort()


	def _add_word( self, words, word_list, senti ):
		for w in words:
			if w in word_list:
				word_list[w][0] += 1
				word_list[w][int(senti)+1] += 1
			else:
				word_list[w] = [1, 0, 0]
				word_list[w][int(senti)+1] += 1


	def _make_morp( self, context ):
		context = re.sub(r"(\"|\')", "", context)
		words = re.findall(r"[\w']+", context)
				
		for i, v in enumerate(words):
			pos = self.mecab.pos(v)
			w = [ p[0] for p in pos if not re.search("NN|XR|VA|VV|MAG|VX|SL|SN", p[1]) ]
			for x in w:
				words[i] = words[i].replace(x, "")

		# remove '' in words
		return [ w for w in words if not w == "" ]

	
	def _arrange_word_list( self, dictionary ):
		words = sorted(dictionary.items(), key=itemgetter(1), reverse=True)
		word_list = []
		for w in words:
			pos = self.mecab.pos(w[0])
			if re.search("NN|XR", pos[0][1]):
				word_list.append(w)

		return word_list


	def _traverse_file( self, keyword ):
		global news_loc

		keyword_list = keyword.split(" ")
		temp_net = {}
		temp_list = {}

		for s in self.section:
			idx = 0
			loc = news_loc+self.date+"/"+s

			print(loc+"/")
			while os.path.isfile(loc+"/"+str(idx)):
				f = open(loc+"/"+str(idx), "r")
				senti   = f.readline().replace("\n", "")
				url     = f.readline().replace("\n", "")
				title   = f.readline().replace("\n", "")
				context = f.read().replace("\n", "")
				words   = self._make_morp(context)
				f.close()
				
				self._add_word(words, temp_list, senti)

				is_key = True
				for key in keyword_list:
					if not key in words: is_key = False

				if is_key:
					self.refer += 1
					self.sentiment[int(senti)] += 1
					self._add_news(context, url, title)
					self._add_word(words, temp_net, senti)

				idx += 1

		# sort word_net
		self.word_net = self._arrange_word_list(temp_net)

		if len(self.word_net) > self.net_limit:
			self.word_net = [ self.word_net[i] for i in range(self.net_limit) ]

		# sort word_list
		self.word_list = self._arrange_word_list(temp_list)
					

	def anaylze( self, keyword ):
		self._traverse_file(keyword)
		print(self.refer)

		return self.sentiment, self.word_net, self.news
