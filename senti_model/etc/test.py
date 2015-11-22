import classifier as cf
import csv, re
import numpy as np
from konlpy.tag import Mecab

if __name__ == "__main__":
	# initalize Mecab tagger
	tagger = Mecab()
	# include POS
	# include MAG, VX to handle negation
	POS = "NN|XR|VA|VV|MAG|VX"
	# initalize regular expression	 
	exp = re.compile(POS, re.IGNORECASE)
	
	# load sentiment dictionary
	bag = cf.load_dictionary()

	# load training reviews from file	
	train_review = cf.load_reviews("./samples/test_data")
	# get feature from train data
	train_data, train_label = cf.feature_data(tagger, exp, bag, train_review)

	ff = [ i for i, data in enumerate(train_data) if sum(data) != 0 ]
	dd = [ i for i, data in enumerate(train_data) if sum(data) == 0 ]

	tt = [ train_review[i] for i in ff ]
	ta = [ train_label[i] for i in ff ]
	xx = [ train_review[i] for i in dd ]

	with open("./samples/m/test_data", "w") as csv_train:	
		writer = csv.writer(csv_train, delimiter=",", quotechar="|")
		for i, d in enumerate(tt):
			writer.writerow(d)
