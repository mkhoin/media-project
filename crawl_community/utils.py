import csv

def find_dup_idx( seq, item ):
	location = []
	start = -1
	
	while True:
		try: loc = seq.index(item, start+1)
		except ValueError: break
		else:
			location.append(loc)
			start = loc

	return location


def load_reviews( name ):
	with open(name, "r") as csv_file:
		reader = csv.reader(csv_file)	
		data = [ r for r in reader ]

	return data


def load_dictionary():
	csv_pos = open("../Resources/dictionary/POS_v1.csv", "r")
	csv_neg = open("../Resources/dictionary/NEG_v1.csv", "r")
	
	# load dictionary from csv file
	read_pos = csv.reader(csv_pos)
	read_neg = csv.reader(csv_neg)
	
	pos = [ r for r in read_pos ]
	neg = [ r for r in read_neg ]

	# merge to one dictionary
	bag_pos = []
	bag_neg = []
	bag = [bag_pos, bag_neg]
	for r in pos: bag[0].append((r[0], r[1]))
	for r in neg: bag[1].append((r[0], r[1]))

	csv_pos.close()
	csv_neg.close()

	return bag

