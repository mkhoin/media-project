import re, pickle
import numpy as np
from konlpy.tag import Mecab
from sklearn import preprocessing

# my python file
import utils
import model


class classifier():
	# include POS, MAG, VX to handle negation
	POS = "NN|XR|VA|VV|MAG|VX"

	POS_IDX = ["NN", "VA", "VV", "XR"]
	# "못"은 따로 처리
	NEG_PREV = [("아니하", "VX"), ("않", "VX"), ("없", "VA"), ("없이", "MAG")]
	NEG_NEXT = [("안", "MAG")]


	def __init__(self):
		# initalize Mecab tagger
		self.tagger = Mecab()
	
		# initalize regular expression	
		self.exp = re.compile(self.POS, re.IGNORECASE)
		
		# load sentiment dictionary
		self.bag = utils.load_dictionary()
	
		# load model if exist
		with open("../Resources/models/model", "rb") as model_file:
			self.model = pickle.load(model_file)


	def handle_negation(self, words, counter):	
		# construct index to negate word except "못"
		neg_idx = []
		for neg in self.NEG_PREV:
			find = utils.find_dup_idx(words, neg)
			for item in find:
				if item-1 > -1: neg_idx.append(item-1)
		for neg in self.NEG_NEXT:
			find = utils.find_dup_idx(words, neg)
			for item in find:
				if item+1 < len(words): neg_idx.append(item+1)
	
		# handle "못~"
		for w in words:
			loc = w[0].find("못")
			if loc > 0 and w[1].find("VX"): neg_idx.append(loc-1)
		# handle "못"
		for w in words:
			loc = w[0].find("못")
			if loc > -1 and w[1].find("MAG"):
				# 긴 부정문 (못햇다, 못 했다..)
				if loc > 1 and words[loc-1][1].find("VV"): neg_idx.append(loc-1)
				# 짧은 부정
				elif loc < len(words)-1: neg_idx.append(loc+1)
				# 한계: 못 생겼다 같은 경우는 이상하게 나옴
	
		# negate word
		for i in neg_idx:
			if words[i] in self.bag[0]:
				try: idx = self.POS_IDX.index(words[i][1])
				except ValueError: pass
				else:	
					counter[idx]   -= 1
					counter[idx+4] += 1
			elif words[i] in self.bag[1]:
				try: idx = self.POS_IDX.index(words[i][1])
				except ValueError: pass
				else:
					counter[idx]   += 1
					counter[idx+4] -= 1
	
		return counter	
	
	def make_features(self, sentence, words):	
		# feature vector:
		# [ pos_noun, pos_adj, pos_verb, pos_root,
		#   neg_noun, neg_adj, neg_verb, neg_root ]
		counter = [0, 0, 0, 0, 0, 0, 0, 0]
	
		if not words: return counter
		
		for i, w in enumerate(words):
			# replace POS to sentiment dictionary type
			words[i] = list(words[i])
			if   words[i][1].find("NN") >= 0: words[i][1] = "NN"
			elif words[i][1].find("VA") >= 0: words[i][1] = "VA"
			elif words[i][1].find("VV") >= 0: words[i][1] = "VV"
			elif words[i][1].find("XR") >= 0: words[i][1] = "XR"
			elif words[i][1].find("VX") >= 0: words[i][1] = "VX"
			elif words[i][1].find("MAG") >= 0: words[i][1] = "MAG"
			words[i] = tuple(words[i])
	
			# count frequency of sentiment words
			if words[i] in self.bag[0]: # positive
				try:
					idx = self.POS_IDX.index(words[i][1])
					counter[idx] += 1
				except ValueError: pass
			elif words[i] in self.bag[1]: # negative	
				try:
					idx = self.POS_IDX.index(words[i][1])
					counter[idx+4] += 1
				except ValueError: pass
	
		counter = self.handle_negation(words, counter)
		return counter
	
			
	def features(self, article):
		# tagging article
		pos = self.tagger.pos(article)
		words = [ p for p in pos if self.exp.search(p[1]) ]
	
		# construct data sets
		data = self.make_features(article, words)
	
		# normalize features
		arr = np.array(data, dtype=float)
		scaled = preprocessing.scale(arr).tolist()
		data = scaled

		return data


	def predict(self, vector):
		return self.model.predict(vector)
