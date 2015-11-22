import json
import dictionary as dc


def export_txt(fname, data):
	with open(fname, "w") as f:
		for d in data:
			f.write("{0:}\n" .format(d))


if __name__ == "__main__":
	raw = dc.parse_json("../Resources/review/review_2.json")
	
	review_pos = []
	review_neg = []

	for r in raw:
		if   r[0] > 8: review_pos.append(r[1])
		elif r[0] < 3: review_neg.append(r[1])

	export_txt("../Resources/review/review_pos", review_pos)
	export_txt("../Resources/review/review_neg", review_neg)


