import re, pickle
import numpy as np
from konlpy.tag import Mecab
from sklearn import preprocessing

# my python file
import utils
from model import NaiveBayes, SVM

# include POS, MAG, VX to handle negation
POS = "NN|XR|VA|VV|MAG|VX"

POS_IDX = ["NN", "VA", "VV", "XR"]

# "못"은 따로 처리
NEG_PREV = [("아니하", "VX"), ("않", "VX"), ("없", "VA"), ("없이", "MAG")]
NEG_NEXT = [("안", "MAG")]

def handle_negation(bag, words, counter):
	global NEG_PREV, NEG_NEXT

	# construct index to negate word except "못"
	neg_idx = []
	for neg in NEG_PREV:
		find = utils.find_dup_idx(words, neg)
		for item in find:
			if item-1 > -1: neg_idx.append(item-1)
	for neg in NEG_NEXT:
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
		if words[i] in bag[0]:
			try: idx = POS_IDX.index(words[i][1])
			except ValueError: pass
			else:	
				counter[idx]   -= 1
				counter[idx+4] += 1
		elif words[i] in bag[1]:
			try: idx = POS_IDX.index(words[i][1])
			except ValueError: pass
			else:
				counter[idx]   += 1
				counter[idx+4] -= 1

	return counter	

def make_features(bag, sentence, words):
	global POS_IDX

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
		if words[i] in bag[0]: # positive
			try:
				idx = POS_IDX.index(words[i][1])
				counter[idx] += 1
			except ValueError: pass
		elif words[i] in bag[1]: # negative	
			try:
				idx = POS_IDX.index(words[i][1])
				counter[idx+4] += 1
			except ValueError: pass

	counter = handle_negation(bag, words, counter)
	return counter

		
def feature_data(tagger, exp, bag, review):
	data  = []
	label = []
	for r in review:
		# tagging review
		pos = tagger.pos(r[1])
		words = [ p for p in pos if exp.search(p[1]) ]

		# construct data sets
		data.append(make_features(bag, r[1], words))
		label.append(r[0])

	# normalize features
	for i, v in enumerate(data):
		arr = np.array(v, dtype=float)
		scaled = preprocessing.scale(arr).tolist()
		data[i] = scaled
		
	return data, label


def evaluate_model(result, labels):
	err = (result == labels).mean() * 100

	r_pos = labels.count('1')
	r_neg = labels.count('0')
	tp = 0
	tn = 0

	for i, r in enumerate(labels):
		if   r == '1' and r == result[i]: tp += 1
		elif r == '0' and r == result[i]: tn += 1

	print("accuracy : {:.2f}%" .format(err))
	print("TPR : {:.2f}%" .format(100*(tp/r_pos)))
	print("TNR : {:.2f}%" .format(100*(tn/r_neg)))
			

if __name__ == "__main__":
	global POS
	
	# initalize Mecab tagger
	tagger = Mecab()

	# initalize regular expression	
	exp = re.compile(POS, re.IGNORECASE)
	
	# load sentiment dictionary
	bag = utils.load_dictionary()

	# load model if exist
	try:
		with open("./models/model", "rb") as model_file:
			model = pickle.load(model_file)
	except IOError as err:
		# load training reviews from file	
		train_review = utils.load_reviews("./samples/train_data")
		# get feature from train data
		train_data, train_label = feature_data(tagger, exp, bag, train_review)
		# initalize classifer class
		model = SVM()
		# train model
		model.train(train_data, train_label)
		#save model
		with open("./models/model", "wb") as model_file:
			pickle.dump(model, model_file)
	else:
		print("use saved model..")
	
	# load test reviews from file
	#test_review  = utils.load_reviews("./samples/test_data")
	# get feature from test data
	#test_data, test_label = feature_data(tagger, exp, bag, test_review)
	
	# predict model
	result = model.predict(train_data)

	# evaluate accuracy
	evaluate_model(result, train_label)

	with open("fault", "w") as ff:
		for i, v in enumerate(train_data):
			if result[i] != train_label[i]:
				ff.write("real:{0!s:s}: {1!s:s}\n" .format(train_review[i][0], train_review[i][1]))
				ff.write("[{0:f} {1:f} {2:f} {3:f} {4:f} {5:f} {6:f} {7:f}\n" .format(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]))


