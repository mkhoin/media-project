import csv

def load_reviews():
	train_pos = []
	train_neg = []
	test_pos = []
	test_neg = []

	with open("train_pos", "r") as f:
		train_pos.extend(f.read().splitlines())

	with open("train_neg", "r") as f:
		train_neg.extend(f.read().splitlines())
	
	with open("test_pos", "r") as f:
		test_pos.extend(f.read().splitlines())
	
	with open("test_neg", "r") as f:
		test_neg.extend(f.read().splitlines())

	return train_pos, train_neg, test_pos, test_neg


def export_csv(train_pos, train_neg, test_pos, test_neg):
	with open("train_data", "w") as csv_train:	
		writer = csv.writer(csv_train, delimiter=",", quotechar="|")
		for d in train_pos:
			writer.writerow([1, d])
		for d in train_neg:
			writer.writerow([0, d])

	with open("test_data", "w") as csv_test:	
		writer = csv.writer(csv_test, delimiter=",", quotechar="|")
		for d in test_pos:
			writer.writerow([1, d])
		for d in test_neg:
			writer.writerow([0, d])



if __name__ == "__main__":
	train_pos, train_neg, test_pos, test_neg = load_reviews()
	export_csv(train_pos, train_neg, test_pos, test_neg)
