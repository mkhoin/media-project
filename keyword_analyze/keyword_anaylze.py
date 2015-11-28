import os.path
import re, math
from konlpy.tag import Mecab
from operator import itemgetter

import util

news_loc = "../Resources/news/"
community_loc = "../Resources/community/"

class keyword_anaylze():
	def __init__( self, date, news_limit = 5, net_limit = 50 ):
		self.section = util.load_file("section.txt")
		self.date = date
		self.news_limit = news_limit
		self.net_limit = net_limit
		self.refer = 0

		self.mecab = Mecab()
		self.exp = re.compile("NN|XR|VA|VV|MAG|VX")
		
		self.temp_net = {}
		self.temp_list = {}
		self.word_net = []	   # relative word and its frequency
		self.word_list = []	   # total word and its frequency (using for PMI)
		self.news = []		   # top # of news
		self.sentiment = [0, 0] # [neg, pos]


	def _add_news( self, context, url, title ):
		if len(self.news) < self.news_limit:
			self.news.append([len(context), url, title])
			self.news.sort()
		else:
			self.news[0] = [len(context), url, title]
			self.news.sort()


	def _add_word( self, words, word_list, senti ):
		for w in words:
			if len(w) < 2: continue

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


	def _traverse_news( self, keyword ):
		global news_loc

		match = 0
	
		keyword_list = keyword.split(" ")
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

				self._add_word(words, self.temp_list, senti)
			
				is_key = True
				for key in keyword_list:
					have_word = False
					for w in words:
						if key in w:
							have_word = True
					if not have_word: is_key = False
				
				if is_key:
					match += 1
					self.refer += 1
					self.sentiment[int(senti)] += 1
					self._add_news(context, url, title)
					self._add_word(words, self.temp_net, senti)

				idx += 1
			
		print(match)


	def _traverse_community( self, keyword ):
		global community_loc
		
		base_loc = community_loc+keyword+"/"
		idx = 0

		print(base_loc)
		while True:
			loc = base_loc+str(idx)
			idx += 1
			if not os.path.isfile(loc): break

			f = open(loc, "r")
			senti   = f.readline().replace("\n", "")
			comm    = f.readline().replace("\n", "")
			title   = f.readline().replace("\n", "")
			context = f.read().replace("\n", "") 
			words   = self._make_morp(context)
			f.close()

			self.sentiment[int(senti)] += 1
			self._add_word(words, self.temp_list, senti)
			self._add_word(words, self.temp_net, senti)

		print(idx)


	def _make_word_net( self ):
		network = []

		words = []
		count = []
		for v in self.word_net:
			words.append(v[0])
			count.append(v[1][0])

		for i, v in enumerate(self.word_list):
			for j, w in enumerate(words):
				if v[0] == w and v[1][0] > 10:
					senti = v[1][2] / v[1][0]
					pmi   = count[j] / v[1][0]
					network.append([w, senti, v[1][0], pmi])

		return network

			
	def anaylze( self, keyword ):
		self._traverse_news(keyword)
		self._traverse_community(keyword)

		# sort word_net
		self.word_net = self._arrange_word_list(self.temp_net)

		if len(self.word_net) > self.net_limit:
			self.word_net = [ self.word_net[i] for i in range(self.net_limit) ]

		# sort word_list
		self.word_list = self._arrange_word_list(self.temp_list)

		# network = [ [word, senti, frequency, PMI] .. ] 
		network = self._make_word_net()

		return self.sentiment, self.news, network
