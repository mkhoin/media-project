import time
import json, csv
import re 						# regular exp
from konlpy.tag import Mecab    # korean analyzer
from collections import Counter # counting list

n_samples = 10
n_minimum = 100
POS = "[JEXSU]" # exlude POS (use in regular exp)

# load and parse json to list
def parse_json(fname = "sample.json"):
	data = []
	
	f = open(fname, 'r')
	while True:
		line = f.readline()
		if not line: break 
	
		raw = json.loads(line)
		for i in range(n_samples):
			data.append([int(raw['rating'][i]), raw['review'][i]])

	f.close()
	return data


# export result to .csv file
def export_csv(fname, data):
	with open(fname, "w") as csv_file:	
		writer = csv.writer(csv_file, delimiter=",", quotechar="|")
		writer.writerow(["word", "POS", "words", "total", "pr"])
		for d in data:
			writer.writerow([d[0][0], d[0][1], d[1], d[2], d[3]])


# construct bag of sentiment word
def construct_bag(tagger, review_list):
	bag_positive = []
	bag_neutral  = []
	bag_negative = []

	for review in review_list:
		pos = tagger.pos(review[1])

		# exclude unimportant POS (using regular expression)
		exp = re.compile(POS, re.IGNORECASE)
		words = [ p for p in pos if not exp.search(p[1]) ]

		for w in words:
			# rate 0 ~ 4  -> negative
			# rate 5 ~ 7  -> neutral
			# rate 8 ~ 10 -> positive
			if review[0] < 5: 	bag_negative.append(w)
			elif review[0] < 8: bag_neutral.append(w)
			else:				bag_positive.append(w)

	return bag_positive, bag_neutral, bag_negative


# post process with anaylized data
def post_process(bag_positive, bag_neutral, bag_negative):
	# remove duplicated and count it (using collections.Counter)
	pos_counter = Counter(bag_positive)
	neu_counter = Counter(bag_neutral)
	neg_counter = Counter(bag_negative)
	
	# convert Counter to list
	tot = (pos_counter + neu_counter + neg_counter).most_common()
	pos = pos_counter.most_common()
	neu = neu_counter.most_common()
	neg = neg_counter.most_common()
	
	# sepearte element and counts
	bag_pos = [ [(item[0][0], item[0][1]), item[1], 0] for item in pos ]
	bag_neu = [ [(item[0][0], item[0][1]), item[1], 0] for item in neu ]
	bag_neg = [ [(item[0][0], item[0][1]), item[1], 0] for item in neg ]

	# re-format BOW data
	for item in tot:
		# if word occurrence is less than 500, don't collect
		if item[1] < n_minimum: continue

		idx = [i for i, (arg1, arg2, arg3) in enumerate(bag_pos) if arg1 == item[0] ]
		if idx: bag_pos[idx[0]][2] += item[1]

		idx = [i for i, (arg1, arg2, arg3) in enumerate(bag_neu) if arg1 == item[0] ]
		if idx: bag_neu[idx[0]][2] += item[1]
		
		idx = [i for i, (arg1, arg2, arg3) in enumerate(bag_neg) if arg1 == item[0] ]
		if idx: bag_neg[idx[0]][2] += item[1]

	# if word occurrence is less than 500, don't collect
	bag_pos[:] = [ x for x in bag_pos if x[2] != 0 ]
	bag_neu[:] = [ x for x in bag_neu if x[2] != 0 ]
	bag_neg[:] = [ x for x in bag_neg if x[2] != 0 ]

	# calculate probability of occurrence in (positive, neutral, negative)
	for i, v in enumerate(bag_pos): 
		bag_pos[i].append(round(v[1]/v[2], 3))

	for i, v in enumerate(bag_neu): 
		bag_neu[i].append(round(v[1]/v[2], 3))

	for i, v in enumerate(bag_neg): 
		bag_neg[i].append(round(v[1]/v[2], 3))

	return bag_pos, bag_neu, bag_neg


if __name__ == "__main__":
	# use Mecab korean anaylzer
	tagger = Mecab()
	
	# load json file to list
	print("parse json..")
	review_list = parse_json()	
	print("done")

	# construct bag of sentiment
	print("construct bag of sentiment..")
	t1 = time.time()
	bag_positive, bag_neutral, bag_negative = construct_bag(tagger, review_list)
	t2 = time.time()
	print("done {0:.3f}s" .format(t2-t1)) 

	# count all POS
	print("post process..")
	t1 = time.time()
	pos, neu, neg = post_process(bag_positive, bag_neutral, bag_negative)
	t2 = time.time()
	print("done {0:.3f}s" .format(t2-t1))

	# export bag to .csv file
	print("export to csv..")
	export_csv("sample/pos.csv", pos)
	export_csv("sample/neg.csv", neg)
	export_csv("sample/neu.csv", neu)
	print("done")
